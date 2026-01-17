# 🖱️ Clicker - LinkedIn Job Application Automation

An automated job application system powered by Cursor AI that intelligently searches LinkedIn and applies to jobs using Easy Apply.

## 🚀 Three-Command System

### Command 1: Plan Search
```
"plan search" or "what should I search"
```
Analyzes your application history and generates an **optimal search strategy** based on:
- Which keyword + location combos are saturated
- Which areas need more coverage
- Historical effectiveness data

### Command 2: Apply to Jobs (Easy Apply)
```
"apply to jobs" or "start applying"
```
Executes the search plan and applies to **Easy Apply** jobs automatically.

### Command 3: Apply External (Non-Easy Apply)
```
"apply external" or "external applications"
```
Handles jobs that redirect to **external company websites**:
- Detects ATS systems (Workday, Greenhouse, Lever, etc.)
- Uses Director + Executor agent pair
- Handles open-ended questions
- Flags complex situations for human review

---

## 📁 Project Structure

```
Clicker/
├── .cursorrules              # Main orchestration rules
├── README.md                 # This file
│
├── config/                   # Configuration (⚠️ EDIT THESE FIRST!)
│   ├── job_preferences.md    # Job titles, keywords, filters
│   ├── locations.md          # Target cities and regions
│   ├── personal_profile.md   # Your info for application answers
│   ├── resume_content.md     # Detailed resume for open-ended questions
│   └── projects.md           # Project portfolio
│
├── agents/                   # 9 specialized agents
│   ├── search_strategist.md  # Plans optimal search strategy
│   ├── job_applicant.md      # Executes Easy Apply applications
│   ├── application_director.md # Supervises external applications
│   ├── external_applicant.md # Executes on external websites
│   ├── csv_tracker.md        # Maintains master CSV
│   ├── search_logger.md      # Logs session searches
│   ├── application_tracker.md # Detailed application logs
│   ├── question_tracker.md   # Tracks unanswered questions
│   └── performance_monitor.md # Timing and stuck detection
│
├── data/                     # Persistent data files
│   ├── applications.csv      # 📊 Master CSV (import to Google Sheets!)
│   ├── current_search_plan.md # Active search strategy
│   └── search_insights.md    # Learning from past sessions
│
└── logs/                     # Session logs
    ├── sessions/             # Per-session search logs
    ├── applications/         # Individual application records
    ├── questions/            # Question database
    └── performance/          # Timing metrics
```

---

## ⚙️ Setup (Required Before First Run)

### 1. Personal Profile (`config/personal_profile.md`)

**⚠️ CRITICAL**: Fill out completely!

Replace all `<!-- FILL IN: ... -->` placeholders with:
- Your name, email, phone
- Work authorization status
- Years of experience per skill
- Resume filename (must be on LinkedIn)

### 2. Job Preferences (`config/job_preferences.md`)

Define your target jobs:
- Job titles and keywords to search
- Experience levels
- Work arrangements

### 3. Locations (`config/locations.md`)

Set target locations in priority order.

### 4. Resume Content (`config/resume_content.md`)

Detailed resume data for answering open-ended questions:
- Work experience with achievements
- Technical skills with proficiency levels
- Education details
- Key strengths with examples

### 5. Projects (`config/projects.md`)

Your project portfolio:
- Featured projects with descriptions
- Technologies used
- Challenges and solutions
- Links to demos/GitHub

---

## 🤖 The 9 Agents

| Agent | Type | Purpose |
|-------|------|---------|
| **Search Strategist** | Planning | Analyzes data, predicts optimal searches |
| **Job Applicant** | Easy Apply | Applies to Easy Apply jobs |
| **Application Director** | External (Supervisor) | Analyzes external pages, directs executor |
| **External Applicant** | External (Executor) | Fills forms on external websites |
| **CSV Tracker** | Data | Maintains master CSV for Google Sheets |
| **Search Logger** | Logging | Tracks searches per session |
| **Application Tracker** | Logging | Detailed logs per application |
| **Question Tracker** | Logging | Flags unanswered questions |
| **Performance Monitor** | Monitoring | Tracks timing and stuck states |

---

## 📊 Google Sheets Integration

The master CSV at `data/applications.csv` tracks **ALL applications** across **ALL sessions**.

### Import to Google Sheets
1. Download `data/applications.csv`
2. Google Sheets → File → Import → Upload
3. Select "Create new spreadsheet"
4. Separator: Comma

### CSV Columns
- `application_id` - Unique identifier
- `date_applied`, `time_applied` - When applied
- `company`, `job_title`, `location` - Job details
- `work_type` - Remote/Hybrid/On-site
- `job_url` - LinkedIn URL
- `status` - Applied/Interview/Rejected/Offer
- `search_keyword`, `search_location` - How job was found
- `time_to_apply_seconds` - Application speed
- And more...

### Recommended Sheet Setup
1. Freeze header row
2. Add filters to all columns
3. Conditional formatting for Status:
   - Applied = Yellow
   - Interview = Green
   - Rejected = Red
   - Offer = Blue

