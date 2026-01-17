# 🖱️ Clicker - LinkedIn Job Application Automation

An automated job application system powered by Cursor AI that searches LinkedIn and applies to jobs using Easy Apply.

## 🚀 Quick Start

1. **Clone this repository**
2. **Fill out the config files** (see Setup below)
3. **Open LinkedIn** in a browser controlled by Cursor
4. **Sign in** to your LinkedIn account
5. **Run the command**: Just say "apply to jobs" or "start applying"

## 📁 Project Structure

```
Clicker/
├── .cursorrules              # Main orchestration rules for Cursor
├── README.md                 # This file
│
├── config/                   # Configuration files (⚠️ EDIT THESE FIRST!)
│   ├── job_preferences.md    # Job titles, keywords, filters
│   ├── locations.md          # Target cities and regions
│   └── personal_profile.md   # Your info for application answers
│
├── agents/                   # Agent instruction files
│   ├── job_applicant.md      # Primary application agent
│   ├── search_logger.md      # Search session tracking
│   ├── application_tracker.md # Application history
│   ├── question_tracker.md   # Unanswered question logging
│   └── performance_monitor.md # Timing and stuck detection
│
└── logs/                     # Generated logs (auto-populated)
    ├── sessions/             # Per-session search logs
    ├── applications/         # Individual application records
    ├── questions/            # Question database & unanswered
    └── performance/          # Timing metrics & stuck events
```

## ⚙️ Setup (Required Before First Run)

### 1. Personal Profile (`config/personal_profile.md`)

**⚠️ CRITICAL**: This file must be filled out completely!

Replace all `<!-- FILL IN: ... -->` placeholders with your actual information:
- Your name, email, phone
- Work authorization status
- Years of experience for each skill
- Yes/No answers for common questions
- Salary expectations
- Resume filename (must be uploaded to LinkedIn)

### 2. Job Preferences (`config/job_preferences.md`)

Define what jobs you're looking for:
- Target job titles and keywords
- Experience levels
- Work arrangements (remote/hybrid/on-site)
- Industries of interest

### 3. Locations (`config/locations.md`)

Set your target locations:
- Primary cities to search
- Whether you're open to remote
- Relocation preferences

## 🤖 Agents

| Agent | Purpose |
|-------|---------|
| **Job Applicant** | Main agent - reads config, searches jobs, fills forms, submits |
| **Search Logger** | Tracks what/where you searched each session |
| **Application Tracker** | Detailed MD file for every job applied |
| **Question Tracker** | Logs questions, especially ones it can't answer |
| **Performance Monitor** | Times each step, logs where it gets stuck |

## 📝 Commands

| Command | What it does |
|---------|--------------|
| "apply to jobs" | Start full search & apply workflow |
| "apply to next 5 jobs" | Apply to next 5 visible Easy Apply jobs |
| "status" | Show current session statistics |
| "stop" | End session gracefully |
| "what questions need answers" | Show unanswered questions |

## 📊 Logs

### Session Logs (`logs/sessions/`)
Created each time you run an application session. Contains:
- All searches performed
- Jobs viewed and applied
- Session statistics

### Application Logs (`logs/applications/`)
One file per application with:
- Job details
- Questions asked and answers given
- Timing information
- Application status

### Question Logs (`logs/questions/`)
- `unanswered.md` - **Review this regularly!** Add answers to your profile.
- `all_questions.md` - Complete question database

### Performance Logs (`logs/performance/`)
- `stuck_log.md` - Where automation gets stuck
- `history.md` - Historical performance trends

## 🔄 Workflow

```
┌─────────────────────────────────────────────────────────┐
│                    SESSION START                         │
│  1. Load config files                                   │
│  2. Create session log                                  │
│  3. Navigate to LinkedIn Jobs                           │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│                    SEARCH LOOP                          │
│  FOR each keyword + location combination:               │
│    - Perform search                                     │
│    - Log results                                        │
│    - Process matching jobs                              │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│                  APPLICATION LOOP                       │
│  FOR each Easy Apply job:                               │
│    - Click Easy Apply                                   │
│    - Fill form using personal_profile.md                │
│    - Log any unknown questions                          │
│    - Submit application                                 │
│    - Record to application tracker                      │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│                    SESSION END                          │
│  Triggers:                                              │
│    - Context > 80% used                                 │
│    - All combinations searched                          │
│    - Rate limit detected                                │
│  Actions:                                               │
│    - Finalize all logs                                  │
│    - Output summary                                     │
│    - List unanswered questions                          │
└─────────────────────────────────────────────────────────┘
```

## 🛡️ Safety Features

- **No duplicate applications** - Skips jobs with "Applied" badge
- **Graceful completion** - Never abandons mid-application
- **Rate limit detection** - Stops if LinkedIn rate limits detected
- **Error threshold** - Ends session after 5 consecutive failures
- **Complete logging** - Every action is recorded

## 📋 After Each Session

1. **Review unanswered questions**: 
   ```
   logs/questions/unanswered.md
   ```
   Add answers to `config/personal_profile.md`

2. **Check stuck events**:
   ```
   logs/performance/stuck_log.md
   ```
   Note any recurring issues

3. **Review applications**:
   ```
   logs/applications/_index.md
   ```
   Track your application status

## ⚠️ Prerequisites

- [Cursor IDE](https://cursor.sh) with browser control capability
- Chrome browser with Cursor browser extension
- LinkedIn account (signed in before starting)
- Completed config files (see Setup section)

## 🐛 Troubleshooting

### "Easy Apply button not found"
- Job may require external application
- Agent will skip and move to next job

### "Application dialog won't open"
- Wait 3 seconds and retry
- Check if page fully loaded

### "Form field errors"
- Check `logs/questions/unanswered.md` for missing answers
- Update `config/personal_profile.md`

### "Rate limited"
- LinkedIn has application limits
- Wait and try again later

### "Profile not filled out"
- Ensure all `<!-- FILL IN: ... -->` placeholders are replaced
- The agent needs this info to fill out applications

## 📈 Tips for Best Results

1. **Fill out your profile completely** - Fewer guesses = better applications
2. **Review unanswered questions daily** - Continuously improve the system
3. **Start with shorter sessions** - Test before long runs
4. **Monitor stuck_log.md** - Identify and fix recurring issues
5. **Keep resume uploaded to LinkedIn** - Faster applications

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

MIT License - See LICENSE file for details.

## ⚠️ Disclaimer

Use responsibly and in accordance with LinkedIn's Terms of Service. This tool is for educational and personal productivity purposes. The authors are not responsible for any account restrictions that may result from automated activity.
