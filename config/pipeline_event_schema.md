# Pipeline Event Schema

> **Purpose**: Defines events specific to the multi-agent pipeline mode (`/apply-pipeline`)
> **Format**: JSON Lines (one JSON object per line)
> **Location**: Same as regular events - `data/events/session_YYYY-MM-DD_N.jsonl`

---

## Overview

Pipeline mode introduces additional events for the orchestrator-based resume tailoring workflow.

The orchestrator also logs to `logs/pipeline/pipeline_YYYY-MM-DD.jsonl` for detailed debugging.

---

## Cursor Agent Events (Browser Side)

### `jd_extracted`
Emitted when job description is extracted and sent to orchestrator.

```json
{
  "type": "jd_extracted",
  "ts": "2026-01-19T14:30:22.000Z",
  "session_id": "session_2026-01-19_01",
  "company": "Google",
  "job_title": "Software Engineer",
  "location": "Mountain View, CA",
  "job_url": "https://linkedin.com/jobs/view/123456",
  "description_length": 2500
}
```

### `tailoring_started`
Emitted when the Cursor agent begins waiting for the orchestrator.

```json
{
  "type": "tailoring_started",
  "ts": "2026-01-19T14:30:25.000Z",
  "session_id": "session_2026-01-19_01",
  "job_id": "20260119_143022_Google_Software_Engineer"
}
```

### `tailoring_completed`
Emitted when the orchestrator finishes and resume is ready.

```json
{
  "type": "tailoring_completed",
  "ts": "2026-01-19T14:32:00.000Z",
  "session_id": "session_2026-01-19_01",
  "job_id": "20260119_143022_Google_Software_Engineer",
  "score": 94,
  "iterations": 2,
  "pdf_path": "resume/tailored/20260119_143022_Google_Software_Engineer_final.pdf"
}
```

### `tailoring_timeout`
Emitted if orchestrator takes too long (>5 minutes).

```json
{
  "type": "tailoring_timeout",
  "ts": "2026-01-19T14:37:00.000Z",
  "session_id": "session_2026-01-19_01",
  "job_id": "20260119_143022_Google_Software_Engineer",
  "waited_seconds": 300,
  "action_taken": "skip_tailoring"
}
```

### `pending_upload`
Emitted when a tailored resume needs manual upload (external sites).

```json
{
  "type": "pending_upload",
  "ts": "2026-01-19T14:35:00.000Z",
  "session_id": "session_2026-01-19_01",
  "company": "Stripe",
  "job_title": "Product Manager",
  "job_url": "https://stripe.com/jobs/...",
  "pdf_path": "resume/tailored/20260119_143500_Stripe_Product_Manager_final.pdf",
  "score": 91,
  "tab_left_open": true
}
```

---

## Pipeline Session Events

For pipeline mode, `session_start` has additional fields:

```json
{
  "type": "session_start",
  "ts": "2026-01-19T14:30:00.000Z",
  "session_id": "session_2026-01-19_01",
  "session_type": "pipeline",
  "max_applications": 10,
  "orchestrator_status": "ready"
}
```

And `session_end` includes pipeline-specific fields:

```json
{
  "type": "session_end",
  "ts": "2026-01-19T15:45:00.000Z",
  "session_id": "session_2026-01-19_01",
  "session_type": "pipeline",
  "total_applications": 8,
  "tailored_count": 8,
  "avg_ats_score": 91.5,
  "pending_uploads": 2,
  "stop_reason": "limit_reached"
}
```

---

## Orchestrator Events (Python Side)

These are logged to `logs/pipeline/pipeline_YYYY-MM-DD.jsonl`:

### `pipeline_started`
```json
{
  "type": "pipeline_started",
  "timestamp": "2026-01-19T14:30:25.000Z",
  "job_id": "20260119_143022_Google_Software_Engineer",
  "company": "Google",
  "job_title": "Software Engineer"
}
```

### `jd_analyzed`
```json
{
  "type": "jd_analyzed",
  "timestamp": "2026-01-19T14:30:30.000Z",
  "job_id": "20260119_143022_Google_Software_Engineer",
  "keywords_found": 15,
  "required_skills": ["Python", "AWS", "Docker"]
}
```

### `resume_tailored`
```json
{
  "type": "resume_tailored",
  "timestamp": "2026-01-19T14:31:00.000Z",
  "job_id": "20260119_143022_Google_Software_Engineer",
  "iteration": 1
}
```

### `resume_scored`
```json
{
  "type": "resume_scored",
  "timestamp": "2026-01-19T14:31:15.000Z",
  "job_id": "20260119_143022_Google_Software_Engineer",
  "iteration": 1,
  "score": 78,
  "keyword_score": 75,
  "skills_score": 80
}
```

### `pipeline_completed`
```json
{
  "type": "pipeline_completed",
  "timestamp": "2026-01-19T14:32:00.000Z",
  "job_id": "20260119_143022_Google_Software_Engineer",
  "final_score": 94,
  "iterations": 2,
  "pdf_path": "resume/tailored/20260119_143022_Google_Software_Engineer_final.pdf"
}
```

### `compilation_failed`
```json
{
  "type": "compilation_failed",
  "timestamp": "2026-01-19T14:32:00.000Z",
  "job_id": "20260119_143022_Google_Software_Engineer",
  "error": "pdflatex not found..."
}
```

### `pipeline_error`
```json
{
  "type": "pipeline_error",
  "timestamp": "2026-01-19T14:32:00.000Z",
  "job_id": "20260119_143022_Google_Software_Engineer",
  "error": "API rate limit exceeded"
}
```

---

## File Communication Protocol

### Cursor → Orchestrator: `data/pipeline/pending_jd.json`

```json
{
  "company": "Google",
  "job_title": "Software Engineer",
  "location": "Mountain View, CA",
  "job_url": "https://linkedin.com/jobs/view/123456",
  "description": "Full job description text here...",
  "timestamp": "2026-01-19T10:30:00Z"
}
```

### Orchestrator → Cursor: `data/pipeline/resume_ready.json`

```json
{
  "success": true,
  "job_id": "20260119_103000_Google_Software_Engineer",
  "score": 92,
  "pdf_path": "/path/to/resume/tailored/..._final.pdf",
  "tex_path": "/path/to/resume/tailored/..._final.tex",
  "iterations": 2,
  "company": "Google",
  "job_title": "Software Engineer",
  "job_url": "https://linkedin.com/jobs/view/123456"
}
```

### Status: `data/pipeline/orchestrator_status.json`

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

Status values: `ready`, `analyzing`, `tailoring`, `scoring`, `compiling`, `stopped`, `error`

