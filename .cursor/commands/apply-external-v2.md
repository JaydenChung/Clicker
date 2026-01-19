# Apply External Command (v2 — Event-Sourced)

Execute the **FULL APPLICATION WORKFLOW** for non-Easy Apply (external) applications.

> **What's Different in V2**: Instead of signaling multiple agents, you emit events to a file.
> Everything else is EXACTLY THE SAME as V1 — same rules, same accuracy, same behavior.
> Post-session: `python3 scripts/process_session.py` generates all reports.

---

## 🚨 CRITICAL RULES - READ FIRST

### THE CORE PRINCIPLE: AUTONOMOUS OPERATION
This is an **autonomous** job application agent. The user may leave their computer unattended expecting applications to continue. **A stopped session means missed opportunities.**

### RULE #1: NEVER STOP THE SESSION FOR "FIT" REASONS
**The session must NEVER stop because:**
- ❌ Job requires more experience than candidate has
- ❌ Salary seems too high/low
- ❌ Role seems too senior/junior
- ❌ Location isn't ideal
- ❌ Any "this isn't a good match" judgment

**If a suboptimal job is encountered**: Complete the application anyway, log concerns in events, and continue to the next job. Let the human decide what's a good fit - the agent's job is to apply.

### RULE #2: SOFT BLOCKERS → LEAVE TAB, CONTINUE SESSION
When encountering verification requirements:
1. **Leave the tab open** (do NOT close)
2. **Emit `blocker_encountered` event**
3. **Emit `application_completed` event** with status: "pending_manual"
4. **Return to LinkedIn tab**
5. **Continue applying to other jobs**

### RULE #3: EXTERNAL JOBS ONLY - SKIP EASY APPLY
This command is **ONLY** for non-Easy Apply jobs:
- ✅ Apply to jobs that redirect to external company websites
- ❌ SKIP all jobs with "Easy Apply" button
- ❌ NEVER apply to Easy Apply jobs during this session

### RULE #4: LOG EVERY SESSION STOP
Every session stop must be documented in `logs/session_stops.md` AND emit `session_end` event.

---

## ⚡ AGENT ACTIVATION

**PRIMARY AGENTS**: 
- `agents/application_director.md` — Supervises, analyzes pages
- `agents/external_applicant.md` — Executes form fills

**READ BOTH AGENT FILES COMPLETELY BEFORE STARTING.**

---

## Prerequisites
- Browser is open and controlled by Cursor
- LinkedIn is loaded and user is SIGNED IN
- Resume PDF available at `resume/Jayden_APM.pdf` for file uploads

---

## Files to Read FIRST

**ALL of these must be read before starting:**

```
config/personal_profile.md       - Personal info for form filling (REQUIRED)
config/resume_content.md         - Detailed resume for open-ended questions (REQUIRED)
config/projects.md               - Project portfolio for technical questions (REQUIRED)
config/job_preferences.md        - max_applications_per_session
agents/application_director.md   - Director instructions (REQUIRED)
agents/external_applicant.md     - Applicant instructions (REQUIRED)
config/event_schema.md           - Event types reference
```

**⚠️ If you skip reading personal_profile.md, resume_content.md, or projects.md, answers will be wrong!**

---

## Execution Flow

### 1. Initialize Session

1. **Read ALL config files listed above**
2. **Determine session file**: `data/events/session_YYYY-MM-DD_NN.jsonl`
3. **Emit `session_start` event** with session_type: "external"
4. **Log session START to `logs/session_stops.md`** with:
   - Session ID, start timestamp
   - Type: External
   - Max applications planned
5. Confirm resume PDF path is accessible

### 2. For Each Non-Easy Apply Job

**⚠️ JOB SELECTION RULES:**
- ONLY select jobs that do NOT have an "Easy Apply" button
- If a job shows "Easy Apply" → SKIP IT, move to next job
- Look for regular "Apply" button that redirects externally

**Director: Analyze LinkedIn Job Page**
1. Verify job does NOT have "Easy Apply" button
2. Identify company name, job title
3. Click "Apply" button (must redirect to external site)
4. **Emit `application_started` event** with ats_system identified
5. Identify ATS system from URL/page structure

**ATS System Reference:**
| ATS | URL Pattern | Complexity |
|-----|-------------|------------|
| Workday | `*.myworkdayjobs.com` | High (4-7 pages) |
| Greenhouse | `boards.greenhouse.io` | Low (1-2 pages) |
| Lever | `jobs.lever.co` | Low (1 page) |
| Ashby | `jobs.ashbyhq.com` | Low (1-2 pages) |
| Taleo | `*.taleo.net` | High (many pages) |
| iCIMS | `careers-*.icims.com` | Medium |
| Custom | Company domain | Variable |

### 3. Page Processing Loop

**WHILE not on confirmation page:**

**Director: Analyze Page**
1. Take snapshot
2. Identify all form fields
3. Categorize each field (text, dropdown, file upload, textarea)
4. Determine required vs optional

**For EACH Field:**

1. **Director: Determine value from config files:**

| Question Type | Source File | Section |
|--------------|-------------|---------|
| Basic info (name, email, phone) | `personal_profile.md` | Basic Information |
| Years of experience | `personal_profile.md` | Experience Levels |
| Yes/No skills | `personal_profile.md` | Skills - Yes/No Questions |
| Work authorization | `personal_profile.md` | Always "Yes" |
| Sponsorship | `personal_profile.md` | Always "No" |
| Salary | `personal_profile.md` | Salary Expectations |
| Demographics/EEO | `personal_profile.md` | Demographics section |
| "Tell me about yourself" | `resume_content.md` | Professional Summary |
| "Describe an accomplishment" | `resume_content.md` | Key Achievements |
| "Describe experience at X" | `resume_content.md` | Work Experience |
| Behavioral questions | `resume_content.md` | Key Strengths |
| "Why interested in this role" | `personal_profile.md` | Additional Questions |
| Technical project questions | `projects.md` | Featured Projects |
| "Describe a project" | `projects.md` | Use High-Note or relevant project |

