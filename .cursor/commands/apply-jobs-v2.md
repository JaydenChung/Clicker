# Apply to Jobs Command (v2 — Event-Sourced)

Execute the **FULL APPLICATION WORKFLOW** for Easy Apply applications.

> **What's Different in V2**: Instead of signaling multiple agents, you emit events to a file.
> Everything else is EXACTLY THE SAME as V1 — same rules, same accuracy, same behavior.
> Post-session: `python3 scripts/process_session.py` generates all reports.

---

## ⚡ AGENT ACTIVATION

**PRIMARY AGENT**: `agents/job_applicant_v2.md`

**READ THE AGENT FILE COMPLETELY BEFORE STARTING.**

---

## Prerequisites
- Browser is open and controlled by Cursor
- LinkedIn is loaded and user is SIGNED IN
- Search plan exists at `data/current_search_plan.md` (run `/plan-search` first if needed)

---

## Files to Read FIRST

**ALL of these must be read before starting:**

```
config/personal_profile.md      - Personal info for form filling (REQUIRED)
config/resume_content.md        - Detailed resume data for questions (REQUIRED)
config/job_preferences.md       - Job preferences + max_applications_per_session
data/current_search_plan.md     - Search strategy (REQUIRED)
agents/job_applicant_v2.md      - Agent instructions (REQUIRED)
config/event_schema.md          - Event types reference
```

**⚠️ If you skip reading personal_profile.md or resume_content.md, answers will be wrong!**

---

## Execution Flow

### 1. Initialize Session

1. **Read ALL config files listed above**
2. **Determine session file name:**
   - Check `data/events/` for existing files today
   - Create: `data/events/session_YYYY-MM-DD_NN.jsonl` (NN = next number)
3. **Emit `session_start` event**
4. **Log session start** to `logs/session_stops.md` with:
   - Session ID (format: `session_YYYY-MM-DD_NN`)
   - Start timestamp
   - Session type: Easy Apply
   - Max applications from config
5. Navigate to LinkedIn Jobs if not there

### 2. For Each Search in Plan

1. Get next search from `data/current_search_plan.md`
2. Mark search as "in_progress" in plan
3. Enter keyword and location in LinkedIn search
4. **APPLY EXPERIENCE LEVEL FILTERS** (Critical!):
   - Click "Experience level" filter or "All filters"
   - Select: ✅ Internship, ✅ Entry level, ✅ Associate
   - Do NOT select Mid-Senior, Director, or Executive
   - Click "Show results"
5. **Emit `search_started` event**
6. Process jobs in results

### 3. For Each Job in Results

**Check if should apply:**
- ✅ Has "Easy Apply" button
- ✅ Does NOT show "Applied" badge
- ✅ Not in "Companies to Avoid" list

**If applying:**
1. Click on job listing
2. **Emit `application_started` event** with all job details
3. Click "Easy Apply" button
4. Fill form (see Form Handling below)
5. Submit application
6. Click "Done"
7. **Emit `application_completed` event**
8. Immediately proceed to next job

### 4. Form Handling (CRITICAL FOR ACCURACY)

#### Contact Information Step
- Should be pre-filled from LinkedIn
- Verify email matches `config/personal_profile.md`
- Click "Next"

#### Resume Step
- Select resume file from `config/personal_profile.md` → Resume section
- Click "Next"

#### Additional Questions Step
**Reference BOTH files for answers:**
- `config/personal_profile.md` — Years of experience, Yes/No questions, salary
- `config/resume_content.md` — Detailed answers for open-ended questions

| Question Type | Where to Find Answer |
|--------------|---------------------|
| Years of experience | `personal_profile.md` → Experience Levels |
| Yes/No skills | `personal_profile.md` → Skills - Yes/No Questions |
| Work authorization | Always "Yes" |
| Sponsorship | Always "No" |
| Salary | `personal_profile.md` → Salary Expectations |
| "Tell me about yourself" | `resume_content.md` → Professional Summary |
| "Describe accomplishment" | `resume_content.md` → Key Achievements |
| Behavioral questions | `resume_content.md` → Key Strengths |

**For each question encountered: Emit `question_encountered` event**

#### Review Step
- Verify information looks correct
- Click "Submit application"

#### Completion
- Click "Done" to close dialog

### 5. Session End

**Triggers:**
- `max_applications_per_session` reached
- Search plan exhausted
- 5+ consecutive errors

**On End:**
1. **Emit `session_end` event**
2. Log session END to `logs/session_stops.md` with:
   - End timestamp
   - Stop reason
   - Total applications
3. Tell user: **"Session complete. Run `python3 scripts/process_session.py` to generate reports."**

---

## Decision Rules (Same as V1)

### APPLY if:
- Job has "Easy Apply" button
- Job does NOT show "Applied" badge
- Job title contains keywords from preferences
- Location matches or is Remote

### SKIP if:
- No "Easy Apply" (external application required)
- Already applied
- Company is in "Companies to Avoid" list

---

## Error Handling (Same as V1)

| Error | Action |
|-------|--------|
| Dialog fails to open | Wait 3 seconds, retry once |
| Form field errors | Emit `error_occurred` event, try to continue |
| Page unresponsive | Emit `error_occurred` event, refresh and continue |
| Rate limited | Emit `error_occurred` event, wait 30 seconds, continue |

---

## Event Emission Quick Reference

| When | Event Type |
|------|------------|
| Session begins | `session_start` |
| New search query | `search_started` |
| Click Easy Apply | `application_started` |
| Each form question | `question_encountered` |
| After submit | `application_completed` |
| On error | `error_occurred` |
| Search done | `search_completed` |
| Session ends | `session_end` |

---

## Files Updated

| During Session | After Session (by script) |
|----------------|---------------------------|
| `data/events/session_*.jsonl` | `data/applications.csv` |
| `logs/session_stops.md` | `logs/questions/all_questions.md` |
| `data/current_search_plan.md` (progress) | `logs/performance/session_*_summary.md` |

---

## Critical Rules (Same as V1)

1. **READ ALL CONFIG FILES** — personal_profile.md AND resume_content.md
2. **APPLY EXPERIENCE FILTERS** — Every new search
3. **COMPLETE APPLICATIONS** — Never stop mid-application
4. **LOG EVERYTHING** — Emit events for all actions
5. **USE CORRECT ANSWERS** — Reference the right file for each question type
6. **UPDATE SESSION_STOPS.MD** — For human visibility

---

## Post-Session

After session ends, run:
```bash
python3 scripts/process_session.py
```

This generates all the same outputs V1 created:
- CSV entries
- Question logs
- Performance summaries

---

## V1 vs V2 Comparison

| Aspect | V1 | V2 |
|--------|----|----|
| Config files read | ✅ All | ✅ All (SAME) |
| Rules followed | ✅ All | ✅ All (SAME) |
| Question answering | ✅ Accurate | ✅ Accurate (SAME) |
| Tracking method | Signal agents | Emit events |
| When logs generated | During session | After session |
| Speed | Slower (7 steps after each app) | Faster (1 step after each app) |

**V2 does everything V1 does. It just logs differently.**
