# Apply with Tailored Resumes (Pipeline Mode)

> **Multi-agent pipeline for job applications with AI-tailored resumes**
> 
> This command works WITH the Python orchestrator running in the background.
> The orchestrator handles resume tailoring/scoring, this agent handles browser automation.

---

## Prerequisites

### 1. Start the Pipeline Orchestrator (Terminal 1)
```bash
cd /Users/jchung/code/Clicker
export ANTHROPIC_API_KEY="your-key-here"
python3 scripts/pipeline_orchestrator.py
```

### 2. Ensure LaTeX is installed (one-time setup)
```bash
brew install basictex
# Or for full installation: brew install mactex
```

### 3. Then run this command (in Cursor)

---

## Files to Read FIRST

Before starting, read these files to understand the system:

```
config/personal_profile.md       # Personal info for form filling
config/resume_content.md         # All experiences and achievements
config/projects.md               # Project portfolio
config/job_preferences.md        # Search settings, max_applications
data/current_search_plan.md      # Search strategy (if exists)
```

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    MULTI-AGENT PIPELINE                                      │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   YOU (Cursor Agent)                    ORCHESTRATOR (Python - background)   │
│   ┌──────────────────────┐              ┌──────────────────────────────────┐│
│   │ 1. Find job listing  │              │                                  ││
│   │ 2. Extract JD text   │──write──────▶│ data/pipeline/pending_jd.json    ││
│   │ 3. WAIT              │              │                                  ││
│   │                      │              │ 4. Analyze JD (fresh context)    ││
│   │                      │              │ 5. Tailor resume (fresh context) ││
│   │                      │              │ 6. Score (fresh context)         ││
│   │                      │              │ 7. Refine loop until 90%+        ││
│   │                      │              │ 8. Compile PDF                   ││
│   │                      │◀──read───────│ data/pipeline/resume_ready.json  ││
│   │ 9. Read result       │              │                                  ││
│   │ 10. Apply to job     │              │                                  ││
│   │ 11. Log everything   │              │                                  ││
│   │ 12. Next job         │              │                                  ││
│   └──────────────────────┘              └──────────────────────────────────┘│
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Your Role: Browser Automation Agent

You are the BROWSER AUTOMATION agent. Your responsibilities:

1. **Navigate** to job listings
2. **Extract** job descriptions
3. **Signal** the orchestrator (write pending_jd.json)
4. **Wait** for the orchestrator (poll resume_ready.json)
5. **Apply** with the tailored resume
6. **Log** everything to events
7. **Continue** to the next job

You do NOT do resume tailoring or scoring - the orchestrator handles that with FRESH LLM contexts for each phase.

---

## Workflow Protocol

### Phase 1: Session Initialization

```
1. Verify browser is on LinkedIn, signed in
2. Check orchestrator is running:
   - Read data/pipeline/orchestrator_status.json
   - If status != "ready", STOP and tell user to start orchestrator
3. Read max_applications from config/job_preferences.md
4. Log session start to data/events/session_*.jsonl
5. Navigate to LinkedIn Jobs if not already there
```

### Phase 2: Job Processing Loop

For each job until max_applications reached:

```
STEP 1: FIND JOB
- Click on a job listing from search results
- Ensure it's not already applied (check for "Applied" badge)

STEP 2: EXTRACT JOB DESCRIPTION
- Take browser snapshot
- Extract: company name, job title, location, job description text
- Extract the FULL job description (scroll if needed)

STEP 3: SIGNAL ORCHESTRATOR
- Write to data/pipeline/pending_jd.json:
  {
    "company": "...",
    "job_title": "...",
    "location": "...",
    "job_url": "...",
    "description": "full job description text...",
    "timestamp": "ISO timestamp"
  }
- Emit event: {"type": "jd_extracted", ...}

STEP 4: WAIT FOR ORCHESTRATOR
- Poll data/pipeline/resume_ready.json every 2 seconds
- Maximum wait: 5 minutes (orchestrator does tailoring + scoring loop)
- While waiting, you can read orchestrator_status.json for progress updates
- If timeout: log error, skip job, continue

STEP 5: READ RESULT
- Read data/pipeline/resume_ready.json
- Extract: pdf_path, tex_path, score, job_id
- Log the tailoring result

STEP 6: APPLY
- If Easy Apply:
  - Click Easy Apply
  - Fill form using config/personal_profile.md
  - When resume upload is needed: NOTE the tailored resume path for human
  - Submit
- If External:
  - Note this as "pending_manual" - human will use tailored resume
  
STEP 7: LOG AND CONTINUE
- Emit event: {"type": "application_completed", "score": X, ...}
- Delete resume_ready.json (cleanup for next job)
- Increment application counter
- Move to next job listing
```

### Phase 3: Session End

```
1. Log session end to events
2. Create summary of tailored resumes:
   - List all PDFs created in resume/tailored/
   - List any jobs pending manual resume upload
3. Output session statistics
```

---

## File Communication Protocol

### You Write: `data/pipeline/pending_jd.json`

