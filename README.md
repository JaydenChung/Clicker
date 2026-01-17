# 🖱️ Clicker - LinkedIn Job Application Automation

An autonomous job application system powered by **Cursor AI** that uses a **multi-agent orchestra** to intelligently search LinkedIn and apply to jobs.

---

## 🎼 Architecture: Cursor Commands + Agent Orchestra

This project uses **Cursor Commands** (`.cursor/commands/`) to orchestrate multiple specialized AI agents. Each command activates a specific combination of agents that work together.

```
┌─────────────────────────────────────────────────────────────────────┐
│                        CURSOR COMMAND                               │
│                    (User types command)                             │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    .cursor/commands/*.md                            │
│              (Command reads and activates agents)                   │
└─────────────────────────────────────────────────────────────────────┘
                              │
          ┌───────────────────┼───────────────────┐
          ▼                   ▼                   ▼
   ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
   │   Agent 1   │     │   Agent 2   │     │   Agent 3   │
   │ (Executor)  │     │  (Tracker)  │     │  (Monitor)  │
   └─────────────┘     └─────────────┘     └─────────────┘
          │                   │                   │
          └───────────────────┼───────────────────┘
                              ▼
                    ┌─────────────────┐
                    │   Data Files    │
                    │  (CSV, Logs)    │
                    └─────────────────┘
```

### Why This Architecture?

- **Modular**: Each agent has a single responsibility
- **Maintainable**: Update one agent without affecting others
- **Scalable**: Add new agents by creating new `.md` files
- **Autonomous**: Agents follow rules to continue without human intervention

---

## 🚀 Three Commands, Full Orchestra

### Command 1: `/plan-search`
```
Triggers: "plan search", "what should I search", "/plan-search"
```

**Agents Activated:**
| Agent | Role |
|-------|------|
| Search Strategist | Analyzes history, generates optimal search plan |

**What it does:**
- Reads application history from CSV
- Calculates saturation by keyword + location
- Generates prioritized search queue
- Saves plan to `data/current_search_plan.md`

---

### Command 2: `/apply-jobs` (Easy Apply)
```
Triggers: "apply to jobs", "start applying", "/apply-jobs"
```

**Agents Activated:**
| Agent | Role |
|-------|------|
| Job Applicant | Executes Easy Apply applications |
| Performance Monitor | Tracks timing for every step |
| Question Tracker | Logs all questions encountered |
| CSV Tracker | Updates master CSV after each application |
| Application Tracker | Creates detailed markdown logs |
| Search Logger | Tracks search progress |

**What it does:**
- Reads search plan from `data/current_search_plan.md`
- Searches LinkedIn for each keyword + location
- Applies to all Easy Apply jobs
- Updates CSV after each application

---

### Command 3: `/apply-external` (Non-Easy Apply)
```
Triggers: "apply external", "external applications", "/apply-external"
```

**Agents Activated:**
| Agent | Role |
|-------|------|
| Application Director | **Supervisor** - analyzes pages, directs executor |
| External Applicant | **Executor** - fills forms as directed |
| Performance Monitor | Tracks timing for every step |
| Question Tracker | Logs all questions (especially open-ended) |
| CSV Tracker | Updates master CSV after each application |
| Application Tracker | Creates detailed markdown logs |

**What it does:**
- Handles jobs that redirect to external company websites
- Detects ATS systems (Workday, Greenhouse, Lever, etc.)
- Navigates multi-page application forms
- Generates responses for open-ended questions

---

## 🚨 Critical Rules: Autonomous Operation

This system is designed to run **autonomously**. The user may leave their computer unattended expecting applications to continue.

### Rule #1: Never Stop for "Fit" Reasons
The session must **NEVER** stop because:
- ❌ Job requires more experience than candidate has
- ❌ Salary seems too high/low
- ❌ Role seems too senior/junior
- ❌ Location isn't ideal

**If a suboptimal job is encountered**: Complete the application anyway, log concerns in notes, continue to next job.

### Rule #2: Soft Blockers → Leave Tab Open, Continue
When encountering verification requirements:
1. Log the blocker in `logs/session_stops.md`
2. Leave the tab open for manual completion
3. Return to LinkedIn
4. Continue applying to other jobs

### Rule #3: Log Every Session Stop
Every session stop is documented in `logs/session_stops.md`:
- **Session START** with timestamp, session ID, max applications planned
- **Session END** with timestamp, stop reason, applications completed
- Application limit reached (`max_applications_per_session` from config)
- Blockers (soft and hard)
- Errors
- User interrupts

