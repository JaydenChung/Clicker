# Session Goal

**Session ID**: 2026-01-19_PIPELINE
**Requested By**: Human
**Date**: 2026-01-19

---

## Goal Statement

Design the architectural foundation for a multi-agent pipeline that enables:
1. Real-time resume tailoring per job description
2. ATS scoring and optimization
3. Coordinated application submission
4. Comprehensive logging of the entire pipeline

---

## Context

### What V1/V2 Solved
- Logging efficiency (event-sourcing vs. multi-agent signaling)
- Same accuracy, faster execution

### What V1/V2 Did NOT Solve
1. **Soft blockers**: Resume file upload on external sites still fails
2. **No multi-agent pipeline**: Currently one agent does everything sequentially
3. **No resume tailoring**: Same resume for every application
4. **No ATS optimization**: No scoring or refinement loop

### The Human's Vision

```
For EACH application:

1. Main Agent reads Job Description
         ↓
2. JD → RESUME TAILOR AGENT
   • Access to ALL projects, experience, skills
   • Creates custom resume for THIS JD
         ↓
3. Resume → ATS SCORER AGENT  
   • Scores against ATS requirements
   • Refines until >90% match
         ↓
4. Main Agent uploads TAILORED resume
   • Submits application
         ↓
5. LOGGING AGENT records everything
         ↓
6. Continue to next application
```

---

## Key Questions to Address

1. **Architecture**: What coordination pattern enables this pipeline?
   - Sequential handoffs?
   - Event-driven?
   - Supervisor/worker?

2. **Technical Feasibility**: Can Cursor/LLM support this?
   - Multiple "agents" in one context?
   - External services needed?
   - File generation (PDF creation)?

3. **Resume Generation**: How do we create tailored resumes?
   - LaTeX compilation?
   - PDF generation?
   - What tools are available?

4. **ATS Scoring**: How do we score resumes?
   - External API?
   - LLM-based scoring?
   - What's "good enough"?

5. **File Upload Blocker**: How do we solve the resume upload problem?
   - MCP tools?
   - Different approach?

---

## Success Criteria

By session end, we should have:
1. Clear architectural recommendation for the pipeline
2. Understanding of technical constraints and solutions
3. Phased implementation plan
4. Identification of what's possible NOW vs. FUTURE

---

## Subcommittees to Engage

- **01 - Agent Architecture** (Primary) — Multi-agent coordination
- **08 - Resume Optimization** — ATS scoring, resume tailoring
- **06 - ATS Systems** — ATS requirements and parsing
- **03 - Browser Automation & Stealth** — File upload solutions
- **16 - Future Systems** — Emerging AI capabilities
- **15 - Product Strategy** — Vision and roadmap
- **09 - Red Team** — Challenge everything