```json
{
  "company": "Google",
  "job_title": "Software Engineer",
  "location": "Mountain View, CA",
  "job_url": "https://linkedin.com/jobs/view/12345",
  "description": "Full job description text here...",
  "timestamp": "2026-01-19T10:30:00Z"
}
```

### You Read: `data/pipeline/resume_ready.json`

```json
{
  "success": true,
  "job_id": "20260119_103000_Google_Software_Engineer",
  "score": 92,
  "pdf_path": "/Users/jchung/code/Clicker/resume/tailored/20260119_103000_Google_Software_Engineer_final.pdf",
  "tex_path": "/Users/jchung/code/Clicker/resume/tailored/20260119_103000_Google_Software_Engineer_final.tex",
  "iterations": 2,
  "company": "Google",
  "job_title": "Software Engineer",
  "job_url": "https://linkedin.com/jobs/view/12345"
}
```

### You Read: `data/pipeline/orchestrator_status.json`

```json
{
  "status": "tailoring",
  "timestamp": "2026-01-19T10:30:15Z",
  "details": {
    "job_id": "20260119_103000_Google_Software_Engineer",
    "phase": "resume_tailoring",
    "iteration": 2
  }
}
```

---

## Event Emission

Log events to `data/events/session_YYYY-MM-DD_NN.jsonl`:

```json
{"type": "session_start", "ts": "...", "session_id": "...", "session_type": "pipeline"}
{"type": "jd_extracted", "ts": "...", "company": "...", "job_title": "..."}
{"type": "tailoring_started", "ts": "...", "job_id": "..."}
{"type": "tailoring_completed", "ts": "...", "job_id": "...", "score": 92, "iterations": 2}
{"type": "application_started", "ts": "...", ...}
{"type": "application_completed", "ts": "...", "status": "applied", "tailored_score": 92}
{"type": "session_end", "ts": "...", "total_applications": 5, "stop_reason": "limit_reached"}
```

---

## Handling the Resume Upload Blocker

For jobs requiring resume upload on external sites:

1. Complete all other form fields
2. Log the job as "pending_upload"
3. Note in the log: "Tailored resume ready at: {pdf_path}"
4. Leave the tab open
5. Continue to next job

The human can later:
1. Check `logs/pipeline/` for pending uploads
2. Find the tailored PDF at `resume/tailored/{job_id}_final.pdf`
3. Manually upload and submit

---

## Session Summary Output

At session end, output:

```
╔═══════════════════════════════════════════════════════════════════════╗
║  SESSION COMPLETE: Pipeline Mode                                       ║
╠═══════════════════════════════════════════════════════════════════════╣
║                                                                        ║
║  Applications: 5 submitted, 2 pending upload                           ║
║                                                                        ║
║  TAILORED RESUMES CREATED:                                             ║
║  ┌────────────────────────────────────────────────────────────────┐   ║
║  │ Company          │ Score │ PDF Location                        │   ║
║  ├──────────────────┼───────┼─────────────────────────────────────┤   ║
║  │ Google           │ 94%   │ resume/tailored/..._Google_...pdf   │   ║
║  │ Meta             │ 91%   │ resume/tailored/..._Meta_...pdf     │   ║
║  │ Amazon           │ 88%   │ resume/tailored/..._Amazon_...pdf   │   ║
║  └────────────────────────────────────────────────────────────────┘   ║
║                                                                        ║
║  PENDING MANUAL UPLOAD (tabs left open):                               ║
║  • Stripe - External site, resume at: resume/tailored/..._Stripe_...   ║
║  • Notion - External site, resume at: resume/tailored/..._Notion_...   ║
║                                                                        ║
║  All tailored resumes saved in: resume/tailored/                       ║
║  Logs available at: logs/pipeline/                                     ║
║                                                                        ║
╚═══════════════════════════════════════════════════════════════════════╝
```

---

## Error Handling

| Situation | Action |
|-----------|--------|
| Orchestrator not running | STOP, tell user to start it |
| Orchestrator timeout (>5 min) | Log error, skip job, continue |
| Tailoring failed | Log error, apply with default resume |
| LaTeX compilation failed | Still have .tex file, note for human |
| Easy Apply succeeds | Log with tailored score |
| External site | Mark pending_upload, note PDF path |

---

## Critical Rules (from .cursorrules)

1. **NEVER STOP FOR FIT REASONS** - Even if the job seems wrong for the candidate
2. **SOFT BLOCKERS → LEAVE TAB OPEN** - Continue session
3. **LOG EVERYTHING** - Events capture the full pipeline
4. **ORCHESTRATOR DOES TAILORING** - You do NOT tailor resumes

---

## Quick Start

1. User starts orchestrator: `python3 scripts/pipeline_orchestrator.py`
2. User runs this command: `/apply-pipeline`
3. You navigate to LinkedIn Jobs
4. For each job: extract JD → wait for tailored resume → apply
5. Session ends when limit reached

The magic happens in the orchestrator - each resume gets FRESH LLM context for consistently high-quality tailoring.

