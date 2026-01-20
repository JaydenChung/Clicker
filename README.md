# 🖱️ Clicker - LinkedIn Job Application Automation

An autonomous job application system powered by **Cursor AI** with a **multi-agent pipeline** that tailors resumes in real-time, achieves 90%+ ATS scores, and applies to jobs at scale.

---

## 🚀 NEW: Multi-Agent Pipeline Architecture

This system uses a revolutionary **two-process architecture** that ensures consistent, high-quality resume tailoring for EVERY application:

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                     MULTI-AGENT PIPELINE ARCHITECTURE                         ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                               ║
║     TERMINAL 1                              TERMINAL 2 (Cursor)               ║
║  ┌─────────────────────┐                 ┌─────────────────────┐             ║
║  │  PYTHON             │                 │  CURSOR AGENT       │             ║
║  │  ORCHESTRATOR       │◄───files────────│  (Browser Control)  │             ║
║  │                     │                 │                     │             ║
║  │  • JD Analyzer      │                 │  • Navigate LinkedIn│             ║
║  │  • Template Selector│────files───────►│  • Extract JD text  │             ║
║  │  • Resume Tailor    │                 │  • Wait for resume  │             ║
║  │  • ATS Scorer       │                 │  • Fill forms       │             ║
║  │  • PDF Compiler     │                 │  • Submit apps      │             ║
║  │                     │                 │                     │             ║
║  │  Fresh Gemini Pro   │                 │                     │             ║
║  │  call for EACH step │                 │                     │             ║
║  └─────────────────────┘                 └─────────────────────┘             ║
║                                                                               ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

### Why This Architecture?

| Old Approach (Single Agent) | New Approach (Pipeline) |
|---------------------------|-------------------------|
| ❌ Context fills up over time | ✅ Fresh context every call |
| ❌ Quality degrades by app #4 | ✅ Perfect quality at app #100 |
| ❌ Single resume for all jobs | ✅ Tailored resume per job |
| ❌ No ATS optimization | ✅ 90%+ ATS score guaranteed |
| ❌ One template fits all | ✅ Auto-selects best template |

---

## 📋 Pipeline Workflow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    JOB APPLICATION PIPELINE                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  STEP 1: CURSOR finds job on LinkedIn                                       │
│         ↓                                                                   │
│  STEP 2: CURSOR extracts Job Description                                    │
│         ↓                                                                   │
│  STEP 3: CURSOR writes JD to pending_jd.json                               │
│         ↓                                                                   │
│  ════════════════════ ORCHESTRATOR TAKES OVER ════════════════════         │
│         ↓                                                                   │
│  STEP 4: JD ANALYZER (Fresh Gemini Call)                                    │
│         • Extracts keywords, skills, requirements                           │
│         • Classifies role: SWE, PM, SE, Data, DevOps                       │
│         ↓                                                                   │
│  STEP 5: TEMPLATE SELECTOR                                                  │
│         • Picks best base resume for this role type                        │
│         • PM job → pm.tex, SWE job → swe.tex                               │
│         ↓                                                                   │
│  STEP 6: RESUME TAILOR (Fresh Gemini Call)                                  │
│         • Reads your complete content pool                                  │
│         • Selects most relevant experiences                                 │
│         • Matches keywords from JD                                          │
│         • Uses XYZ formula for bullet points                                │
│         ↓                                                                   │
│  STEP 7: ATS SCORER (Fresh Gemini Call)                                     │
│         • Scores resume against JD                                          │
│         • If score < 90%, provides feedback                                 │
│         ↓                                                                   │
│  STEP 8: REFINEMENT LOOP (up to 3 iterations)                               │
│         • Tailor → Score → Tailor → Score → ...                            │
│         • Until 90%+ achieved                                               │
│         ↓                                                                   │
│  STEP 9: PDF COMPILATION                                                    │
│         • Compiles LaTeX to PDF                                             │
│         • Saves to resume/tailored/                                         │
│         ↓                                                                   │
│  STEP 10: ORCHESTRATOR writes resume_ready.json                            │
│         ↓                                                                   │
│  ════════════════════ CURSOR TAKES OVER ════════════════════               │
│         ↓                                                                   │
│  STEP 11: CURSOR applies with tailored resume                              │
│         ↓                                                                   │
│  REPEAT for next job                                                        │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 🎯 Role-Based Template Selection

The system automatically picks the best base resume for each job:

