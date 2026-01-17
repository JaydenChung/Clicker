# Apply External Command

Execute the **FULL AGENT ORCHESTRA** for non-Easy Apply (external) applications.

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

**If a suboptimal job is encountered**: Complete the application anyway, log concerns in notes, and continue to the next job. Let the human decide what's a good fit - the agent's job is to apply.

### RULE #2: SOFT BLOCKERS → LEAVE TAB, CONTINUE SESSION
When encountering verification requirements:
1. **Leave the tab open** (do NOT close)
2. **Log the blocker** in `logs/session_stops.md`
3. **Return to LinkedIn tab**
4. **Continue applying to other jobs**
5. User will manually complete blocked applications later

### RULE #3: EXTERNAL JOBS ONLY - SKIP EASY APPLY
This command is **ONLY** for non-Easy Apply jobs:
- ✅ Apply to jobs that redirect to external company websites
- ❌ SKIP all jobs with "Easy Apply" button
- ❌ NEVER apply to Easy Apply jobs during this session

**If a job shows "Easy Apply"**: Skip it and move to the next job. Easy Apply jobs are handled by the `/apply-jobs` command, not this one.

### RULE #4: LOG EVERY SESSION STOP
Every session stop must be documented in `logs/session_stops.md`:
- Blockers (soft and hard)
- Errors
- User interrupts
- Successful completion
- No more external jobs available

**If you don't log why the session stopped, the user has no way to debug or improve the system.**

---

## ⚡ AGENTS TO ACTIVATE

You MUST activate and follow ALL of these agents simultaneously:

1. **Application Director** (`agents/application_director.md`) - Supervisor for external apps
2. **External Applicant** (`agents/external_applicant.md`) - Executor for external apps
3. **Performance Monitor** (`agents/performance_monitor.md`) - Track timing for EVERY step
4. **Question Tracker** (`agents/question_tracker.md`) - Log ALL questions (especially open-ended)
5. **CSV Tracker** (`agents/csv_tracker.md`) - Update CSV after each application
6. **Application Tracker** (`agents/application_tracker.md`) - Create detailed MD logs

**READ ALL AGENT FILES BEFORE STARTING.**

---

## Prerequisites
- Browser is open and controlled by Cursor
- LinkedIn is loaded and user is SIGNED IN
- Resume PDF available at `resume/Jayden_APM.pdf` for file uploads

---

## Files to Read FIRST

```
config/personal_profile.md       - Personal info for form filling
config/resume_content.md         - Resume data for open-ended questions
config/projects.md               - Project portfolio for technical questions
agents/application_director.md   - Director (supervisor) instructions
agents/external_applicant.md     - Applicant (executor) instructions
agents/performance_monitor.md    - Performance tracking instructions
agents/question_tracker.md       - Question tracking instructions
agents/csv_tracker.md            - CSV tracking instructions
agents/application_tracker.md    - Application logging instructions
```

---

## Execution Flow

### 1. Initialize
- Load all config files
- Read `max_applications_per_session` from `/config/job_preferences.md`
- **Log session START** to `logs/session_stops.md` with:
  - Session ID, start timestamp
  - Type: External
  - Max applications planned
- Create session folder: `logs/applications/session_{id}_external/`
- Create session log in `logs/sessions/`
- Initialize performance tracking
- Confirm resume PDF path

### 2. For Each Non-Easy Apply Job

**⚠️ JOB SELECTION RULES:**
- ONLY select jobs that do NOT have an "Easy Apply" button
- If a job shows "Easy Apply" → SKIP IT, move to next job
- Look for regular "Apply" button that redirects externally
- If no more external jobs found → End session

**Director: Analyze LinkedIn Job Page**
1. Verify job does NOT have "Easy Apply" button (if it does, SKIP)
2. Identify company name, job title
3. Click "Apply" button (must redirect to external site)
4. Handle redirect to external site
5. Identify ATS system from URL/page structure

**ATS System Reference:**
| ATS | URL Pattern | Complexity |
|-----|-------------|------------|
| Workday | `*.myworkdayjobs.com` | High (4-7 pages) |
| Greenhouse | `boards.greenhouse.io` | Low (1-2 pages) |
| Lever | `jobs.lever.co` | Low (1 page) |
| Taleo | `*.taleo.net` | High (many pages) |
| iCIMS | `careers-*.icims.com` | Medium |
| Custom | Company domain | Variable |

### 3. Page Processing Loop

**START TIMERS (Performance Monitor)**
```
external_app_start = now()
page_count = 0
```

**WHILE not on confirmation page:**

```
page_start = now()
page_count += 1
```

