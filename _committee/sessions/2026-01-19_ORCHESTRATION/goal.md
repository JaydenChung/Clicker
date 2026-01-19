# Session Goal

**Session ID**: 2026-01-19_ORCHESTRATION
**Requested By**: Human
**Date**: 2026-01-19

---

## Goal Statement

Determine the best architecture for handling multiple tracking/logging agents that need to run alongside the main Cursor AI brain during job application sessions.

---

## Context

### Current State
- The main Cursor AI "brain" (Job Applicant Agent) is responsible for:
  - Applying to jobs
  - Orchestrating all sub-agents (CSV Tracker, Question Tracker, Performance Monitor, etc.)
- The "agents" in `/agents/` are pseudo-agents — role descriptions that the same LLM plays
- Everything runs sequentially through a single LLM context

### Problems Identified
1. The main applicant agent is overloaded with orchestration responsibilities
2. Tracking/logging competes with application execution
3. No true parallelism — everything is sequential
4. Complexity will grow as more capabilities are added (e.g., ATS scoring)

### Options Under Consideration
1. **Watcher Script**: External process that monitors and logs independently
2. **Parallel AI Agents**: Multiple LLM instances running concurrently
3. **Simplified Single Agent**: Keep current approach but streamline

### Future Requirements
- ATS scoring capability (additional agent)
- Real-time analytics
- More tracking agents as system grows

---

## Success Criteria

By session end, we should have:
1. Clear recommendation on architecture approach
2. Understanding of trade-offs for each option
3. Implementation path forward
4. Consideration of future scalability

---

## Subcommittees Engaged

- **01 - Agent Architecture** (Primary)
- **02 - Concurrency & Parallelism**
- **04 - LLM Orchestration**
- **17 - Integration & Ecosystem**
- **09 - Red Team / Adversarial** (Challenge)

