# State Recovery Patterns

## Overview
Patterns for recovering from failures and maintaining consistent state.

---

## Pattern 1: Write-Ahead Logging

### Description
Before making changes, log the intended change. If crash occurs, replay the log.

### Application
```
1. Write to intent log: "About to apply to job X"
2. Perform application
3. Write to CSV
4. Mark intent as complete
```

### Recovery
On startup, check for incomplete intents and either complete or rollback.

### Applicability
Medium — Adds complexity, may be overkill for current needs

---

## Pattern 2: Checkpoint-Based Recovery

### Description
Periodically save complete state snapshots. On crash, restore from last checkpoint.

### Application
```
After every N applications:
1. Save current search plan progress
2. Save application count
3. Save current position in job list
```

### Recovery
On startup, load last checkpoint and resume from there.

### Applicability
High — Simple and effective for our use case

---

## Pattern 3: Idempotent Operations

### Description
Design operations so running them twice has the same effect as running once.

### Application
- Before applying, check if already applied (via CSV or "Applied" badge)
- Before logging, check if log entry exists
- Before writing file, check if content already matches

### Benefits
- Safe to retry on failure
- No duplicate entries
- Simpler recovery

### Applicability
High — Essential for reliability

---

## Pattern 4: Atomic File Updates

### Description
Instead of modifying files in place, write to temp file and rename.

### Application
```
1. Write CSV update to applications.csv.tmp
2. Verify write succeeded
3. Rename applications.csv.tmp to applications.csv
```

### Benefits
- Crash during write doesn't corrupt main file
- Always have complete, valid file

### Applicability
High — Should implement for CSV updates

---

## Pattern 5: State as Events

### Description
Store events (what happened) rather than current state. Derive state from events.

### Application
```
Events:
- ApplicationStarted(job_id, timestamp)
- ApplicationCompleted(job_id, timestamp)
- ApplicationFailed(job_id, reason, timestamp)

State derived by replaying events.
```

### Benefits
- Full audit trail
- Can reconstruct any point in time
- Naturally idempotent

### Applicability
Medium — More complex, but powerful for debugging

---

## Current System Gaps

### Gap 1: No Mid-Application Recovery
**Current**: If crash during application, no record
**Fix**: Log intent before starting, mark complete after

### Gap 2: Non-Atomic CSV Writes
**Current**: Direct file writes
**Fix**: Write to temp file, then rename

### Gap 3: No Checkpoint of Progress
**Current**: Lose position on crash
**Fix**: Save position after each application

### Gap 4: Duplicate Detection
**Current**: May re-apply to same job
**Fix**: Check CSV before applying

---

## Recommended Implementation

### Immediate (Low Effort)
1. Check for duplicate applications before applying
2. Use atomic file writes for CSV

### Short-Term (Medium Effort)
1. Add checkpoint file for session progress
2. Log application intent before starting

### Long-Term (Higher Effort)
1. Consider event sourcing for complete audit trail