**Director: Analyze Page**
1. Take snapshot
2. Identify all form fields
3. Categorize each field (text, dropdown, file upload, etc.)
4. Determine required vs optional

**For EACH Field:**

```
field_start = now()
```

1. **Director: Determine value**
   - Check `personal_profile.md`
   - Check `resume_content.md` for detailed questions
   - Check `projects.md` for technical questions
   
2. **Question Tracker: Log the question**
   ```
   {
     question: "[exact text]",
     field_type: "text|dropdown|textarea|file|checkbox",
     required: true|false,
     company: "[company]",
     ats_system: "[workday|greenhouse|etc]",
     is_open_ended: true|false
   }
   ```

3. **If OPEN-ENDED question:**
   - Director generates response using profile data
   - Response should be 2-3 sentences
   - Log to Question Tracker with `is_open_ended: true`
   - Include the generated response in the log
   
4. **Applicant: Fill the field**
   - Execute the fill action
   - Report success/failure
   
5. **Log timing:**
   ```
   field_time = now() - field_start
   If field_time > 30s → Log stuck event
   ```

**After all fields:**
```
page_time = now() - page_start
Log page to performance tracker
```

**Click Next/Continue/Submit**

**Check for blockers (see Blocker Categories):**

---

## Blocker Categories

### ⏸️ SOFT BLOCKERS (Leave Tab Open, Continue Session)
These blockers require human intervention but should NOT stop the session:

| Blocker | Action | Log Entry |
|---------|--------|-----------|
| **Email verification code** | Leave tab open, continue session | Log in session_stops.md |
| **Phone verification** | Leave tab open, continue session | Log in session_stops.md |
| **Account creation email confirmation** | Leave tab open, continue session | Log in session_stops.md |
| **MFA/2FA required** | Leave tab open, continue session | Log in session_stops.md |
| **"Check your email" pages** | Leave tab open, continue session | Log in session_stops.md |

**On Soft Blocker:**
```
1. Log application attempt in logs/applications/session_{session_id}_external/[date]_[company]_[role].md
2. Add entry to logs/session_stops.md
3. DO NOT close the tab
4. Switch back to LinkedIn tab
5. Find next NON-Easy Apply job (SKIP any Easy Apply jobs)
6. Continue with next EXTERNAL application only
```

**⚠️ IMPORTANT**: After returning to LinkedIn, you MUST:
- Look for jobs WITHOUT the "Easy Apply" button
- SKIP all jobs that show "Easy Apply" - these are for the `/apply-jobs` command
- Only click "Apply" on jobs that redirect to external sites
- If no more external jobs are found, end the session

### 🛑 HARD BLOCKERS (Skip Application, Continue Session)
These blockers make the application impossible to complete:

| Blocker | Action | Log Entry |
|---------|--------|-----------|
| **CAPTCHA/reCAPTCHA interactive** | Skip application | Log in session_stops.md |
| **Mandatory assessment/test** | Skip application | Log in session_stops.md |
| **Video interview required to apply** | Skip application | Log in session_stops.md |
| **Security questions we can't answer** | Skip application | Log in session_stops.md |
| **Broken/non-functional form** | Skip application | Log in session_stops.md |

**On Hard Blocker:**
```
1. Log blocker in logs/session_stops.md
2. Close the tab OR navigate back to LinkedIn
3. Find next NON-Easy Apply job (SKIP any Easy Apply jobs)
4. Continue with next EXTERNAL application only
```

### ⚠️ NOT BLOCKERS (Continue Application)
These are NOT reasons to stop. Log for reference but keep applying:

| Issue | Action | Log Entry |
|-------|--------|-----------|
| **High experience requirements** | Continue application | Note in application log |
| **Salary mismatch** | Continue application | Note in application log |
| **Senior-level role** | Continue application | Note in application log |
| **Missing optional fields** | Continue application | Skip optional fields |
| **Location mismatch** | Continue application | Note in application log |

---

### 4. On Confirmation Page

1. Detect confirmation message/page
2. Record: `total_time = now() - external_app_start`
3. Take screenshot for verification

### 5. Log to ALL Trackers

**CSV Tracker** - Append row with:
- `work_type`: "External"
- `ats_system`: Detected ATS
- `time_to_apply_seconds`: Total time
- `steps_count`: Number of pages

**Application Tracker** - Create detailed MD log:
- All questions and answers
- Open-ended responses generated
- Page-by-page breakdown
- Any blockers encountered

**Question Tracker** - Update:
- All questions (especially open-ended)
- Unanswered questions
- ATS-specific patterns

**Performance Monitor** - Update:
- External app timing (separate from Easy Apply)
- Page-by-page timing
- Stuck events

