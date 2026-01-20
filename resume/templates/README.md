# Resume Templates

This directory contains role-specific base resume templates. The pipeline orchestrator automatically selects the best template based on the job description.

## How It Works

```
JOB DESCRIPTION                    TEMPLATE SELECTION
     │                                    │
     ▼                                    ▼
┌─────────────────┐              ┌─────────────────┐
│  JD Analyzer    │   outputs    │  _manifest.json │
│  (Gemini API)   │ ──────────►  │  (role mapping) │
│                 │  role_type   │                 │
└─────────────────┘              └─────────────────┘
                                          │
                                          ▼
                                 ┌─────────────────┐
                                 │  Best Template  │
                                 │  (e.g., pm.tex) │
                                 └─────────────────┘
                                          │
                                          ▼
                                 ┌─────────────────┐
                                 │  Resume Tailor  │
                                 │  (Gemini API)   │
                                 └─────────────────┘
                                          │
                                          ▼
                                 ┌─────────────────┐
                                 │  Tailored Resume│
                                 │  (90%+ ATS)     │
                                 └─────────────────┘
```

## Template Files

| File | Role Category | Keywords |
|------|---------------|----------|
| `swe.tex` | Software Engineer | software engineer, backend, frontend, developer |
| `pm.tex` | Product Manager | product manager, APM, program manager |
| `se.tex` | Solutions Engineer | solutions engineer, sales engineer, pre-sales |
| `data.tex` | Data Scientist | data scientist, analyst, ML engineer |
| `devops.tex` | DevOps/SRE | devops, SRE, platform engineer |

## Creating New Templates

1. Create a new `.tex` file in this directory
2. Add entry to `_manifest.json` with:
   - `name`: Display name
   - `file`: Filename
   - `keywords`: Job title keywords (case-insensitive)
   - `priority`: Lower = higher priority (for tie-breaking)
   - `description`: What roles this template is for

## Template Structure

Each template should be a complete, compilable LaTeX document. The Resume Tailor agent will:

1. Keep the overall structure/formatting
2. Replace content sections with tailored bullet points
3. Match keywords from the JD
4. Use XYZ formula for achievements

## Fallback

If a template file doesn't exist, the orchestrator falls back to `swe.tex` (the default template).

