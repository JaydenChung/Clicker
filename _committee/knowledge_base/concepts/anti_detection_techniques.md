# Anti-Detection Techniques

## Overview

This document describes techniques for avoiding detection as automation while browsing and applying to jobs.

---

## Detection Vectors

### Browser-Level Detection
- `navigator.webdriver` flag
- Missing plugins/fonts
- Canvas fingerprinting
- WebGL fingerprinting
- Audio fingerprinting

### Behavioral Detection
- Mouse movement patterns
- Click timing uniformity
- Typing patterns
- Scroll behavior
- Page interaction timing

### Network Detection
- Request timing patterns
- TLS fingerprinting
- IP reputation
- Geographic inconsistency

### Platform-Specific Detection
- Rate limit violations
- Unusual access patterns
- Application velocity
- Session characteristics

---

## Countermeasures

### Browser Hardening
- Use real browser (not headless)
- Stealth plugins if using automation library
- Normal user agent
- Full plugin/font set

### Behavioral Mimicry
- **Random delays**: Not uniform timing
  ```
  // Bad: Fixed delay
  await sleep(2000);
  
  // Better: Random delay
  await sleep(1500 + Math.random() * 1500);
  ```
- **Mouse curves**: Not straight lines
- **Variable typing**: Not uniform speed
- **Human-like pauses**: Read time, think time

### Rate Management
- Respect implicit rate limits
- Vary timing between actions
- Take breaks during long sessions
- Monitor for rate limit signals

### Session Management
- Maintain consistent session
- Don't clear cookies unnecessarily
- Keep timezone/location consistent
- Act like returning user

---

## Risk Assessment

### High Risk Actions
- Applying too fast
- Too many applications per day
- Identical behavior patterns
- Running during unusual hours

### Lower Risk Actions
- Human-paced applications
- Varied timing
- Normal browsing hours
- Mixed with real browsing

---

## Monitoring for Detection

### Warning Signs
- Increased CAPTCHAs
- Slower page loads
- Missing search results
- Account restrictions
- Error messages

### Response to Signs
1. Slow down immediately
2. Take longer breaks
3. Review recent patterns
4. Consider IP change
5. Verify account status

---

## Ethical Note

These techniques are for legitimate personal automation. The goal is to apply efficiently, not to circumvent fraud protection. Always respect platform rules within reasonable interpretation.

