# Subcommittee Charter: Browser Automation & Stealth

## Identity
| Field | Value |
|-------|-------|
| **Number** | 03 |
| **Name** | Browser Automation & Stealth |
| **Chair** | "Shadow" (Anonymous) |
| **Category** | Technical |
| **Members** | 12 |

---

## Purpose

The Browser Automation & Stealth Subcommittee advises on all matters relating to controlling web browsers programmatically while evading detection as automation. This is one of the most critical subcommittees given the high risk of account suspension.

---

## Scope

### In Scope
- Browser fingerprinting and evasion
- Automation detection vectors
- Rate limiting and throttling
- Behavioral signature masking
- Human-like timing patterns
- Selenium/Playwright best practices
- Proxy and IP management
- Cookie and session handling
- LinkedIn-specific detection
- ATS-specific detection

### Out of Scope
- Agent design (→ Agent Architecture)
- Application form content (→ ATS Systems)
- Ethical considerations (→ Ethics & Compliance)

---

## Key Questions We Address

1. How does LinkedIn detect automation?
2. What fingerprinting techniques are used against us?
3. How do we make automated behavior appear human?
4. What timing patterns are safe?
5. How do we handle rate limiting?
6. What are the risks of specific approaches?

---

## Current System Context

The system currently:
- Uses Cursor's browser extension (MCP tools)
- Operates a single browser session
- Uses default timing/delays
- Does not actively evade fingerprinting
- Has unknown detection exposure

Risks:
- LinkedIn account suspension
- IP blocking
- Permanent bans
- Loss of application history

---

## Archetype Distribution

| Archetype | Members | Names |
|-----------|---------|-------|
| Skeptic/Paranoid | 5 | Shadow, Zara Chen, Hassan Al-Rashid, Claire DuPont, Oleg Petrov |
| Insider | 2 | Declan Murphy (ex-anti-fraud), Marcus "Ghost" Webb (proxy networks) |
| Academic | 2 | Dr. Mikhail Volkov, Dr. Amanda Foster |
| Practitioner | 3 | Rex Drummond, Yuki Nakamura, Samira Patel |

---

## Meeting Triggers

This subcommittee should be called when:
- Considering any change to browser automation
- Evaluating detection risk of new features
- After any suspicious account behavior
- Before increasing automation speed/volume
- When adding parallel browser sessions
- Reviewing anti-detection strategies

---

## Relationships to Other Subcommittees

| Subcommittee | Relationship |
|--------------|--------------|
| Agent Architecture | Browser actions come from agents |
| Concurrency | More parallelism = more detection risk |
| Anti-Detection | We share detection concerns; they focus on LinkedIn-specific |
| Performance | Speed increases detection risk |
| Ethics & Compliance | ToS implications of evasion |
| Red Team | They test our stealth |

---

## Classification: SENSITIVE

This subcommittee's deliberations and knowledge may contain techniques that should not be widely shared. Knowledge base entries should be reviewed for sensitivity.

