# Event Schema

> **Purpose**: Defines the structure of events emitted by the main agent during job application sessions.  
> **Format**: JSON Lines (one JSON object per line)  
> **Location**: `data/events/session_YYYY-MM-DD_N.jsonl`

---

## Core Principles

1. **Every event has**: `type`, `ts` (ISO timestamp), `session_id`
2. **Append-only**: Events are only added, never modified
3. **Self-contained**: Each event has all context needed to process it
4. **Minimal**: Main agent does minimal work — just emit and continue

---

## Event Types

### Session Events

#### `session_start`
Emitted once at the beginning of each session.

```json
{
  "type": "session_start",
  "ts": "2026-01-19T14:30:00.000Z",
  "session_id": "session_2026-01-19_01",
  "session_type": "easy_apply",
  "max_applications": 10
}
```

#### `session_end`
Emitted once at the end of each session.

```json
{
  "type": "session_end",
  "ts": "2026-01-19T15:45:00.000Z",
  "session_id": "session_2026-01-19_01",
  "total_applications": 12,
  "stop_reason": "limit_reached"
}
```

| `stop_reason` values |
|---------------------|
| `limit_reached` |
| `plan_exhausted` |
| `error_threshold` |
| `user_interrupt` |

---

### Search Events

#### `search_started`
Emitted when a new keyword+location search begins.

```json
{
  "type": "search_started",
  "ts": "2026-01-19T14:30:05.000Z",
  "session_id": "session_2026-01-19_01",
  "keyword": "Product Manager",
  "location": "Remote",
  "filters_applied": ["Internship", "Entry level", "Associate"]
}
```

#### `search_completed`
Emitted when done processing a search's results.

```json
{
  "type": "search_completed",
  "ts": "2026-01-19T14:45:00.000Z",
  "session_id": "session_2026-01-19_01",
  "keyword": "Product Manager",
  "location": "Remote",
  "jobs_found": 25,
  "jobs_applied": 8,
  "jobs_skipped": 17
}
```

---

### Application Events

#### `application_started`
Emitted when clicking Easy Apply on a job.

```json
{
  "type": "application_started",
  "ts": "2026-01-19T14:30:22.000Z",
  "session_id": "session_2026-01-19_01",
  "company": "Acme Corp",
  "job_title": "Product Manager",
  "location": "San Francisco, CA",
  "work_type": "Hybrid",
  "job_url": "https://linkedin.com/jobs/view/123456789",
  "salary_listed": "$120k-$150k",
  "applicant_count": "87 applicants"
}
```

#### `step_started`
Emitted when entering a new step in the application form.

```json
{
  "type": "step_started",
  "ts": "2026-01-19T14:30:25.000Z",
  "session_id": "session_2026-01-19_01",
  "step_number": 1,
  "step_name": "contact_info"
}
```

| `step_name` values |
|-------------------|
| `contact_info` |
| `resume` |
| `additional_questions` |
| `review` |
| `submit` |

#### `step_completed`
Emitted when a step is finished.

```json
{
  "type": "step_completed",
  "ts": "2026-01-19T14:30:31.000Z",
  "session_id": "session_2026-01-19_01",
  "step_number": 1,
  "step_name": "contact_info",
  "duration_ms": 6000
}
```

#### `question_encountered`
Emitted for each form question answered.

```json
{
  "type": "question_encountered",
  "ts": "2026-01-19T14:30:35.000Z",
  "session_id": "session_2026-01-19_01",
  "question_text": "How many years of experience do you have with Python?",
  "question_type": "numeric",
  "answer_given": "3",
  "answer_source": "profile",
  "was_required": true
}
```

| `answer_source` values |
|-----------------------|
| `profile` — Found in personal_profile.md |
| `default` — Used a safe default |
| `generated` — LLM generated answer |
| `skipped` — Optional question left blank |

#### `application_completed`
Emitted when application is submitted (or blocked).

```json
{
  "type": "application_completed",
  "ts": "2026-01-19T14:31:02.000Z",
  "session_id": "session_2026-01-19_01",
  "company": "Acme Corp",
  "job_title": "Product Manager",
  "status": "applied",
  "total_steps": 4,
  "total_questions": 5,
  "questions_from_profile": 4,
  "questions_unanswered": 1,
  "duration_ms": 40000
}
```

| `status` values |
|----------------|
| `applied` — Successfully submitted |
| `skipped` — Hard blocker (CAPTCHA, assessment) |
| `pending_manual` — Soft blocker (verification needed) |
| `error` — Technical failure |

---

### Error Events