2. **Emit `question_encountered` event** with:
   - question_text, answer_given, answer_source
   - is_open_ended: true/false

3. **Applicant: Fill the field**

4. **If OPEN-ENDED question:**
   - Generate 2-3 sentence response using profile/resume data
   - Emit event with the generated response

**After all fields: Click Next/Continue/Submit**

**Check for blockers:**

---

## Blocker Categories

### ⏸️ SOFT BLOCKERS (Leave Tab Open, Continue Session)

| Blocker | Action |
|---------|--------|
| Email verification code | Emit event, leave tab open, continue |
| Phone verification | Emit event, leave tab open, continue |
| Account creation email | Emit event, leave tab open, continue |
| MFA/2FA required | Emit event, leave tab open, continue |

**On Soft Blocker:**
1. **Emit `blocker_encountered` event** with blocker_type: "soft"
2. **Emit `application_completed` event** with status: "pending_manual"
3. DO NOT close the tab
4. Switch back to LinkedIn
5. Find next EXTERNAL job (SKIP Easy Apply)
6. Continue session

### 🛑 HARD BLOCKERS (Skip Application, Continue Session)

| Blocker | Action |
|---------|--------|
| CAPTCHA/reCAPTCHA | Emit event, skip, continue |
| Mandatory assessment | Emit event, skip, continue |
| Video interview required | Emit event, skip, continue |
| Broken form | Emit event, skip, continue |

**On Hard Blocker:**
1. **Emit `blocker_encountered` event** with blocker_type: "hard"
2. **Emit `application_completed` event** with status: "skipped"
3. Navigate back to LinkedIn
4. Continue with next external job

### ⚠️ NOT BLOCKERS (Continue Application)

| Issue | Action |
|-------|--------|
| High experience requirements | Continue, note in event |
| Salary mismatch | Continue, note in event |
| Senior-level role | Continue, note in event |
| Missing optional fields | Skip field, continue |

---

### 4. On Confirmation Page

1. Detect confirmation message/page
2. **Emit `application_completed` event** with:
   - status: "applied"
   - ats_system: detected system
   - duration_ms: total time

### 5. Return to LinkedIn

Navigate back to LinkedIn to find next EXTERNAL job:
- SKIP all jobs with "Easy Apply"
- Only click "Apply" on jobs that redirect externally
- If no more external jobs → end session

---

## Session End

### Triggers
- All external applications done
- No more external jobs found
- Only Easy Apply jobs remaining
- `max_applications_per_session` reached
- 3+ consecutive failures

### On End:
1. **Emit `session_end` event** with:
   - total_applications
   - stop_reason: "completed" / "no_more_external" / "limit_reached" / "error_threshold"
2. Log session END to `logs/session_stops.md` with full summary
3. Tell user: **"Session complete. Run `python3 scripts/process_session.py` to generate reports."**

---

## Event Types for External

| When | Event | Key Fields |
|------|-------|------------|
| Session begins | `session_start` | session_type: "external" |
| Click Apply (external) | `application_started` | ats_system, job_url |
| Each form field | `question_encountered` | is_open_ended, answer_source |
| Hit blocker | `blocker_encountered` | blocker_type, blocker_reason |
| App complete/blocked | `application_completed` | status, ats_system |
| Session ends | `session_end` | stop_reason |

---

## Files Updated

| During Session | After Session (by script) |
|----------------|---------------------------|
| `data/events/session_*.jsonl` | `data/applications.csv` |
| `logs/session_stops.md` | `logs/questions/all_questions.md` |
| | `logs/performance/session_*_summary.md` |

---

## Critical Rules (Priority Order)

1. **🏆 COMPLETE APPLICATIONS NO MATTER WHAT** — Experience mismatches, salary, location are NOT reasons to stop
2. **📖 READ ALL CONFIG FILES** — personal_profile.md, resume_content.md, AND projects.md
3. **📝 EMIT ALL EVENTS** — Every action should have an event
4. **⏸️ SOFT BLOCKERS: LEAVE TAB OPEN** — Don't close tabs with pending verifications
5. **🔄 DIRECTOR SUPERVISES, APPLICANT EXECUTES** — Clear separation of concerns
6. **📋 USE CORRECT ANSWERS** — Match question type to the right source file
7. **📍 LOG SESSION STOPS** — Update logs/session_stops.md for human visibility

---

## Post-Session

After session ends, run:
```bash
python3 scripts/process_session.py
```

This generates all the same outputs V1 created:
- CSV entries (with status: Applied, Pending Manual, Skipped)
- Question logs (including open-ended responses)
- Session summary

---

## V1 vs V2 Comparison

| Aspect | V1 | V2 |
|--------|----|----|
| Config files read | ✅ All | ✅ All (SAME) |
| Rules followed | ✅ All | ✅ All (SAME) |
| Question answering | ✅ Accurate | ✅ Accurate (SAME) |
| Blocker handling | ✅ Same rules | ✅ Same rules |
| Tracking method | Signal agents | Emit events |
| When logs generated | During session | After session |

**V2 does everything V1 does. It just logs differently.**