### Rule #4: Hard Blockers → Skip Application, Continue Session
For insurmountable blockers (CAPTCHA, mandatory assessments):
1. Log the blocker
2. Skip THIS application
3. Continue with next job

---

## 📁 Project Structure

```
Clicker/
├── .cursor/
│   └── commands/              # 🎯 CURSOR COMMANDS (entry points)
│       ├── plan-search.md     # Invokes Search Strategist
│       ├── apply-jobs.md      # Invokes Easy Apply orchestra
│       └── apply-external.md  # Invokes External App orchestra
│
├── .cursorrules               # Global rules and orchestration
│
├── agents/                    # 🤖 THE 9 AGENTS
│   ├── search_strategist.md   # Plans optimal search strategy
│   ├── job_applicant.md       # Executes Easy Apply applications
│   ├── application_director.md # Supervises external applications
│   ├── external_applicant.md  # Executes on external websites
│   ├── csv_tracker.md         # Maintains master CSV
│   ├── search_logger.md       # Logs session searches
│   ├── application_tracker.md # Detailed application logs
│   ├── question_tracker.md    # Tracks unanswered questions
│   └── performance_monitor.md # Timing and stuck detection
│
├── config/                    # ⚠️ USER CONFIGURATION (edit these!)
│   ├── personal_profile.md    # Your info for application answers
│   ├── job_preferences.md     # Job titles, keywords, filters
│   ├── locations.md           # Target cities and regions
│   ├── resume_content.md      # Detailed resume for questions
│   └── projects.md            # Project portfolio
│
├── data/                      # 📊 PERSISTENT DATA
│   ├── applications.csv       # Master CSV (import to Google Sheets!)
│   ├── current_search_plan.md # Active search strategy
│   └── search_insights.md     # Learning from past sessions
│
├── logs/                      # 📝 SESSION LOGS
│   ├── session_stops.md       # 🚨 All session stop reasons
│   ├── sessions/              # Per-session search logs
│   ├── applications/          # Application records (organized by session)
│   │   ├── _index.md          # Master index of all applications
│   │   └── session_{id}_{type}/ # Session folders (easy-apply or external)
│   ├── questions/             # Question database
│   └── performance/           # Timing metrics
│
└── resume/                    # 📄 YOUR RESUME FILES
    └── Your_Resume.pdf        # PDF for external applications
```

---

## ⚙️ Setup (Required Before First Run)

### Step 1: Fill Out Config Files

All config files have `<!-- FILL IN: ... -->` placeholders. Replace them with your information:

| File | What to Fill |
|------|--------------|
| `config/personal_profile.md` | Name, email, phone, work authorization, experience levels |
| `config/job_preferences.md` | Target job titles, keywords, filters |
| `config/locations.md` | Target cities in priority order |
| `config/resume_content.md` | Detailed resume for open-ended questions |
| `config/projects.md` | Project portfolio with descriptions |

### Step 2: Add Resume

Place your PDF resume in the `resume/` folder for external applications.

### Step 3: Ensure Browser is Ready

- Chrome is open and controlled by Cursor
- LinkedIn is loaded and you are **signed in**
- Browser extension is active

---

## 🤖 The 9 Agents

| Agent | Type | Command | Purpose |
|-------|------|---------|---------|
| **Search Strategist** | Planning | `/plan-search` | Analyzes data, predicts optimal searches |
| **Job Applicant** | Executor | `/apply-jobs` | Applies to Easy Apply jobs |
| **Application Director** | Supervisor | `/apply-external` | Analyzes external pages, directs executor |
| **External Applicant** | Executor | `/apply-external` | Fills forms on external websites |
| **CSV Tracker** | Data | All | Maintains master CSV for Google Sheets |
| **Search Logger** | Logging | `/apply-jobs` | Tracks searches per session |
| **Application Tracker** | Logging | All | Detailed logs per application |
| **Question Tracker** | Logging | All | Flags unanswered questions |
| **Performance Monitor** | Monitoring | All | Tracks timing and stuck states |

---

## 🔄 Typical Workflow

