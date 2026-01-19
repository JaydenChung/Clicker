# ⚖️ DECISION FRAMEWORK

## Principles

1. **Decisions are advisory** — The Human has final authority
2. **Dissent is valued** — Minority opinions are recorded and preserved
3. **Rationale is required** — Decisions without reasoning have no weight
4. **Reversibility matters** — Distinguish reversible from irreversible decisions
5. **History informs** — Past decisions should be consulted

---

## Decision Types

### Type 1: Strategic Decisions
**Scope**: Major architectural direction, fundamental approach changes
**Process**: Full committee deliberation, formal vote
**Documentation**: Full decision record with rationale and dissents
**Examples**:
- Switching from sequential to parallel agent execution
- Adding a new major capability
- Changing the fundamental automation approach

### Type 2: Tactical Decisions
**Scope**: Specific implementation choices, optimization approaches
**Process**: Relevant subcommittee(s), Chair synthesis
**Documentation**: Brief decision record
**Examples**:
- How to handle a specific ATS edge case
- Timing adjustments for rate limiting
- Adding a new question to the profile

### Type 3: Procedural Decisions
**Scope**: How the committee operates
**Process**: Parliamentarian recommendation, Chair approval
**Documentation**: Update to procedures
**Examples**:
- Changing session format
- Adding a new subcommittee
- Modifying speaking protocol

---

## Decision Process

### Step 1: Frame the Question
```
CHAIR: "The question before us is: [Specific question]

This is a [Type 1/2/3] decision.

Relevant subcommittees: [List]

Let's hear perspectives."
```

### Step 2: Gather Perspectives
- Relevant subcommittee chairs speak
- Skeptics and critics challenge
- Historians provide context
- Human provides direction

### Step 3: Identify Options
```
CHAIR: "I'm hearing the following options:

Option A: [Description]
  - Advocates: [Members]
  - Rationale: [Key points]

Option B: [Description]
  - Advocates: [Members]
  - Rationale: [Key points]

Option C: [Description]
  - Advocates: [Members]
  - Rationale: [Key points]

Are there other options we should consider?"
```

### Step 4: Deliberate Trade-offs
- What are the risks of each option?
- What are the benefits?
- What's reversible vs. irreversible?
- What does history suggest?

### Step 5: Sense of the Committee
```
CHAIR: "Let me take the sense of the committee.

On the question of [question]:

Those favoring Option A?"
[Members respond]

"Those favoring Option B?"
[Members respond]

"Those favoring Option C?"
[Members respond]

"Abstentions?"
[Members respond]

"The sense of the committee is [conclusion]."
```

### Step 6: Record Decision
```
CHAIR: "Secretary, please record.

DECISION [#]: [Brief title]
QUESTION: [What was decided]
DECISION: [What we decided]
RATIONALE: [Why]
DISSENTS: [Any formal dissents]
ACTION ITEMS: [What follows]"
```

---

## Dissent Process

### Registering Dissent
```
[MEMBER]: "I wish to formally dissent from this decision."

CHAIR: "Your dissent is recognized. Please state it for the record."

[MEMBER]: "I dissent because [reasoning]. 
My alternative recommendation is [alternative].
I believe this decision will lead to [predicted outcome]."

CHAIR: "Your dissent is recorded. Secretary, please ensure 
this is preserved in the decision record and the dissents archive."
```

### Value of Dissent
- Dissents are not failures — they're valuable records
- Dissenting opinions may prove correct over time
- They provide alternatives if the decision fails
- They document the full range of thinking

---

## Decision Record Template

```markdown
# Decision Record: [DECISION-YYYY-MM-DD-###]

## Summary
**Decision**: [One-line summary]
**Date**: [Date]
**Session**: [Session ID]
**Type**: [Strategic/Tactical/Procedural]

## Question
[The specific question that was addressed]

## Context
[Background and why this decision was needed]

## Options Considered

### Option A: [Name]
- Description: [What this option entails]
- Advocates: [Who supported this]
- Pros: [Benefits]
- Cons: [Drawbacks]

### Option B: [Name]
- Description: [What this option entails]
- Advocates: [Who supported this]
- Pros: [Benefits]
- Cons: [Drawbacks]

[Additional options as needed]

## Decision
[What was decided and why]

## Rationale
[Detailed reasoning behind the decision]

## Dissenting Opinions

### [Member Name]
[Their dissent and reasoning]

## Implications
[What this decision means for the system]

## Action Items
| Item | Owner | Due |
|------|-------|-----|
| [Action] | [Member] | [Date] |

## Review Date
[When this decision should be revisited, if applicable]
```

---

## Decision Governance

### Who Can Decide What

| Decision Type | Authority |
|---------------|-----------|
| Strategic | Human (advised by full committee) |
| Tactical | Chair (advised by relevant subcommittees) |
| Procedural | Parliamentarian (with Chair approval) |

### Decision Escalation
- If subcommittee cannot reach consensus → Escalate to full committee
- If committee cannot reach consensus → Present options to Human
- If decision has major implications → Require Human approval

### Decision Review
- Strategic decisions reviewed quarterly
- Tactical decisions reviewed when relevant
- Any member may request decision review

---

## Quick Decision Protocol

For time-sensitive tactical decisions:
```
CHAIR: "This requires a quick decision. 

Question: [Question]
Recommendation: [What Chair recommends]
Rationale: [Brief reasoning]

Any objections? [Pause]

Hearing none, we proceed with [decision]. 
Secretary, record as expedited decision."
```

If objection raised:
```
[MEMBER]: "I object. [Reason]"

CHAIR: "Objection noted. We'll take 5 minutes to discuss 
before deciding."
```

