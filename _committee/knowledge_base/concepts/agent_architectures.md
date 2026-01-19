# Agent Architectures

## Overview

This document describes how AI agents are structured and organized in automation systems like the job application system.

---

## What is an Agent?

In this context, an **agent** is:
- A defined persona or role that the AI assumes
- Specified through a prompt/instruction file
- Has specific responsibilities and behaviors
- Interacts with tools and other agents

---

## Current System Agents

### Job Applicant Agent
**File**: `agents/job_applicant.md`
**Role**: Execute Easy Apply applications
**Trigger**: "apply to jobs" command
**Responsibilities**:
- Read search plan
- Navigate LinkedIn
- Fill application forms
- Submit applications
- Coordinate logging

### Application Director Agent
**File**: `agents/application_director.md`
**Role**: Supervise external applications
**Trigger**: External site detection
**Responsibilities**:
- Analyze page state
- Identify ATS systems
- Direct External Applicant
- Handle edge cases

### External Applicant Agent
**File**: `agents/external_applicant.md`
**Role**: Execute external site actions
**Trigger**: Director instructions
**Responsibilities**:
- Navigate external sites
- Fill forms as directed
- Report results

### Supporting Agents
- **CSV Tracker**: Data persistence
- **Search Logger**: Session logging
- **Application Tracker**: Per-application logs
- **Question Tracker**: Question database
- **Performance Monitor**: Timing and stuck detection
- **Search Strategist**: Planning

---

## Common Agent Patterns

### Supervisor-Worker
One agent oversees others:
```
[Supervisor]
    ├── [Worker 1]
    ├── [Worker 2]
    └── [Worker 3]
```

### Pipeline
Agents in sequence:
```
[Agent A] → [Agent B] → [Agent C]
```

### Event-Driven
Agents react to events:
```
[Event] → [Interested Agents Subscribe]
```

---

## Agent Communication

Agents communicate through:
1. **Signals**: One agent notifies another
2. **Shared State**: Files both can read/write
3. **Tool Calls**: Using shared tools
4. **Turn Taking**: Explicit handoffs

---

## Design Principles

1. **Single Responsibility**: Each agent has one job
2. **Clear Interfaces**: Well-defined inputs/outputs
3. **Failure Isolation**: One agent's failure doesn't cascade
4. **Stateless Preference**: Minimize state within agents
5. **Explicit Communication**: Clear handoffs and signals

