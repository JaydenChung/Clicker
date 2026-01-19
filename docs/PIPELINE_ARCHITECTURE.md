# Multi-Agent Pipeline Architecture

> **Solves**: Context degradation across multiple applications
> **Enables**: Consistent quality resume tailoring at scale

---

## The Problem

With a single LLM context handling everything:

```
Application 1: Fresh context → HIGH QUALITY tailoring ⭐⭐⭐⭐⭐
Application 2: Context bloated → GOOD tailoring ⭐⭐⭐⭐
Application 3: Context full → DEGRADED tailoring ⭐⭐⭐
Application 4: Context exhausted → POOR tailoring ⭐⭐
```

The LLM "forgets" the tailoring instructions because they're buried under application history.

---

## The Solution: Fresh Context Per Phase

Each phase of the pipeline uses a FRESH LLM context:

```
Application 1:
  JD Analysis → Fresh API call → Perfect analysis ⭐⭐⭐⭐⭐
  Tailoring   → Fresh API call → Perfect resume ⭐⭐⭐⭐⭐
  Scoring     → Fresh API call → Accurate score ⭐⭐⭐⭐⭐

Application 10:
  JD Analysis → Fresh API call → Perfect analysis ⭐⭐⭐⭐⭐
  Tailoring   → Fresh API call → Perfect resume ⭐⭐⭐⭐⭐
  Scoring     → Fresh API call → Accurate score ⭐⭐⭐⭐⭐
```

**Same quality on application 1, 10, or 100.**

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                         MULTI-AGENT PIPELINE                                         │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                      │
│   CURSOR AGENT (Browser)                ORCHESTRATOR (Python - Background)           │
│   ┌─────────────────────────┐           ┌─────────────────────────────────────────┐ │
│   │                         │           │                                         │ │
│   │  1. Find job listing    │           │   scripts/pipeline_orchestrator.py      │ │
│   │                         │           │                                         │ │
│   │  2. Extract JD text     │           │   Watches for: pending_jd.json          │ │
│   │     ↓                   │           │                                         │ │
│   │  3. Write pending_jd ───┼──────────▶│   4. JD Analysis (Fresh LLM call)       │ │
│   │                         │           │      ↓                                  │ │
│   │  4. WAIT...             │           │   5. Resume Tailoring (Fresh LLM call)  │ │
│   │     ↓                   │           │      ↓                                  │ │
│   │  5. Poll for ready      │           │   6. ATS Scoring (Fresh LLM call)       │ │
│   │     ↓                   │           │      ↓                                  │ │
│   │  6. Read resume_ready ◀─┼───────────│   7. Refinement loop (if score < 90%)   │ │
│   │     ↓                   │           │      ↓                                  │ │
│   │  7. Apply to job        │           │   8. Compile PDF                        │ │
│   │     ↓                   │           │      ↓                                  │ │
│   │  8. Log everything      │           │   9. Write resume_ready.json            │ │
│   │     ↓                   │           │                                         │ │
│   │  9. Next job            │           │   10. Wait for next job                 │ │
│   │                         │           │                                         │ │
│   └─────────────────────────┘           └─────────────────────────────────────────┘ │
│              │                                          │                            │
│              │        FILE-BASED COMMUNICATION          │                            │
│              │                                          │                            │
│              └───────▶ data/pipeline/ ◀─────────────────┘                            │
│                        ├── pending_jd.json                                           │
│                        ├── resume_ready.json                                         │
│                        └── orchestrator_status.json                                  │
│                                                                                      │
└─────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Components

### 1. Cursor Agent (`/apply-pipeline`)

**Location**: `.cursor/commands/apply-pipeline.md`

**Responsibilities**:
- Browser automation (navigate, click, fill forms)
- Extract job descriptions
- Signal orchestrator (write `pending_jd.json`)
- Wait for tailored resume
- Apply to jobs
- Log events

**Does NOT**:
- Tailor resumes
- Score resumes
- Make heavy LLM calls

### 2. Python Orchestrator

**Location**: `scripts/pipeline_orchestrator.py`

**Responsibilities**:
- Watch for incoming JDs
- Call specialized agent modules with FRESH contexts
- Coordinate the tailor → score → refine loop
- Compile LaTeX to PDF
- Signal completion

**Agent Modules**:
- `scripts/agents/jd_analyzer.py` - Extract keywords and requirements
- `scripts/agents/resume_tailor.py` - Generate tailored LaTeX
- `scripts/agents/ats_scorer.py` - Score and provide feedback

### 3. File-Based Communication

**Why files?**
- Simple, reliable, cross-process
- Atomic writes (single line = safe)
- Easy to debug (human-readable)
- No complex IPC needed

**Files**:
| File | Writer | Reader | Purpose |
|------|--------|--------|---------|
| `pending_jd.json` | Cursor | Orchestrator | New job to process |
| `resume_ready.json` | Orchestrator | Cursor | Tailored resume ready |
| `orchestrator_status.json` | Orchestrator | Cursor | Progress updates |

---

## Data Flow

### Per-Job Flow

