"""Builds the post-disclosure appendix pages and appends them to the frozen 8-page report.

Usage: python build_appendix.py <frozen_report.pdf> <post-disclosure-runs.csv> <out.pdf> "<cutoff text>"
The 8 body pages are not edited. The appendix is labelled late work.
"""
import csv, io, sys
from pypdf import PdfReader, PdfWriter
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

src, csvp, out, cutoff = sys.argv[1:5]
ss = getSampleStyleSheet()
H = ParagraphStyle("H", parent=ss["Heading2"], fontSize=12, spaceBefore=8, spaceAfter=3, keepWithNext=1)
B = ParagraphStyle("B", parent=ss["BodyText"], fontSize=8.6, leading=11)
S = ParagraphStyle("S", parent=B, fontSize=7, leading=8.6, wordWrap="CJK")
def P(t, st=B): return Paragraph(t, st)
rows = list(csv.DictReader(open(csvp)))
post = [r for r in rows if int(r["run_id"]) >= 45504039498]
data = [[P("<b>Run</b>", S), P("<b>Issue</b>", S), P("<b>Started IST</b>", S), P("<b>Furthest stage / outcome</b>", S), P("<b>Cause and configuration</b>", S)]]
for r in post:
    cause = r["cause"]
    data.append([P(r["run_id"], S), P("#" + r["issue"], S), P(r["started_ist"][5:], S),
                 P(f'{r["furthest_stage"]} / {r["outcome"]}', S), P(f'{cause} <i>[{r["config"]}]</i>', S)])
t = Table(data, colWidths=[54, 26, 46, 62, 326], repeatRows=1)
t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.3, colors.grey), ("VALIGN", (0, 0), (-1, -1), "TOP"),
                       ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e8e8e8")),
                       ("LEFTPADDING", (0, 0), (-1, -1), 3), ("RIGHTPADDING", (0, 0), (-1, -1), 3)]))
buf = io.BytesIO()
doc = SimpleDocTemplate(buf, pagesize=A4, leftMargin=40, rightMargin=40, topMargin=40, bottomMargin=40)
el = [P("<b>Appendix A. Post-disclosure update (late work, not part of the 8-page body)</b>", ss["Heading1"]),
      P(f"Written after the report body and after the sealed 10-head evaluation. Figures cut off at: {cutoff}. "
        "Nothing here changes the frozen evaluation results in the body, and nothing here is unseen-test evidence. "
        "Failed, cancelled and negative runs are kept. The automated approve verdict on PR #57 is not a human approval and the PR is not merged."),
      P("A.1 What happened after the evaluation", H),
      P("Fresh issues #35 to #39 were run one at a time from run 16 onward (links: results/post-disclosure-runs.csv, "
        "results/post-disclosure-rerun-log.md). One uninterrupted full chain exists (run 16, issue #36: requirements, design, develop, release, "
        "then an automated review that posted approve; PR #57 open). Every other fresh run stopped earlier. The failure causes, in order of "
        "appearance: provider 503 and 429 errors, a force-with-lease push on a residue branch, malformed markdown table rows written by the model "
        "(the raw model reply itself contains them; the write tool stores content unchanged), a Developer read loop to the 40-step cap, "
        "a 90-minute job timeout, and finally the free daily quota on every model the repo had approved."),
      Spacer(1, 4), t,
      P("A.2 Decisions added (ADR-021 to ADR-034)", H),
      P("ADR-027 early switch to the fallback tier after two 429s. ADR-028 unique branch suffix per retry, so no ref is deleted or force-updated. "
        "ADR-029, 032 deterministic table-row and column-count checks. ADR-030, 031 no-op edit errors and reminder text. ADR-033 quota-aware 429 handling and "
        "logging of the quota id. ADR-034 (proposed, see the repository for its status) structured table data rendered by the harness. No check, judge, step cap "
        "or token limit was loosened in any of them. Each run after a harness or model change is a different configuration and is labelled so in the CSV."),
      P("A.3 Tokens", H),
      P("Exact for call-logged Actions runs: 6,941,374 provider-reported tokens (AutoSE_A3 6,292,067; AutoSE_A3_Alt 649,307), through run 31; 1,058 call records carry no usage because the call failed. "
        "E2 local trials: 597,542 (121,609 plus 475,933). Actions runs before the call log existed: only overlapping per-branch snapshots, at most 4,812,201 for that scope. "
        "The exact lifetime total is unavailable and no lifetime upper bound is proven: manual probes, runs without artifacts and later runs are not included "
        "(results/token-accounting.md lists the omissions). Provider console, read 25 Nov 18:21 IST (UTC-8 windows, one project, all models): the AI Studio project showed 8,535,319 input and 188,806 output tokens over the console's 7-day window (1,271 requests), and 20,803,749 input and 889,930 output over 28 days. These are window totals for the whole project, not an A3-only count, and they are not reconciled to the repository logs (different key scope). The fallback ORION project key has not been measured at the provider (its console needed a sign-in approval that was not completed). Cost: both Gemini projects show Free tier with no billing linked today, and the first account has no Google Cloud billing account; this is current state, not proof of the state before the first run, and not a provider-set hard limit (results/token-accounting.md)."),
      P("A.4 Rubric status", H),
      P("Deliverables present: ADRs (more than 8), three views, five issues with hidden tests held outside the repo, five seeded PRs, README with pinned commit "
        "edff96a and AI-use disclosure, results files, the canonical one-run demo demo_run16.mp4 (2:30, run 45504039498, issue page to posted review; frames checked), the earlier recovered-chain demo.mp4 (3:47, labelled as not one uninterrupted run), submission file. Design-before-code: the ADR and view commit is the parent of "
        "the workflow commit, but both carry the same timestamp. Unmet or partly met: an exact A3-only token total (provider window totals and logged subtotals are reported, not reconciled) and a provider-set hard spending limit verified from before the first run (current console state is free tier, no billing); "
        "and the unanswered E1 question (ADR-006 model tiers: incomplete and confounded, labelled). E1 is not itself a brief requirement, because the brief asks for two tested ADRs and E2 and E3 are those. The brief states no number of successful chains; the observed count is reported as found. See results/rubric-matrix.md."),
      P("A.5 Added limitations", H),
      P("(1) Most post-disclosure runs used one small model for the SpecWriter; its table and file-writing defects are model-generation defects, not harness faults, and the stage check correctly stopped them. "
        "(2) The wording-level check for the words gate and basis in VALIDATION is a proxy for the A1 skill's required summary content, not a test of correctness. "
        "(3) Free-tier daily quotas set how many runs were possible in a day, so run counts reflect quota, not workflow quality. "
        "(4) Post-disclosure runs share the repository with the frozen heads; their branches carry suffixes to avoid touching the frozen heads.")]
doc.build(el)
body = PdfReader(src)
app = PdfReader(io.BytesIO(buf.getvalue()))
w = PdfWriter()
for p in body.pages[:8]: w.add_page(p)  # frozen 8-page body only
for p in app.pages: w.add_page(p)
w.write(open(out, "wb"))
print("body 8 + appendix", len(app.pages))
