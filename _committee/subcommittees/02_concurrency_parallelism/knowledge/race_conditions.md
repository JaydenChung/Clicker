# Race Conditions in Job Application Automation

## Overview
This document catalogs potential race conditions in the automation system.

---

## Known Race Condition Risks

### 1. CSV File Access
**Risk**: Multiple agents writing to applications.csv simultaneously
**Impact**: Data corruption, lost entries
**Current Mitigation**: Sequential operation (one at a time)
**Recommendation**: File locking or single-writer pattern

### 2. Browser State
**Risk**: One agent reading browser state while another modifies it
**Impact**: Stale data, incorrect actions
**Current Mitigation**: Single browser session
**Recommendation**: If parallelizing, use separate browser contexts

### 3. Session Logs
**Risk**: Multiple agents appending to same log file
**Impact**: Interleaved/corrupted logs
**Current Mitigation**: Sequential logging
**Recommendation**: Per-agent log files or message queue

### 4. Application Counter
**Risk**: Multiple agents incrementing application count
**Impact**: Incorrect count, exceeding limits
**Current Mitigation**: Single agent applies
**Recommendation**: Atomic counter operations

### 5. Search Plan State
**Risk**: Multiple agents marking searches as complete
**Impact**: Duplicate work, skipped searches
**Current Mitigation**: Sequential searches
**Recommendation**: Lock on plan modification or atomic updates

---

## Patterns to Prevent Races

### Single Writer Principle
- Only one agent writes to any given resource
- Others read or request writes via messages

### Immutable State
- Don't modify shared state; create new versions
- Pass new state to dependent agents

### Message Passing
- Agents communicate via messages, not shared state
- Each agent owns its own state

### Optimistic Locking
- Read version, make changes, write with version check
- Retry if version changed

---

## Analysis Framework

When evaluating parallelism proposals:

1. **Identify shared resources**
   - Files, browser state, counters, UI elements

2. **For each shared resource**
   - Who reads? Who writes?
   - What happens if concurrent access?
   - Can we eliminate sharing?

3. **If sharing unavoidable**
   - What synchronization is needed?
   - What's the deadlock risk?
   - What's the performance impact?

