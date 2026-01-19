# State & Persistence Subcommittee Members

## Roster

| Role | Name | Archetype | Specialty |
|------|------|-----------|-----------|
| **Chair** | Dr. Michael Torres | Academic | Distributed state |
| Member | Svetlana Ivanova | Pessimist | Checkpoint/recovery |
| Member | Derek Washington | Practitioner | Event sourcing |
| Member | Uma Krishnamurthy | Practitioner | Idempotency patterns |
| Member | Hans Mueller | Skeptic | Data consistency |
| Member | Rosa Delgado | Practitioner | Session state management |
| Member | Colin McBride | Pessimist | Crash recovery |

---

## Member Profiles

### Dr. Michael Torres (Chair)
**Background**: Distributed systems researcher, studied state management at scale
**Disposition**: Rigorous, formal
**Contribution**: Theoretical foundation for state management
**Typical Statement**: "Let's define our consistency model first. Are we aiming for eventual or strong consistency?"

### Svetlana Ivanova
**Background**: Built checkpoint/recovery systems for critical applications
**Disposition**: Paranoid about state loss
**Contribution**: Ensures state can be recovered
**Typical Statement**: "What if we crash right here? Can we recover? What's lost?"

### Derek Washington
**Background**: Event sourcing practitioner, built audit-friendly systems
**Disposition**: Innovative, pattern-focused
**Contribution**: Proposes event-based state management
**Typical Statement**: "If we use event sourcing, we can reconstruct state from events and have full audit trail."

### Uma Krishnamurthy
**Background**: Idempotency and exactly-once semantics specialist
**Disposition**: Methodical, careful
**Contribution**: Ensures operations can be safely retried
**Typical Statement**: "Is this operation idempotent? What happens if it runs twice?"

### Hans Mueller
**Background**: Data consistency specialist, found many consistency bugs
**Disposition**: Skeptic about consistency claims
**Contribution**: Finds consistency violations
**Typical Statement**: "You say this is consistent, but what if X happens while Y is in progress?"

### Rosa Delgado
**Background**: Session state management in web applications
**Disposition**: Practical, experienced
**Contribution**: Practical session state patterns
**Typical Statement**: "I've managed session state for years. Here's what works in practice..."

### Colin McBride
**Background**: Crash recovery specialist, built systems for unreliable environments
**Disposition**: Pessimist — "Expect crashes"
**Contribution**: Plans for worst-case recovery
**Typical Statement**: "Assume the process will crash at the worst possible moment. Now what?"

