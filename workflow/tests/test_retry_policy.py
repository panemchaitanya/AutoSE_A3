"""Offline tests of the patient bounded retry policy (ADR-018).
No API calls, generated issue changes or hidden acceptance tests.
"""
import json,os,subprocess,sys,unittest
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'agent'))
import config,gemini

def ok_payload(text='{"action":"finish","result":{}}'):
 return {'candidates':[{'content':{'parts':[{'text':text}]},'finishReason':'STOP'}],
         'usageMetadata':{'promptTokenCount':3,'candidatesTokenCount':1,'totalTokenCount':4}}

class RetryPolicy(unittest.TestCase):
 def setUp(self):
  gemini._TIER_COOLDOWN_UNTIL.clear()
  os.environ['GEMINI_API_KEY']='offline-fixture'
  self.saved=(config.API_RETRIES,list(config.API_BACKOFF_SECONDS))
  config.API_RETRIES=3
  config.API_BACKOFF_SECONDS=[30,60,120]
 def tearDown(self):
  gemini._TIER_COOLDOWN_UNTIL.clear()
  config.API_RETRIES,config.API_BACKOFF_SECONDS=self.saved
 def test_defaults_are_patient_but_bounded(self):
  env={k:v for k,v in os.environ.items() if not k.startswith('API_')}
  out=subprocess.run([sys.executable,'-c',
   'import config;print(config.API_RETRIES, sum(config.API_BACKOFF_SECONDS), max(config.API_BACKOFF_SECONDS))'],
   cwd=str(Path(__file__).resolve().parents[1]/'agent'),env=env,capture_output=True,text=True)
  retries,total,longest=map(int,out.stdout.split())
  self.assertGreaterEqual(retries,3)
  self.assertGreaterEqual(total,180)   # tolerates short spikes, then falls back fast
  self.assertLessEqual(total,1800)      # still bounded, not an infinite wait
  self.assertLessEqual(longest,300)
 def test_env_override(self):
  env=dict(os.environ,API_RETRIES='6',API_BACKOFF_SECONDS='5,10')
  out=subprocess.run([sys.executable,'-c',
   'import config;print(config.API_RETRIES, config.API_BACKOFF_SECONDS)'],
   cwd=str(Path(__file__).resolve().parents[1]/'agent'),env=env,capture_output=True,text=True)
  self.assertEqual(out.stdout.strip(),"6 [5, 10]")
 def test_spike_then_success_uses_config_without_fallback(self):
  calls=[]
  def fake_post(model,payload,key):
   calls.append(model)
   if len(calls)<3:raise gemini._Transient('503 spike')
   return ok_payload()
  with patch.object(gemini,'_post',side_effect=fake_post),patch.object(gemini.time,'sleep') as slp:
   text=gemini.generate('gemini-primary-x','system',[],gemini.Usage())
  self.assertIn('finish',text)
  self.assertEqual(calls,['gemini-primary-x']*3)
  self.assertEqual([c.args[0] for c in slp.call_args_list if c.args[0]>5],[30,60])
 def test_exhaustion_falls_back_once_then_raises(self):
  calls=[]
  def fake_post(model,payload,key):
   calls.append(model);raise gemini._Transient('still down')
  with patch.object(gemini,'_post',side_effect=fake_post),patch.object(gemini.time,'sleep'):
   with self.assertRaises(gemini.QuotaExhausted):
    gemini.generate('gemini-primary-x','system',[],gemini.Usage())
  self.assertEqual(calls,['gemini-primary-x']*4+[config.MODEL_FALLBACK]*4)

 def test_consecutive_429_switches_to_fallback_early(self):
  calls=[]
  def fake_post(model,payload,key):
   calls.append(model)
   if model=='gemini-primary-x':raise gemini._RateLimited('429')
   return ok_payload()
  with patch.object(gemini,'_post',side_effect=fake_post),patch.object(gemini.time,'sleep') as slp:
   text=gemini.generate('gemini-primary-x','system',[],gemini.Usage())
  self.assertIn('finish',text)
  self.assertEqual(calls,['gemini-primary-x']*config.RATE_LIMIT_SWITCH_AFTER+[config.MODEL_FALLBACK])
  self.assertEqual([c.args[0] for c in slp.call_args_list if c.args[0]>5],[30])
 def test_503_still_uses_full_ladder(self):
  calls=[]
  def fake_post(model,payload,key):
   calls.append(model)
   if len(calls)<4:raise gemini._Transient('503')
   return ok_payload()
  with patch.object(gemini,'_post',side_effect=fake_post),patch.object(gemini.time,'sleep'):
   gemini.generate('gemini-primary-x','system',[],gemini.Usage())
  self.assertEqual(calls,['gemini-primary-x']*4)
 def test_429_on_fallback_tier_not_cut_short(self):
  calls=[]
  def fake_post(model,payload,key):
   calls.append(model);raise gemini._RateLimited('429')
  with patch.object(gemini,'_post',side_effect=fake_post),patch.object(gemini.time,'sleep'):
   with self.assertRaises(gemini.QuotaExhausted):
    gemini.generate('gemini-primary-x','system',[],gemini.Usage())
  self.assertEqual(calls,['gemini-primary-x']*config.RATE_LIMIT_SWITCH_AFTER+[config.MODEL_FALLBACK]*4)

 def test_cooldown_skips_primary_for_later_calls(self):
  calls=[]
  def fake_post(model,payload,key):
   calls.append(model)
   if model=='gemini-primary-x':raise gemini._RateLimited('429')
   return ok_payload()
  with patch.object(gemini,'_post',side_effect=fake_post),patch.object(gemini.time,'sleep'):
   gemini.generate('gemini-primary-x','system',[],gemini.Usage())
   calls.clear()
   gemini.generate('gemini-primary-x','system',[],gemini.Usage())
  self.assertEqual(calls,[config.MODEL_FALLBACK])
 def test_cooldown_never_skips_last_tier(self):
  gemini._TIER_COOLDOWN_UNTIL[config.MODEL_FALLBACK]=gemini.time.monotonic()+999
  calls=[]
  def fake_post(model,payload,key):
   calls.append(model);return ok_payload()
  with patch.object(gemini,'_post',side_effect=fake_post),patch.object(gemini.time,'sleep'):
   gemini.generate('gemini-primary-x','system',[],gemini.Usage())
  self.assertEqual(calls,['gemini-primary-x'])

 def test_cooldown_expires(self):
  calls=[]
  def fake_post(model,payload,key):
   calls.append(model)
   if model=='gemini-primary-x':raise gemini._RateLimited('429')
   return ok_payload()
  with patch.object(gemini,'_post',side_effect=fake_post),patch.object(gemini.time,'sleep'):
   gemini.generate('gemini-primary-x','system',[],gemini.Usage())
   gemini._TIER_COOLDOWN_UNTIL['gemini-primary-x']=gemini.time.monotonic()-1
   calls.clear()
   gemini.generate('gemini-primary-x','system',[],gemini.Usage())
  self.assertEqual(calls,['gemini-primary-x']*config.RATE_LIMIT_SWITCH_AFTER+[config.MODEL_FALLBACK])