#### `error_occurred`
Emitted when something goes wrong.

```json
{
  "type": "error_occurred",
  "ts": "2026-01-19T14:35:00.000Z",
  "session_id": "session_2026-01-19_01",
  "error_type": "element_not_found",
  "error_message": "Could not find Easy Apply button",
  "context": "application_started",
  "company": "TechStart Inc",
  "recoverable": true
}
```

#### `blocker_encountered`
Emitted when hitting a hard or soft blocker.

```json
{
  "type": "blocker_encountered",
  "ts": "2026-01-19T14:40:00.000Z",
  "session_id": "session_2026-01-19_01",
  "blocker_type": "soft",
  "blocker_reason": "email_verification",
  "company": "DataCorp",
  "action_taken": "left_tab_open"
}
```

| `blocker_type` | `blocker_reason` values |
|---------------|------------------------|
| `soft` | `email_verification`, `phone_verification`, `account_confirmation` |
| `hard` | `captcha`, `assessment_required`, `video_interview` |

---

## File Naming Convention

```
data/events/session_YYYY-MM-DD_NN.jsonl

Examples:
data/events/session_2026-01-19_01.jsonl  (first session of the day)
data/events/session_2026-01-19_02.jsonl  (second session of the day)
```

---

## Processing Notes

The `scripts/process_session.py` script will:

1. Read all events from a session file
2. Reconstruct application records from start→complete pairs
3. Handle orphaned events (started but not completed)
4. Generate:
   - CSV row for each application
   - Question log entries
   - Performance metrics
   - Session summary

---

## Example Complete Session

```json
{"type":"session_start","ts":"2026-01-19T14:30:00.000Z","session_id":"session_2026-01-19_01","session_type":"easy_apply","max_applications":10}
{"type":"search_started","ts":"2026-01-19T14:30:05.000Z","session_id":"session_2026-01-19_01","keyword":"Product Manager","location":"Remote","filters_applied":["Entry level"]}
{"type":"application_started","ts":"2026-01-19T14:30:22.000Z","session_id":"session_2026-01-19_01","company":"Acme Corp","job_title":"PM","location":"Remote","work_type":"Remote","job_url":"https://linkedin.com/jobs/view/123","salary_listed":"","applicant_count":"50 applicants"}
{"type":"step_started","ts":"2026-01-19T14:30:23.000Z","session_id":"session_2026-01-19_01","step_number":1,"step_name":"contact_info"}
{"type":"step_completed","ts":"2026-01-19T14:30:28.000Z","session_id":"session_2026-01-19_01","step_number":1,"step_name":"contact_info","duration_ms":5000}
{"type":"step_started","ts":"2026-01-19T14:30:29.000Z","session_id":"session_2026-01-19_01","step_number":2,"step_name":"resume"}
{"type":"step_completed","ts":"2026-01-19T14:30:35.000Z","session_id":"session_2026-01-19_01","step_number":2,"step_name":"resume","duration_ms":6000}
{"type":"step_started","ts":"2026-01-19T14:30:36.000Z","session_id":"session_2026-01-19_01","step_number":3,"step_name":"additional_questions"}
{"type":"question_encountered","ts":"2026-01-19T14:30:40.000Z","session_id":"session_2026-01-19_01","question_text":"Years of PM experience?","question_type":"numeric","answer_given":"2","answer_source":"profile","was_required":true}
{"type":"step_completed","ts":"2026-01-19T14:30:50.000Z","session_id":"session_2026-01-19_01","step_number":3,"step_name":"additional_questions","duration_ms":14000}
{"type":"step_started","ts":"2026-01-19T14:30:51.000Z","session_id":"session_2026-01-19_01","step_number":4,"step_name":"review"}
{"type":"step_completed","ts":"2026-01-19T14:30:55.000Z","session_id":"session_2026-01-19_01","step_number":4,"step_name":"review","duration_ms":4000}
{"type":"application_completed","ts":"2026-01-19T14:31:02.000Z","session_id":"session_2026-01-19_01","company":"Acme Corp","job_title":"PM","status":"applied","total_steps":4,"total_questions":1,"questions_from_profile":1,"questions_unanswered":0,"duration_ms":40000}
{"type":"search_completed","ts":"2026-01-19T14:45:00.000Z","session_id":"session_2026-01-19_01","keyword":"Product Manager","location":"Remote","jobs_found":10,"jobs_applied":5,"jobs_skipped":5}
{"type":"session_end","ts":"2026-01-19T14:50:00.000Z","session_id":"session_2026-01-19_01","total_applications":5,"stop_reason":"limit_reached"}
```