### 6. Return to LinkedIn

Navigate back to LinkedIn to find the next **EXTERNAL** job:

```
1. Switch to LinkedIn tab
2. Scroll through job listings
3. FOR each job in list:
   - IF job has "Easy Apply" button → SKIP (do not click)
   - IF job has regular "Apply" button → SELECT for external application
4. IF no more external jobs found:
   - Log "No more external jobs available" in session_stops.md
   - End session
5. ELSE: Continue with next external application
```

**⚠️ NEVER apply to Easy Apply jobs during an external session.**

---

## Session End

### Session End Triggers (ALWAYS LOG THE REASON)

| Trigger | Category | Action |
|---------|----------|--------|
| All external applications done | ✅ COMPLETED | Log success |
| No more external jobs found | ✅ COMPLETED | Log "no more external jobs in results" |
| Only Easy Apply jobs remaining | ✅ COMPLETED | Log "only Easy Apply jobs remaining - use /apply-jobs" |
| `max_applications_per_session` reached | ✅ COMPLETED | Log limit reached |
| Browser disconnected | ⚠️ SYSTEM LIMIT | Log error |
| 3+ consecutive failures | ⚠️ SYSTEM LIMIT | Log errors, pause |
| User interrupts | 🚫 USER INTERRUPT | Log current state |

### MANDATORY: Log Session Stop

**Every session end MUST update `logs/session_stops.md` with:**

```markdown
### [DATE] - Session [#] ([Type])

| Time | Company | Job Title | Stop Type | Reason | Tab Left Open | Resume Action |
|------|---------|-----------|-----------|--------|---------------|---------------|
| HH:MM | [Company] | [Title] | [Type] | [Reason] | ✅/❌ | [Action] |

**Session Status**: [COMPLETED/PAUSED/ENDED]
**Applications Attempted**: X
**Applications Completed**: X
**Applications Pending Manual**: X

**Notes**:
- [Context]
```

### Generate Summaries

```
📊 EXTERNAL APPLICATION SESSION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Session End Reason: [REASON]

Applications Attempted: X
Successfully Completed: X
Pending Manual Completion: X
Blocked/Skipped: X

By ATS:
  Workday: X
  Greenhouse: X
  Lever: X
  Custom: X

Average Time: XX minutes per application

Tabs Left Open: X (for manual completion)
```

```
📋 OPEN-ENDED QUESTIONS GENERATED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. "Why are you interested?" → [response used]
2. "Describe experience with X" → [response used]

Review these in logs/questions/ for accuracy!
```

```
⏸️ PENDING MANUAL COMPLETION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. [Company] - [Role] - [Blocker Reason]
   Tab: Left open
   Action: [What user needs to do]
```

---

## Files to Update

### On EVERY Application (Complete or Blocked)

| File | What to Update |
|------|----------------|
| `logs/applications/[date]_[company]_[role].md` | Create detailed record |
| `logs/questions/all_questions.md` | Add all questions |
| `logs/questions/unanswered.md` | Add unknown questions |
| `logs/performance/current_session.md` | Add timing data |

### On COMPLETED Applications Only

| File | What to Update |
|------|----------------|
| `data/applications.csv` | Add new row (mark as External, status=Applied) |
| `logs/sessions/session_*.md` | Add application entry |

### On BLOCKED Applications

| File | What to Update |
|------|----------------|
| `data/applications.csv` | Add new row (status=Pending Manual) |
| `logs/session_stops.md` | Add blocker entry |
| `logs/applications/[date]_[company]_[role].md` | Include blocker details |

### On EVERY Session End

| File | What to Update |
|------|----------------|
| `logs/session_stops.md` | **MANDATORY** - Log session end reason |
| `logs/sessions/session_*.md` | Update session summary |

---

## Critical Rules (PRIORITY ORDER)

1. **🏆 COMPLETE APPLICATIONS NO MATTER WHAT** - Experience mismatches, salary, location are NOT reasons to stop
2. **📝 LOG EVERY SESSION STOP** - Always document why a session ended
3. **⏸️ SOFT BLOCKERS: LEAVE TAB OPEN, CONTINUE** - Don't close tabs with pending verifications
4. **🔄 DIRECTOR SUPERVISES, APPLICANT EXECUTES** - Clear separation of concerns
5. **📋 LOG ALL OPEN-ENDED QUESTIONS** - These need human review
6. **⏱️ TRACK TIME PER PAGE** - External apps have multiple pages
7. **💾 SAVE GENERATED RESPONSES** - For quality review
8. **🔒 NEVER DELETE DATA** - Only append, never remove application records
