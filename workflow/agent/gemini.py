"""Minimal Gemini REST client (stdlib only).

Why no SDK (ADR-005): the harness must run anywhere with zero install, and a
hand-rolled client makes retries, fallbacks and token accounting explicit.

The API key is read from the GEMINI_API_KEY environment variable and is never
printed, logged or embedded in a URL (it travels in the x-goog-api-key
header). Token usage is taken from the API's own usageMetadata so the cost
reporting required by the assignment is measured, not estimated.
"""

import json
import http.client
import os
import time
import urllib.error
import urllib.request

import config
import call_log

API_BASE = "https://generativelanguage.googleapis.com/v1beta/models"
_LAST_REQUEST = 0.0


class QuotaExhausted(Exception):
    """Raised when every retry and the fallback tier are rate-limited."""


class BudgetExhausted(Exception):
    """Raised when the per-run token budget (ADR-009) would be exceeded."""


class Usage:
    """Cumulative token accounting for one workflow run."""

    def __init__(self, prior=None):
        prior = prior or {}
        self.prompt_tokens = prior.get("prompt_tokens", 0)
        self.completion_tokens = prior.get("completion_tokens", 0)
        self.total_tokens = prior.get("total_tokens", 0)
        self.calls = prior.get("calls", 0)
        self.fallbacks = prior.get("fallbacks", 0)
        self.models = prior.get("models", {})

    def record(self, metadata):
        self.prompt_tokens += metadata.get("promptTokenCount", 0)
        self.completion_tokens += metadata.get("candidatesTokenCount", 0)
        self.total_tokens += metadata.get("totalTokenCount", 0)
        self.calls += 1

    def as_dict(self):
        return {
            "prompt_tokens": self.prompt_tokens,
            "completion_tokens": self.completion_tokens,
            "total_tokens": self.total_tokens,
            "calls": self.calls,
            "fallbacks": self.fallbacks,
            "models": self.models,
        }


def _quota_info(raw):
    """ADR-033: non-secret quota identity from a 429 body: (quotaId, retry seconds).
    Either may be None. Never raises."""
    try:
        details = json.loads(raw).get("error", {}).get("details", [])
    except (ValueError, AttributeError):
        return None, None
    quota_id = None
    delay = None
    for d in details if isinstance(details, list) else []:
        if not isinstance(d, dict):
            continue
        for v in d.get("violations") or []:
            if isinstance(v, dict) and v.get("quotaId") and quota_id is None:
                quota_id = str(v["quotaId"])[:120]
        rd = d.get("retryDelay")
        if isinstance(rd, str) and rd.endswith("s"):
            try:
                delay = float(rd[:-1])
            except ValueError:
                pass
    return quota_id, delay


def _per_minute(err):
    return "PerMinute" in (getattr(err, "quota_id", None) or "")


def _post(model, payload, api_key):
    global _LAST_REQUEST
    time.sleep(max(0.0, 5.0 - (time.monotonic() - _LAST_REQUEST)))
    _LAST_REQUEST = time.monotonic()
    url = f"{API_BASE}/{model}:generateContent"
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "x-goog-api-key": api_key,
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8", "replace")
        body = raw[:500]
        if e.code == 429:
            err = _RateLimited(body)
            err.http_status = 429
            err.quota_id, err.retry_delay_s = _quota_info(raw)
            raise err
        if 500 <= e.code < 600:
            err = _Transient(f"Gemini API error {e.code}: {body}")
            err.http_status = e.code
            raise err
        err = RuntimeError(f"Gemini API error {e.code}: {body}")
        err.http_status = e.code
        raise err
    except (TimeoutError, ConnectionError, urllib.error.URLError,
            http.client.RemoteDisconnected) as e:
        err = _Transient(f"transport failure: {type(e).__name__}: {e}")
        err.category = "transport"
        raise err from e


_TIER_COOLDOWN_UNTIL = {}


class _RateLimited(Exception):
    pass


class _Transient(Exception):
    """Retryable 5xx from the API, or an empty/candidate-less reply."""