```
JOB TITLE                         TEMPLATE SELECTED
─────────────────────────────────────────────────────
"Software Engineer"        →      swe.tex
"Frontend Developer"       →      swe.tex
"Product Manager"          →      pm.tex
"Associate PM"             →      pm.tex
"Solutions Engineer"       →      se.tex
"Sales Engineer"           →      se.tex
"Data Scientist"           →      data.tex
"ML Engineer"              →      data.tex
"DevOps Engineer"          →      devops.tex
"SRE"                      →      devops.tex
```

### Adding New Templates

1. Create `resume/templates/your_role.tex`
2. Add entry to `resume/templates/_manifest.json`:

```json
{
  "your_role": {
    "name": "Your Role Name",
    "file": "your_role.tex",
    "keywords": ["job title keywords"],
    "priority": 6
  }
}
```

---

## 🚀 Quick Start

### Prerequisites

- [Cursor IDE](https://cursor.sh) with browser control extension
- Chrome browser
- LinkedIn account (signed in)
- Google Gemini API key (or Anthropic)

### Step 1: Set API Key

```bash
export GOOGLE_API_KEY="your-gemini-api-key"
```

### Step 2: Start the Orchestrator

```bash
# Terminal 1
cd /path/to/Clicker
python3 scripts/pipeline_orchestrator.py
```

You should see:
```
════════════════════════════════════════════════════════════════
🚀 Pipeline Orchestrator Started
════════════════════════════════════════════════════════════════
✅ LLM Provider: GEMINI
✅ Templates available: swe, pm, se, data, devops
Waiting for job descriptions from Cursor agent...
```

### Step 3: Run Cursor Command

```
# In Cursor
/apply-pipeline
```

---

## 📁 Project Structure

```
Clicker/
├── .cursor/commands/              # 🎯 CURSOR COMMANDS
│   ├── plan-search.md             # Generate search strategy
│   └── apply-pipeline.md          # Full pipeline application
│
├── scripts/                       # 🐍 PYTHON ORCHESTRATOR
│   ├── pipeline_orchestrator.py   # Main orchestrator loop
│   └── agents/                    # Specialized LLM agents
│       ├── llm_client.py          # Gemini/Anthropic wrapper
│       ├── jd_analyzer.py         # JD analysis + role classification
│       ├── resume_tailor.py       # Resume generation
│       └── ats_scorer.py          # ATS scoring + feedback
│
├── resume/                        # 📄 RESUME ASSETS
│   ├── templates/                 # Role-specific base templates
│   │   ├── _manifest.json         # Template configuration
│   │   ├── swe.tex                # Software Engineer template
│   │   ├── pm.tex                 # Product Manager template
│   │   └── ...                    # Add more as needed
│   └── tailored/                  # Generated tailored resumes
│       ├── {job_id}_final.pdf     # Compiled PDF
│       ├── {job_id}_final.tex     # LaTeX source
│       └── {job_id}_jd_analysis   # JD analysis for reference
│
├── config/                        # ⚠️ USER CONFIGURATION
│   ├── personal_profile.md        # Your info for applications
│   ├── resume_content.md          # FULL content pool for tailoring
│   ├── projects.md                # All projects (even old ones!)
│   ├── job_preferences.md         # Target roles, max apps
│   └── locations.md               # Target cities
│
├── data/                          # 📊 RUNTIME DATA
│   ├── pipeline/                  # Cursor ↔ Orchestrator communication
│   │   ├── pending_jd.json        # Cursor writes, Orchestrator reads
│   │   └── resume_ready.json      # Orchestrator writes, Cursor reads
│   ├── applications.csv           # Master tracking spreadsheet
│   └── events/                    # Event logs for processing
│
└── logs/                          # 📝 SESSION LOGS
    ├── pipeline/                  # Pipeline-specific logs
    ├── sessions/                  # Application session logs
    └── session_stops.md           # Why sessions ended
```

---

## ⚙️ Configuration

### Content Pool (`config/resume_content.md`)

This file should contain **EVERYTHING** about you - the AI will select what's relevant:

```markdown
## Work Experience

### Company A - Role (2023-Present)
- Achievement 1 with metrics
- Achievement 2 with metrics
- Technologies: Python, AWS, etc.

### Company B - Role (2021-2023)
- Older but still relevant achievements
- ...

## Projects

### Project 1
- Full description
- Technologies used
- Metrics/outcomes

### Project 2
...

## Skills
- Programming: Python, JavaScript, Go, ...
- Cloud: AWS, GCP, Azure
- Tools: Docker, Kubernetes, Terraform
...

## Education
...

## Certifications
...
```

**Key Point**: Include MORE than what fits on one page. The AI will select the most relevant content for each job.

### Templates (`resume/templates/_manifest.json`)

```json
{
  "templates": {
    "swe": {
      "name": "Software Engineer",
      "file": "swe.tex",
      "keywords": ["software engineer", "developer", "sde"],
      "priority": 1
    },
    "pm": {
      "name": "Product Manager", 
      "file": "pm.tex",
      "keywords": ["product manager", "apm", "program manager"],
      "priority": 2
    }
  },
  "default_template": "swe"
}
```

---

## 🔄 Typical Usage Workflow

```
Session Start:
┌────────────────────────────────────────────────────┐
│ Step 1: PLAN                                       │
│ Command: "/plan-search"                            │
│ → Analyzes your application history                │
│ → Generates optimized search strategy              │
└────────────────────────────────────────────────────┘
                      │
                      ▼
┌────────────────────────────────────────────────────┐
│ Step 2: START ORCHESTRATOR                         │
│ Terminal: python3 scripts/pipeline_orchestrator.py │
│ → Loads your content pool                          │
│ → Loads template manifest                          │
│ → Waits for jobs from Cursor                       │
└────────────────────────────────────────────────────┘
                      │
                      ▼
┌────────────────────────────────────────────────────┐
│ Step 3: APPLY                                      │
│ Cursor: "/apply-pipeline"                          │
│ → Searches LinkedIn                                │
│ → For each job:                                    │
│   → Extracts JD → Orchestrator tailors resume      │
│   → Achieves 90%+ ATS score                        │
│   → Applies with tailored resume                   │
│ → Continues until limit reached                    │
└────────────────────────────────────────────────────┘
                      │
                      ▼
┌────────────────────────────────────────────────────┐
│ Step 4: REVIEW                                     │
│ → Check resume/tailored/ for generated resumes     │
│ → Review logs/session_stops.md                     │
│ → Export applications.csv to Google Sheets         │
└────────────────────────────────────────────────────┘
```

---

## 📊 Output Files

After each application, you'll find in `resume/tailored/`:

| File | Description |
|------|-------------|
| `{job_id}_jd_analysis.json` | Extracted keywords, skills, role category |
| `{job_id}_v1.tex` | First tailoring iteration |
| `{job_id}_v1_score.json` | ATS score and feedback |
| `{job_id}_v2.tex` | Refined (if needed) |
| `{job_id}_v2_score.json` | Improved score |
| `{job_id}_final.tex` | Best version |
| `{job_id}_final.pdf` | Compiled PDF (if LaTeX installed) |

---

## 🚨 Critical Rules: Autonomous Operation

This system is designed to run **autonomously**. The user may leave their computer unattended.

### Rule #1: Never Stop for "Fit" Reasons
The session must **NEVER** stop because:
- ❌ Job requires more experience
- ❌ Salary seems wrong
- ❌ Role seems too senior/junior

**Action**: Complete the application anyway, log concerns, continue.

### Rule #2: Soft Blockers → Leave Tab Open, Continue
For email/phone verification:
1. Log the blocker
2. Leave tab open
3. Continue applying

### Rule #3: Hard Blockers → Skip, Continue
For CAPTCHA, mandatory assessments:
1. Log the blocker
2. Skip THIS application
3. Continue with next job

---

## 🛠️ Troubleshooting

### "No LLM API key found"
```bash
export GOOGLE_API_KEY="your-key-here"
# or
export ANTHROPIC_API_KEY="your-key-here"
```

### "pdflatex not found"
```bash
# macOS
brew install --cask basictex

# Then restart terminal or:
eval "$(/usr/libexec/path_helper)"
```

### "Template not found"
Ensure template files exist in `resume/templates/` and are listed in `_manifest.json`.

### "Score stuck below 90%"
- Check that `config/resume_content.md` has comprehensive content
- Ensure the job isn't too far outside your experience
- Review feedback in `*_score.json` files

---

## 📄 License

MIT License - See LICENSE file.

## ⚠️ Disclaimer

Use responsibly per LinkedIn's Terms of Service. This tool is for personal productivity. Authors not responsible for account restrictions from automated activity.
