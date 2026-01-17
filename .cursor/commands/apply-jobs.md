# Apply to Jobs Command

Execute the **FULL AGENT ORCHESTRA** for Easy Apply applications.

---

## ⚡ AGENTS TO ACTIVATE

You MUST activate and follow ALL of these agents simultaneously:

1. **Job Applicant** (`agents/job_applicant.md`) - Primary executor
2. **Performance Monitor** (`agents/performance_monitor.md`) - Track timing for EVERY step
3. **Question Tracker** (`agents/question_tracker.md`) - Log ALL questions encountered
4. **CSV Tracker** (`agents/csv_tracker.md`) - Update CSV after each application
5. **Application Tracker** (`agents/application_tracker.md`) - Create detailed MD logs
6. **Search Logger** (`agents/search_logger.md`) - Track search progress

**READ ALL AGENT FILES BEFORE STARTING.**

---

## Prerequisites
- Browser is open and controlled by Cursor
- LinkedIn is loaded and user is SIGNED IN
- Search plan exists at `data/current_search_plan.md` (run `/plan-search` first if needed)

---

## Files to Read FIRST

```
config/personal_profile.md    - Personal info for form filling
config/resume_content.md      - Resume data for questions  
config/job_preferences.md     - Job preferences
data/current_search_plan.md   - Search strategy
agents/job_applicant.md       - Job applicant instructions
agents/performance_monitor.md - Performance tracking instructions
agents/question_tracker.md    - Question tracking instructions
agents/csv_tracker.md         - CSV tracking instructions
agents/application_tracker.md - Application logging instructions
agents/search_logger.md       - Search logging instructions
```

---

## Execution Flow

### 1. Initialize Session
- Create session log in `logs/sessions/session_YYYY-MM-DD_HH-MM.md`
- Initialize performance tracking file `logs/performance/current_session.md`
- Load search plan from `data/current_search_plan.md`

### 2. For Each Search in Plan

#### Search Execution
1. Enter keyword in job search box
2. Enter location
3. Execute search
4. Log search start to session log

#### For Each "Easy Apply" Job (skip jobs with "Applied" badge)

**START TIMERS (Performance Monitor)**
```
- application_start_time = now()
- current_step = 0
```

**A. Open Job**
1. Click on job listing
2. Record: `step_1_start = now()`
3. Click "Easy Apply" button
4. Record: `step_1_time = now() - step_1_start`

**B. Fill Each Form Step**

For EACH step/page in the application:
```
step_start = now()
current_step += 1
```

For EACH field on the page:
```
field_start = now()
```

1. **Identify the question/field**
2. **Log to Question Tracker:**
   - Question text (exact wording)
   - Field type (text, dropdown, radio, checkbox)
   - Required or optional?
   - Company name
   
3. **Find answer in personal_profile.md**
   - If FOUND: Use the answer, log as "from_profile"
   - If NOT FOUND: 
     - Try to infer from similar questions
     - Log as "guessed" or "skipped"
     - Add to `logs/questions/unanswered.md` with HIGH PRIORITY

4. **Fill the field**
   ```
   field_time = now() - field_start
   Log: {question, answer, source, time_ms}
   ```

5. **Check for stuck state (Performance Monitor)**
   - If field_time > 30 seconds → Log to `logs/performance/stuck_log.md`

After all fields on page:
```
step_time = now() - step_start
Log step to performance current_session.md
```

Click "Next" or "Review" or "Submit"

**C. Submit Application**
1. On final review screen, click "Submit application"
2. Wait for confirmation
3. Click "Done"
4. Record: `total_application_time = now() - application_start_time`

**D. Log to ALL Trackers**

**CSV Tracker** - Append row to `data/applications.csv`:
```csv
application_id,date_applied,time_applied,company,job_title,location,work_type,job_url,status,salary_listed,applicant_count,search_keyword,search_location,session_id,questions_count,questions_unanswered,time_to_apply_seconds,steps_count,notes
```

**Application Tracker** - Create `logs/applications/YYYY-MM-DD_company_title.md`:
- Job details
- All questions and answers
- Timing breakdown
- Any issues encountered

**Performance Monitor** - Update `logs/performance/current_session.md`:
- Application timing table
- Step-by-step breakdown
- Any stuck events

**Question Tracker** - Update:
- `logs/questions/all_questions.md` - All questions seen
- `logs/questions/unanswered.md` - Questions without profile answers
- `logs/questions/patterns.md` - Question patterns

### 3. Session End

Triggers:
- Context usage exceeds 80%
- Search plan exhausted
- Rate limit detected
- User interrupts

**On End, Generate Summaries:**

**Session Log Summary:**
```
📊 SESSION COMPLETE
━━━━━━━━━━━━━━━━━━
Applications: X submitted
Searches: Y completed
Duration: Z minutes
```

**Performance Summary:**
```
📊 PERFORMANCE SUMMARY
━━━━━━━━━━━━━━━━━━━━━━
Average time per application: XX seconds
Fastest: XXs (Company)
Slowest: XXs (Company)
Stuck events: X
```

**Question Summary:**
```
📋 QUESTION TRACKER SUMMARY
━━━━━━━━━━━━━━━━━━━━━━━━━━
Questions Encountered: XX
From Profile: XX (XX%)
Guessed: XX (XX%)
Skipped: XX (XX%)

⚠️ NEW UNANSWERED QUESTIONS:
1. [question] - guessed "[answer]"
2. [question] - skipped

Please update config/personal_profile.md!
```

---

## Files to Update (EVERY application)

| File | What to Update |
|------|----------------|
| `data/applications.csv` | Add new row |
| `logs/sessions/session_*.md` | Add application entry |
| `logs/applications/*.md` | Create detailed record |
| `logs/performance/current_session.md` | Add timing data |
| `logs/questions/all_questions.md` | Add all questions |
| `logs/questions/unanswered.md` | Add unknown questions |
| `logs/questions/patterns.md` | Update patterns |

---

## Critical Rules

1. **TRACK TIME FOR EVERY STEP** - Not just total time
2. **LOG EVERY QUESTION** - Even if we have the answer
3. **UPDATE CSV IMMEDIATELY** - After each application, not at end
4. **DETECT STUCK STATES** - Log if any step > 30 seconds
5. **COMPLETE APPLICATIONS** - Don't end session mid-application