```
1. Cursor: Find job → Extract JD
                         ↓
2. Cursor: Write data/pipeline/pending_jd.json
                         ↓
3. Orchestrator: Detect pending_jd.json
                         ↓
4. Orchestrator: analyze_jd() → FRESH Claude API call
                         ↓
5. Orchestrator: tailor_resume() → FRESH Claude API call
                         ↓
6. Orchestrator: score_resume() → FRESH Claude API call
                         ↓
7. Orchestrator: if score < 90%:
                    - Get suggestions
                    - tailor_resume() again → FRESH call
                    - score_resume() again → FRESH call
                    - Repeat max 3 times
                         ↓
8. Orchestrator: pdflatex → Compile PDF
                         ↓
9. Orchestrator: Write data/pipeline/resume_ready.json
                         ↓
10. Orchestrator: Delete pending_jd.json
                         ↓
11. Cursor: Detect resume_ready.json
                         ↓
12. Cursor: Read result, apply to job
                         ↓
13. Cursor: Delete resume_ready.json, move to next job
```

### Session Flow

```
Terminal 1:                              Terminal 2 (Cursor):
$ python3 scripts/pipeline_orchestrator.py
🚀 Pipeline Orchestrator Started
Waiting for jobs...                      User: /apply-pipeline
                                         
📥 New JD detected: Google              → Extracting JD...
  📋 Analyzing JD...                     → Writing pending_jd.json
  ✏️  Tailoring resume (iter 1)...       → Waiting...
  📊 Scoring (78%)...                    
  ✏️  Tailoring resume (iter 2)...       
  📊 Scoring (94%)...                    
  📄 Compiling PDF...                    
✅ Resume ready: 94%                     → Found resume_ready.json
                                         → Applying to job...
Waiting for next job...                  → Moving to next job...
```

---

## Configuration

### Prerequisites

1. **Install LaTeX**:
   ```bash
   brew install basictex
   # Add to PATH: export PATH="/Library/TeX/texbin:$PATH"
   ```

2. **Install Python dependencies**:
   ```bash
   pip install anthropic
   ```

3. **Set API key**:
   ```bash
   export ANTHROPIC_API_KEY="your-key-here"
   ```

### Settings

| Setting | Location | Default |
|---------|----------|---------|
| Target ATS score | `pipeline_orchestrator.py` | 90% |
| Max refinement iterations | `pipeline_orchestrator.py` | 3 |
| Wait timeout | `apply-pipeline.md` | 5 minutes |

---

## Output Structure

```
resume/tailored/
├── 20260119_103000_Google_SWE_final.pdf        # Ready to upload!
├── 20260119_103000_Google_SWE_final.tex        # LaTeX source
├── 20260119_103000_Google_SWE_jd_analysis.json # JD analysis
├── 20260119_103000_Google_SWE_v1.tex           # Iteration 1
├── 20260119_103000_Google_SWE_v1_score.json    # Score: 78%
├── 20260119_103000_Google_SWE_v2.tex           # Iteration 2  
├── 20260119_103000_Google_SWE_v2_score.json    # Score: 94% ✓
└── README.md                                    # Instructions
```

---

## Logging

### Cursor Events
Location: `data/events/session_YYYY-MM-DD_N.jsonl`

Events: `jd_extracted`, `tailoring_started`, `tailoring_completed`, `pending_upload`

### Orchestrator Logs
Location: `logs/pipeline/pipeline_YYYY-MM-DD.jsonl`

Events: `pipeline_started`, `jd_analyzed`, `resume_tailored`, `resume_scored`, `pipeline_completed`

---

## Handling File Upload Blocker

External sites can't receive programmatic file uploads (browser security).

**Solution**: Leave tab open, continue session

```
Session end output:

PENDING MANUAL UPLOAD (tabs left open):
• Stripe - External site
  Resume at: resume/tailored/..._Stripe_PM_final.pdf
  Tab should be open, just upload and submit
```

Human can quickly:
1. Find the open tab
2. Upload the tailored PDF
3. Submit

---

## Quick Start

### 1. Start the orchestrator (Terminal 1)
```bash
cd /Users/jchung/code/Clicker
export ANTHROPIC_API_KEY="your-key"
python3 scripts/pipeline_orchestrator.py
```

### 2. Run the Cursor command
In Cursor, type: `/apply-pipeline`

### 3. Watch the magic
- Cursor extracts JDs
- Orchestrator tailors resumes with fresh contexts
- Applications get submitted with 90%+ ATS scores
- PDFs saved for manual uploads

---

## Why This Architecture?

| Aspect | Single Agent | Pipeline |
|--------|--------------|----------|
| Context per job | Grows with history | Fresh each time |
| Quality consistency | Degrades | Constant |
| Debugging | Hard (mixed concerns) | Easy (isolated) |
| Scalability | Limited by context | Unlimited |
| Token efficiency | Wasted on history | Optimized |

---

## Future Enhancements

1. **Real-time dashboard**: Watch orchestrator progress in browser
2. **Parallel tailoring**: Tailor next resume while applying to current
3. **Resume caching**: Reuse similar tailorings for similar JDs
4. **External ATS APIs**: Use Jobscan-like services for higher accuracy
5. **Multi-model**: Use different models for different tasks

