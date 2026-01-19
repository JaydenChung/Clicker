# Browser Automation Detection Vectors

## Overview
This document catalogs known vectors by which automation can be detected.

---

## Category 1: Browser Fingerprinting

### Navigator Properties
- `navigator.webdriver` — Set to true in automated browsers
- `navigator.plugins` — Empty in headless
- `navigator.languages` — Inconsistent with locale

### Canvas Fingerprinting
- Unique rendering of canvas elements
- Automated browsers may have different rendering

### WebGL Fingerprinting
- GPU information leaks
- Consistent across sessions = suspicion

### Audio Fingerprinting
- AudioContext processing
- Different in automation environments

### Font Fingerprinting
- Available fonts enumerated
- Headless has different font list

---

## Category 2: Behavioral Analysis

### Mouse Movement
- Human mice have curves, micro-movements
- Automated = straight lines, perfect paths

### Click Patterns
- Humans click with variable timing
- Automation = precise, uniform

### Typing Patterns
- Human typing has rhythm, errors, variation
- Automation = perfect, uniform speed

### Scroll Behavior
- Humans scroll variably
- Automation = programmatic scrolling

### Page Interaction Time
- Humans take time to read/process
- Automation may skip too fast

---

## Category 3: Network Analysis

### Request Timing
- Human requests are variable
- Automation = regular intervals

### Request Patterns
- Humans browse naturally
- Automation = direct to targets

### TLS Fingerprinting
- Different TLS stacks have signatures
- Headless Chrome has known fingerprint

### IP Reputation
- Datacenter IPs are known
- VPN/proxy IPs are flagged

### Geographic Consistency
- IP location vs. timezone vs. language
- Mismatches are suspicious

---

## Category 4: JavaScript Environment

### Automation Detection Code
```javascript
// Common detection checks
if (navigator.webdriver) // Automation detected
if (window.Cypress) // Testing framework
if (window.__selenium_unwrapped) // Selenium
```

### Honeypots
- Invisible elements that only bots click
- Links hidden with CSS

### Timing APIs
- `performance.now()` precision
- Automation environments may differ

---

## Category 5: LinkedIn-Specific

### Rate Limiting
- Too many actions per time period
- Triggers throttling, then blocking

### Session Behavior
- Normal users have varied sessions
- Automation = same patterns repeatedly

### Application Patterns
- Humans are selective
- Applying to everything = suspicious

### Profile Views vs. Applications
- Humans view multiple, apply to few
- Automation may apply without viewing

---

## Mitigation Strategies

### Fingerprint Spoofing
- Use stealth plugins (puppeteer-extra-plugin-stealth)
- Randomize canvas, WebGL responses

### Behavioral Mimicry
- Add random delays (log-normal distribution)
- Curved mouse paths
- Variable typing speeds

### Network Obfuscation
- Residential proxies
- Consistent IP/location/timezone

### Environment Hardening
- Real browser (not headless)
- Full plugins, fonts, etc.

---

## Current System Assessment

| Vector | Current Status | Risk Level |
|--------|----------------|------------|
| navigator.webdriver | Unknown | High |
| Mouse patterns | Linear | High |
| Timing uniformity | Likely uniform | Medium |
| IP reputation | User's home IP | Low |
| Rate limiting | Manual limits | Medium |
| Behavioral patterns | Unknown | Medium |

**Recommendation**: Conduct detection audit before increasing automation volume.