```
┌────────────────────────────────────────────────────┐
│ Step 1: PLAN                                       │
│ Command: "/plan-search"                            │
│ → Search Strategist analyzes your history          │
│ → Generates prioritized search strategy            │
│ → Outputs: data/current_search_plan.md             │
└────────────────────────────────────────────────────┘
                      │
                      ▼
┌────────────────────────────────────────────────────┐
│ Step 2: APPLY (Easy Apply)                         │
│ Command: "/apply-jobs"                             │
│ → 6 agents activate simultaneously                 │
│ → Follows the search plan                          │
│ → Updates CSV after each application               │
│ → Continues until max_applications reached or plan │
│   complete (limit set in config/job_preferences.md)│
└────────────────────────────────────────────────────┘
                      │
                      ▼
┌────────────────────────────────────────────────────┐
│ Step 2b: APPLY (External) - Optional               │
│ Command: "/apply-external"                         │
│ → 6 agents activate (Director + Executor pair)     │
│ → Handles non-Easy Apply jobs                      │
│ → Navigates external ATS systems                   │
└────────────────────────────────────────────────────┘
                      │
                      ▼
┌────────────────────────────────────────────────────┐
│ Step 3: REVIEW                                     │
│ → Check logs/session_stops.md for blockers         │
│ → Complete any "Pending Manual" applications       │
│ → Download applications.csv → Google Sheets        │
│ → Review logs/questions/unanswered.md              │
│ → Update config/personal_profile.md                │
└────────────────────────────────────────────────────┘
                      │
                      ▼
              Repeat from Step 1
```

---

## 📊 Google Sheets Integration

The master CSV at `data/applications.csv` tracks **ALL applications** across **ALL sessions**.

### Import to Google Sheets
1. Download `data/applications.csv`
2. Google Sheets → File → Import → Upload
3. Select "Create new spreadsheet"
4. Separator: Comma

### Application Status Values

| Status | Meaning |
|--------|---------|
| `Applied` | Successfully submitted |
| `Pending Manual` | Soft blocker - awaiting human completion |
| `Skipped` | Hard blocker - could not complete |
| `Interview` | Got interview (manual update) |
| `Rejected` | Rejected (manual update) |
| `Offer` | Received offer (manual update) |

---

## 🌐 Supported ATS Systems

| ATS | Complexity | Account Required |
|-----|------------|------------------|
| **Greenhouse** | Low (1-2 pages) | No |
| **Lever** | Low (1 page) | No |
| **SmartRecruiters** | Medium | No |
| **Workday** | High (4-7 pages) | Yes |
| **Taleo** | High | Yes |
| **iCIMS** | Medium | Sometimes |
| **Custom** | Variable | Variable |

---

## 📝 Command Reference

| Command | Agents | Purpose |
|---------|--------|---------|
| `/plan-search` | 1 | Generate search strategy |
| `/apply-jobs` | 6 | Easy Apply automation |
| `/apply-external` | 6 | External site automation |
| `"status"` | - | Show session statistics |
| `"stop"` | - | End session, save data |

---

## 📋 After Each Session

1. **Check session stops**: `logs/session_stops.md`
2. **Complete blocked apps**: Tabs should still be open
3. **Review unanswered questions**: `logs/questions/unanswered.md`
4. **Export to Google Sheets**: `data/applications.csv`
5. **Run plan-search**: Before next apply session

---

## 🛡️ Safety Features

- **CSV saves after each application** - No data loss
- **No duplicate applications** - Skips "Applied" badges
- **Graceful session end** - Completes current app first
- **Configurable application limit** - `max_applications_per_session` in config (default: 10)
- **Session start/end logging** - Every session documented in `logs/session_stops.md`
- **Complete logging** - Everything tracked for review
- **Soft blocker handling** - Leaves tabs open, continues session

---

## ⚠️ Prerequisites

- [Cursor IDE](https://cursor.sh) with browser control
- Chrome with Cursor browser extension
- LinkedIn account (signed in)
- Completed config files (all `<!-- FILL IN -->` placeholders replaced)

---

## 🐛 Troubleshooting

### "No search plan found"
Run `/plan-search` first to generate a strategy.

### "Profile not filled out"
Complete all `<!-- FILL IN: -->` placeholders in config files.

### "Session stopped unexpectedly"
Check `logs/session_stops.md` for the reason and category.

### "Application pending manual"
A soft blocker occurred. Find the open tab and complete manually.

### "Session ended at 10 applications"
This is the default `max_applications_per_session` limit. Change it in `config/job_preferences.md` under Session Settings.

---

## 📄 License

MIT License - See LICENSE file.

## ⚠️ Disclaimer

Use responsibly per LinkedIn's Terms of Service. This tool is for personal productivity. Authors not responsible for account restrictions from automated activity.