def response_schema(system_prompt):
    """Constrain JSON-as-data actions; no native provider tools are used."""
    string = {"type": "STRING"}
    strings = {"type": "ARRAY", "items": string}
    boolean = {"type": "BOOLEAN"}
    def obj(properties, required=()):
        return {"type": "OBJECT", "properties": properties,
                "required": list(required)}
    if '"pass": true|false' in system_prompt:
        return obj({"pass": boolean, "reasons": strings}, ("pass", "reasons"))
    finding = obj({"file": string, "line": {"type": "INTEGER"},
                   "issue": string, "severity": string})
    failure = obj({"criterion": string, "error": string})
    result = obj({
        "summary": string, "files": strings, "files_changed": strings,
        "acceptance_criteria": strings, "assumptions": strings,
        "blocked": boolean, "reason": string, "notes_for_tester": string,
        "tests_written": strings, "all_pass": boolean,
        "failures": {"type": "ARRAY", "items": failure},
        "criteria_untestable": strings, "verdict": string,
        "findings": {"type": "ARRAY", "items": finding},
        "classification": {"type": "STRING", "nullable": True},
    })
    if "You are the Reviewer agent" in system_prompt:
        result = obj({
            "verdict": {"type": "STRING", "enum": ["approve", "request_changes"]},
            "findings": {"type": "ARRAY", "items": obj({
                "file": string, "line": {"type": "INTEGER"}, "issue": string,
                "severity": {"type": "STRING", "enum": ["blocker", "major", "minor"]}},
                ("file", "line", "issue", "severity"))},
            "classification": {"type": "STRING", "nullable": True},
            "summary": string,
        }, ("verdict", "findings", "classification", "summary"))
    def action(name, fields):
        return obj({"action": {"type": "STRING", "enum": [name]},
                    **fields}, ("action", *fields))
    return {"anyOf": [
        action("list_files", {"path": string}),
        obj({"action": {"type":"STRING","enum":["read_file"]}, "path":string,
             "start_line":{"type":"INTEGER"},"end_line":{"type":"INTEGER"}},
            ("action","path")),
        obj({"action": {"type": "STRING", "enum": ["write_file"]},
             "path": string, "content": string,
             "tables": {"type": "ARRAY", "items": obj({
                 "name": string,
                 "header": {"type": "ARRAY", "items": string},
                 "rows": {"type": "ARRAY", "items": {"type": "ARRAY", "items": string}}},
                 ("name", "header", "rows"))}},
            ("action", "path", "content")),
        action("edit_file", {"path": string, "old_text": string, "new_text": string}),
        action("run_shell", {"command": string}),
        action("finish", {"result": result}),
    ]}



