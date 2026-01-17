# Apply External Command

Execute the **FULL AGENT ORCHESTRA** for non-Easy Apply (external) applications.

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
- Create session log
- Initialize performance tracking
- Confirm resume PDF path

### 2. For Each Non-Easy Apply Job

**Director: Analyze LinkedIn Job Page**
1. Identify company name, job title
2. Click "Apply" button (not Easy Apply)
3. Handle redirect to external site
4. Identify ATS system from URL/page structure

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

**Check for blockers:**
- Account creation required → Attempt or flag
- CAPTCHA → Flag for human, skip job
- File upload → Upload `resume/Jayden_APM.pdf`
- Error message → Log and attempt recovery

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

Navigate back to LinkedIn to continue with next job.

---

## Session End

Triggers:
- Context usage exceeds 80%
- User interrupts
- Too many blockers

**Generate Summaries:**

```
📊 EXTERNAL APPLICATION SESSION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Applications Attempted: X
Successfully Completed: X
Blocked/Skipped: X

By ATS:
  Workday: X
  Greenhouse: X
  Lever: X
  Custom: X

Average Time: XX minutes per application
```

```
📋 OPEN-ENDED QUESTIONS GENERATED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. "Why are you interested?" → [response used]
2. "Describe experience with X" → [response used]

Review these in logs/questions/ for accuracy!
```

---

## Files to Update (EVERY application)

| File | What to Update |
|------|----------------|
| `data/applications.csv` | Add new row (mark as External) |
| `logs/sessions/session_*.md` | Add application entry |
| `logs/applications/*.md` | Create detailed record |
| `logs/performance/current_session.md` | Add timing data |
| `logs/questions/all_questions.md` | Add all questions |
| `logs/questions/unanswered.md` | Add unknown questions |
| `logs/questions/patterns.md` | Add ATS-specific patterns |

---

## Critical Rules

1. **DIRECTOR SUPERVISES, APPLICANT EXECUTES** - Clear separation
2. **LOG ALL OPEN-ENDED QUESTIONS** - These need human review
3. **TRACK TIME PER PAGE** - External apps have multiple pages
4. **HANDLE BLOCKERS GRACEFULLY** - Skip if necessary, don't crash
5. **SAVE GENERATED RESPONSES** - For quality review