if __name__=='__main__':
 unittest.main()


class QuotaAware(unittest.TestCase):
 def setUp(self):
  gemini._TIER_COOLDOWN_UNTIL.clear()
  os.environ['GEMINI_API_KEY']='offline-fixture'
  self.saved=(config.API_RETRIES,list(config.API_BACKOFF_SECONDS))
  config.API_RETRIES=3
  config.API_BACKOFF_SECONDS=[30,60,120]
 def tearDown(self):
  gemini._TIER_COOLDOWN_UNTIL.clear()
  config.API_RETRIES,config.API_BACKOFF_SECONDS=self.saved
 def _err(self,qid,delay):
  e=gemini._RateLimited('429'); e.quota_id=qid; e.retry_delay_s=delay; return e
 def test_quota_info_parses_provider_body(self):
  raw=json.dumps({'error':{'details':[{'violations':[{'quotaId':'GenerateRequestsPerDayPerProjectPerModel-FreeTier'}]},{'retryDelay':'16046s'}]}})
  self.assertEqual(gemini._quota_info(raw),('GenerateRequestsPerDayPerProjectPerModel-FreeTier',16046.0))
  self.assertEqual(gemini._quota_info('not json'),(None,None))
 def test_per_minute_429_stays_on_primary_and_uses_provider_delay(self):
  calls=[]
  def fake_post(model,payload,key):
   calls.append(model)
   if len(calls)<=3:raise self._err('GenerateRequestsPerMinutePerProjectPerModel-FreeTier',12)
   return ok_payload()
  with patch.object(gemini,'_post',side_effect=fake_post),patch.object(gemini.time,'sleep') as slp:
   gemini.generate('gemini-primary-x','system',[],gemini.Usage())
  self.assertEqual(calls,['gemini-primary-x']*4)
  self.assertEqual([c.args[0] for c in slp.call_args_list if c.args[0]>5],[14.0,14.0,14.0])
 def test_daily_429_still_switches_early(self):
  calls=[]
  def fake_post(model,payload,key):
   calls.append(model)
   if model=='gemini-primary-x':raise self._err('GenerateRequestsPerDayPerProjectPerModel-FreeTier',16000)
   return ok_payload()
  with patch.object(gemini,'_post',side_effect=fake_post),patch.object(gemini.time,'sleep'):
   gemini.generate('gemini-primary-x','system',[],gemini.Usage())
  self.assertEqual(calls,['gemini-primary-x']*config.RATE_LIMIT_SWITCH_AFTER+[config.MODEL_FALLBACK])