---

## 🌐 External Applications (Non-Easy Apply)

External applications are more complex because they redirect to company websites with varying ATS systems.

### Supported ATS Systems

| ATS | Complexity | Account Required |
|-----|------------|------------------|
| **Greenhouse** | Low (1-2 pages) | No |
| **Lever** | Low (1 page) | No |
| **SmartRecruiters** | Medium | No |
| **Workday** | High (4-7 pages) | Yes |
| **Taleo** | High | Yes |
| **iCIMS** | Medium | Sometimes |
| **Custom** | Variable | Variable |

### How It Works

1. **Application Director** (Supervisor):
   - Analyzes each page
   - Identifies the ATS system
   - Determines what fields need filling
   - Handles open-ended questions
   - Decides when to skip vs. continue

2. **External Applicant** (Executor):
   - Follows Director's instructions
   - Fills form fields
   - Handles file uploads
   - Navigates multi-page forms
   - Reports results back

### Open-Ended Questions

The Director handles text-based questions by:
- Categorizing the question type
- Generating appropriate responses from templates
- Using your profile data for specifics
- Flagging uncertain answers for human review

### Blockers

Some situations require human intervention:
- CAPTCHA challenges
- Two-factor authentication
- Complex custom ATS systems
- Ambiguous required fields

These are logged and the application is skipped.

---

## 🔄 Typical Workflow

```
┌────────────────────────────────────────────────┐
│ Step 1: PLAN                                   │
│ Run: "plan search"                             │
│ → Analyzes your application history            │
│ → Generates prioritized search strategy        │
│ → Shows saturation by keyword + location       │
└────────────────────────────────────────────────┘
                      │
                      ▼
┌────────────────────────────────────────────────┐
│ Step 2: APPLY                                  │
│ Run: "apply to jobs"                           │
│ → Follows the search plan                      │
│ → Applies to Easy Apply jobs                   │
│ → Updates CSV after each application           │
│ → Ends when context fills or plan complete     │
└────────────────────────────────────────────────┘
                      │
                      ▼
┌────────────────────────────────────────────────┐
│ Step 3: REVIEW                                 │
│ → Download applications.csv                    │
│ → Import to Google Sheets                      │
│ → Review unanswered questions                  │
│ → Update personal_profile.md                   │
└────────────────────────────────────────────────┘
                      │
                      ▼
              Repeat from Step 1
```

---

## 📝 All Commands

| Command | What it does |
|---------|--------------|
| **"plan search"** | Analyze data, generate search strategy |
| **"what should I search"** | Same as plan search |
| **"apply to jobs"** | Start applying using current plan |
| **"start applying"** | Same as apply to jobs |
| **"apply to next X jobs"** | Quick apply to X visible jobs |
| **"status"** | Show current session statistics |
| **"stop"** | End session, save all data |
| **"show csv stats"** | Display application statistics |

---

## 📈 Search Strategy Example

When you run "plan search", you'll see:

```
🎯 Search Strategy Report

Application Distribution:
| Location      | Applications | Status      |
|---------------|--------------|-------------|
| Los Angeles   | 45           | ⚠️ Heavy    |
| San Francisco | 12           | ✅ Moderate |
| San Jose      | 3            | 🟢 Light    |

Recommended Search Order:
1. Solutions Engineer + San Jose (Priority: HIGH)
2. Product Manager + San Jose (Priority: HIGH)
3. Solutions Engineer + San Francisco (Priority: MED)

Skip (Saturated):
- Software Engineer + Los Angeles (45 apps)
```

---

## 🛡️ Safety Features

- **CSV saves after each application** - No data loss
- **No duplicate applications** - Skips "Applied" badges
- **Graceful session end** - Completes current app first
- **Rate limit detection** - Stops if LinkedIn limits detected
- **Complete logging** - Everything tracked for review

---

## 📋 After Each Session

1. **Review unanswered questions**:
   ```
   logs/questions/unanswered.md
   ```
   Add answers to `config/personal_profile.md`

2. **Export to Google Sheets**:
   ```
   data/applications.csv
   ```

3. **Plan next session**:
   ```
   Run "plan search" before next "apply to jobs"
   ```

---

## ⚠️ Prerequisites

- [Cursor IDE](https://cursor.sh) with browser control
- Chrome with Cursor browser extension
- LinkedIn account (signed in)
- Completed config files

---

## 🐛 Troubleshooting

### "No search plan found"
Run `"plan search"` first to generate a strategy.

### "Profile not filled out"
Complete all `<!-- FILL IN: -->` placeholders in config files.

### "CSV not updating"
Check `data/applications.csv` exists with header row.

### "Rate limited"
Wait and try again later. LinkedIn has daily limits.

---

## 📄 License

MIT License - See LICENSE file.

## ⚠️ Disclaimer

Use responsibly per LinkedIn's Terms of Service. This tool is for personal productivity. Authors not responsible for account restrictions from automated activity.
