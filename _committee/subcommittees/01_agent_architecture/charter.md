# Subcommittee Charter: Agent Architecture

## Identity
| Field | Value |
|-------|-------|
| **Number** | 01 |
| **Name** | Agent Architecture |
| **Chair** | Dr. Yuki Tanaka |
| **Category** | Technical |
| **Members** | 10 |

---

## Purpose

The Agent Architecture Subcommittee advises the committee on all matters relating to the design, structure, communication, and coordination of AI agents within the job application automation system.

---

## Scope

### In Scope
- Agent roles and responsibilities definition
- Inter-agent communication patterns
- State management across agents
- Supervisor/worker patterns
- Agent lifecycle management
- Error propagation between agents
- Agent composition and decomposition
- Coordination protocols

### Out of Scope
- Specific browser automation (→ Browser Stealth)
- LLM prompt design (→ LLM Orchestration)
- Performance tuning (→ Performance Optimization)

---

## Key Questions We Address

1. How should agents be structured and what roles should exist?
2. How should agents communicate and coordinate?
3. What happens when one agent fails?
4. How do we manage state across multiple agents?
5. When should tasks be split vs. combined?
6. What patterns from distributed systems apply?

---

## Current System Context

The existing system has these agents:
- Job Applicant Agent (Easy Apply execution)
- Application Director (External app supervisor)
- External Applicant (External app executor)
- CSV Tracker (Data persistence)
- Search Logger (Session logging)
- Application Tracker (Application logging)
- Question Tracker (Question logging)
- Performance Monitor (Timing/stuck detection)
- Search Strategist (Planning)

Our subcommittee evaluates whether this structure is optimal.

---

## Archetype Distribution

| Archetype | Members | Names |
|-----------|---------|-------|
| Skeptic | 2 | Viktor Petrov, Ingrid Svensson |
| Academic | 2 | Dr. Yuki Tanaka, Dr. Klaus Richter |
| Practitioner | 5 | Sarah Okonkwo, Chen Wei, Damon Brooks, Lucia Fernandez, Raj Patel |
| Historian | 1 | Marcus Stone |

---

## Meeting Triggers

This subcommittee should be called when:
- Considering changes to agent structure
- Adding or removing agents
- Changing how agents communicate
- Addressing coordination failures
- Designing new capabilities that require agents
- Reviewing agent-related incidents

---

## Relationships to Other Subcommittees

| Subcommittee | Relationship |
|--------------|--------------|
| Concurrency & Parallelism | We design agents; they ensure they can run in parallel |
| LLM Orchestration | We define agent roles; they define how agents use LLMs |
| State & Persistence | We generate state; they ensure it persists |
| Reliability Engineering | We design for reliability; they validate it |
| Browser Stealth | Our agents control browsers; they ensure stealth |

