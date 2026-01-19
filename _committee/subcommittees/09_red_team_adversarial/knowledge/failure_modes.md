# Failure Mode Catalog

## Overview
This document catalogs known and potential failure modes for the job application automation system.

---

## Category 1: Detection Failures

### FM-1.1: Account Suspension
**Description**: LinkedIn detects automation and suspends account
**Likelihood**: Medium-High
**Impact**: Critical — loss of all progress, potential permanent ban
**Triggers**: Too many applications, pattern detection, rate violations
**Mitigation**: Rate limiting, human-like timing, detection evasion

### FM-1.2: IP Blocking
**Description**: IP address blocked by LinkedIn or ATS
**Likelihood**: Low-Medium
**Impact**: High — all access blocked
**Triggers**: Suspicious traffic patterns, known datacenter IP
**Mitigation**: Residential IP, proxy rotation

### FM-1.3: Captcha Triggered
**Description**: CAPTCHA challenge blocks progress
**Likelihood**: Medium
**Impact**: Medium — application blocked, but can continue with others
**Triggers**: Suspicious behavior, rate limits, IP reputation
**Mitigation**: Human intervention, skip and continue

---

## Category 2: State Failures

### FM-2.1: Data Corruption
**Description**: CSV or other data files become corrupted
**Likelihood**: Low
**Impact**: High — loss of application history
**Triggers**: Crash during write, concurrent access
**Mitigation**: Atomic writes, backups, write-ahead logging

### FM-2.2: State Desynchronization
**Description**: System state doesn't match reality
**Likelihood**: Medium
**Impact**: Medium — duplicate applications, missed jobs
**Triggers**: Crash, partial completion, browser state mismatch
**Mitigation**: Checkpointing, verification, idempotency

### FM-2.3: Lost Progress
**Description**: Progress lost after crash or interruption
**Likelihood**: Medium
**Impact**: Medium — repeated work
**Triggers**: Crash, power loss, user interrupt
**Mitigation**: Frequent checkpointing, session recovery

---

## Category 3: ATS Failures

### FM-3.1: Unknown Form Field
**Description**: Encounter field that can't be mapped to profile
**Likelihood**: High
**Impact**: Low-Medium — application blocked or incomplete
**Triggers**: Unusual questions, custom fields
**Mitigation**: Fallback strategies, skip optional, flag for human

### FM-3.2: Resume Upload Failure
**Description**: Resume fails to upload or parse
**Likelihood**: Medium
**Impact**: Medium — application incomplete
**Triggers**: File format issues, size limits, network timeout
**Mitigation**: Retry logic, format fallbacks

### FM-3.3: Multi-Page Navigation Failure
**Description**: Lost in multi-page wizard, can't find next step
**Likelihood**: Medium
**Impact**: Medium — application abandoned
**Triggers**: Unexpected page structure, AJAX issues
**Mitigation**: State tracking, timeout detection

---

## Category 4: Browser Failures

### FM-4.1: Browser Crash
**Description**: Browser process crashes
**Likelihood**: Low
**Impact**: High — session lost
**Triggers**: Memory leak, resource exhaustion
**Mitigation**: Browser restart, session recovery

### FM-4.2: Element Not Found
**Description**: Expected element missing from page
**Likelihood**: High
**Impact**: Low — action fails
**Triggers**: Page changes, timing issues, wrong selector
**Mitigation**: Multiple selectors, retry with wait

### FM-4.3: Stale Element
**Description**: Element reference no longer valid
**Likelihood**: Medium
**Impact**: Low — action fails
**Triggers**: Page reload, dynamic content
**Mitigation**: Re-fetch element before action

---

## Category 5: Network Failures

### FM-5.1: Connection Timeout
**Description**: Network request times out
**Likelihood**: Low-Medium
**Impact**: Low — action fails
**Triggers**: Slow network, server issues
**Mitigation**: Retry with exponential backoff

### FM-5.2: Rate Limiting
**Description**: Too many requests, server rejects
**Likelihood**: Medium
**Impact**: Medium — temporarily blocked
**Triggers**: Too fast, too many requests
**Mitigation**: Rate limiting, backoff

---

## Failure Severity Matrix

| Failure | Likelihood | Impact | Risk Score | Priority |
|---------|------------|--------|------------|----------|
| Account Suspension | Medium-High | Critical | Critical | P0 |
| Data Corruption | Low | High | Medium | P1 |
| Unknown Form Field | High | Low-Medium | Medium | P2 |
| Browser Crash | Low | High | Medium | P2 |
| State Desync | Medium | Medium | Medium | P2 |
| Connection Timeout | Low-Medium | Low | Low | P3 |

---

## Red Team Recommendations

1. **P0: Detection Prevention**
   - Implement detection countermeasures before increasing volume
   - Add monitoring for suspension indicators

2. **P1: Data Protection**
   - Implement atomic CSV writes immediately
   - Add periodic backups

3. **P2: Resilience**
   - Add retry logic with backoff
   - Implement session recovery
   - Improve element finding strategies