def generate(model, system_prompt, contents, usage, temperature=0.2,
             context=None):
    """One generateContent call with retries, fallback and budget checks.

    contents: list of {"role": "user"|"model", "parts": [{"text": ...}]}
    context: optional provenance dict (role, stage, repo_root, task) -
    every HTTP attempt is logged through call_log (schema autose-call/1).
    Returns the reply text. Raises BudgetExhausted / QuotaExhausted.
    """
    if usage.total_tokens >= config.MAX_TOKENS_PER_RUN:
        raise BudgetExhausted(
            f"token budget {config.MAX_TOKENS_PER_RUN} reached "
            f"({usage.total_tokens} used)"
        )
    api_key = os.environ.get("GEMINI_API_KEY", "")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY is not set")

    context = dict(context or {})
    context.setdefault("system_sha256", call_log.sha256_text(system_prompt))
    if "task_sha256" not in context:
        first = ""
        for entry in contents:
            if entry.get("role") == "user":
                first = "".join(p.get("text", "")
                                for p in entry.get("parts", []))
                break
        context["task_sha256"] = call_log.sha256_text(first)

    context["request_contents_sha256"] = call_log.sha256_text(
        json.dumps(contents, sort_keys=True, separators=(",", ":")))
    payload = {
        "system_instruction": {"parts": [{"text": system_prompt}]},
        "contents": contents,
        "generationConfig": {
            "temperature": temperature,
            "maxOutputTokens": config.MAX_OUTPUT_TOKENS,
            # Agent replies are JSON objects by contract (TOOL_CONTRACT);
            # without this, gemini-3.5-flash-lite answers with
            # finishReason=MALFORMED_FUNCTION_CALL and an empty text part.
            "responseMimeType": "application/json",
            "responseSchema": response_schema(system_prompt),
        },
    }

    # Try the primary model, then one tier down (ADR-006), each with retries.
    models_to_try = [model]
    if model != config.MODEL_FALLBACK:
        models_to_try.append(config.MODEL_FALLBACK)

    last_err = None
    for tier_index, active_model in enumerate(models_to_try):
        # ADR-027: a tier that was just moved off after repeated 429s is
        # skipped while it cools down, as long as a later tier remains.
        if (tier_index < len(models_to_try) - 1
                and time.monotonic() < _TIER_COOLDOWN_UNTIL.get(active_model, 0.0)):
            continue
        consecutive_429 = 0
        for attempt in range(config.API_RETRIES + 1):
            try:
                data = _post(active_model, payload, api_key)
                usage.record(data.get("usageMetadata", {}))
                usage.models[active_model] = usage.models.get(active_model, 0) + 1
                if active_model != model:
                    usage.fallbacks += 1
                candidates = data.get("candidates") or []
                if not candidates:
                    # Preserve every fact the provider did return (usage,
                    # model version, response id) even though the call is
                    # unusable; then record the failure category only.
                    call_log.record(
                        context, model, active_model, "error",
                        usage_metadata=data.get("usageMetadata") or None,
                        provider_model_version=data.get("modelVersion"),
                        response_id=data.get("responseId"),
                        error={"category": "no_candidates",
                               "http_status": None, "finish_reason": None})
                    err = _Transient("Gemini returned no candidates")
                    err.category = "no_candidates"
                    err._logged = True
                    raise err
                parts = candidates[0].get("content", {}).get("parts", [])
                text = "".join(p.get("text", "") for p in parts)
                if not text.strip():
                    finish_reason = candidates[0].get("finishReason", "unknown")
                    call_log.record(
                        context, model, active_model, "error",
                        usage_metadata=data.get("usageMetadata") or None,
                        provider_model_version=data.get("modelVersion"),
                        response_id=data.get("responseId"),
                        error={"category": "empty_reply",
                               "http_status": None,
                               "finish_reason": finish_reason})
                    err = _Transient("empty model reply")
                    err.category = "empty_reply"
                    err._logged = True
                    raise err
                call_log.record(
                    context, model, active_model, "success",
                    usage_metadata=data.get("usageMetadata") or None,
                    provider_model_version=data.get("modelVersion"),
                    response_id=data.get("responseId"))
                return text
            except (_RateLimited, _Transient) as e:
                last_err = e
                # ADR-027: repeated 429 on a tier with a fallback tier left
                # moves to the fallback after RATE_LIMIT_SWITCH_AFTER
                # consecutive 429s instead of waiting out the whole ladder.
                consecutive_429 = (consecutive_429 + 1
                                   if isinstance(e, _RateLimited) else 0)
                if not getattr(e, "_logged", False):
                    call_log.record(
                        context, model, active_model, "error",
                        usage_metadata=None,
                        error=call_log.categorize_error(e))
                # ADR-033: a per-minute 429 clears within the minute, so keep the
                # primary and honour the provider's retry delay; only daily-quota
                # or unidentified 429s switch tiers (the fallback has a small
                # daily budget and must not be spent on a one-minute burst).
                if (consecutive_429 >= config.RATE_LIMIT_SWITCH_AFTER
                        and not _per_minute(e)
                        and tier_index < len(models_to_try) - 1):
                    _TIER_COOLDOWN_UNTIL[active_model] = (
                        time.monotonic() + config.RATE_LIMIT_COOLDOWN_SECONDS)
                    break
                if attempt < config.API_RETRIES:
                    wait = config.API_BACKOFF_SECONDS[
                        min(attempt, len(config.API_BACKOFF_SECONDS) - 1)]
                    delay = getattr(e, "retry_delay_s", None)
                    if _per_minute(e) and delay:
                        wait = min(wait, max(5.0, delay + 2.0))
                    time.sleep(wait)
            except Exception as e:
                # Non-retryable failures (client-error HTTP, decode errors,
                # anything else) are still attempts: record the category,
                # then keep the original control flow.
                call_log.record(
                    context, model, active_model, "error",
                    usage_metadata=None,
                    error=call_log.categorize_error(e))
                raise
        # primary exhausted its retries: fall through to the fallback tier
    raise QuotaExhausted(
        f"model retries exhausted; last error type={type(last_err).__name__}: {last_err}"
    )
