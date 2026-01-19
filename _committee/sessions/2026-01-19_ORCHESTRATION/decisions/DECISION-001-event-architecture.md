# Decision Record: DECISION-001

## Event-Sourcing Architecture for Agent Coordination

**Decision ID**: DECISION-001  
**Session**: 2026-01-19_ORCHESTRATION  
**Date**: 2026-01-19  
**Status**: APPROVED

---

## Decision

Adopt a **staged event-sourcing architecture** to separate job application execution from tracking/logging concerns.

---

## Context

The current system has a single Cursor LLM agent responsible for:
- Applying to jobs (primary function)
- Logging to CSV
- Tracking questions
- Monitoring performance
- Multiple other tracking tasks

This creates a bottleneck where tracking overhead slows down the application loop.

---

## Options Considered

| Option | Description | Verdict |
|--------|-------------|---------|
| A. Sidecar Pattern | Watcher process runs alongside main agent | Approved for Stage 2 |
| B. Multi-Agent Swarm | Multiple parallel LLM instances | Rejected (not feasible in Cursor) |
| C. Event-Sourced Monolith | Single agent, deferred processing | **Approved for Stage 1** |
| D. Status Quo | Keep current architecture | Rejected (confirmed bottleneck) |

---

## Decision Details

### Stage 1: Immediate Implementation
1. Main agent emits events to `data/events/session_*.jsonl`
2. Processing happens post-session via `scripts/process_session.py`
3. Remove all pseudo-agent "signaling" from main agent

### Stage 2: Future Enhancement
1. Add `scripts/watcher.py` for real-time processing
2. Enable live tracking and stuck detection

### Stage 3: Future Expansion
1. Additional consumers (ATS scorer, etc.) read from event stream
2. Architecture scales without changing main agent

---

## Mitigations Required

1. Test Cursor file append behavior before deployment
2. Include session_id in every event
3. Handle orphaned/incomplete events in processor
4. Make processing idempotent
5. Accept temporary loss of real-time stuck detection

---

## Rationale

- Solves confirmed bottleneck (tracking overhead)
- Minimal immediate complexity (Stage 1 is simple)
- Enables future expansion (Stages 2-3)
- Skeptics approved after staged approach proposed
- Red Team found no fatal flaws

---

## Dissenting Opinions

None recorded. Skeptics (Viktor Petrov, Otto Grimm) approved the staged approach.

---

## Contributors

- Dr. Yuki Tanaka (Agent Architecture Chair) — Pattern analysis
- Dr. Robert Kim (Concurrency Chair) — Parallelism constraints
- Dr. Alex Thompson (Integration Chair) — Cursor capabilities
- Viktor Petrov (Skeptic) — Complexity concerns, accepted staged approach
- Otto Grimm (Chief Skeptic) — Validated problem is real
- Damon Brooks (Event-Driven Specialist) — Event schema design
- "Raven" Black (Red Team Chair) — Attack vectors and mitigations

---

## Follow-Up Actions

See: `action_items.md`

