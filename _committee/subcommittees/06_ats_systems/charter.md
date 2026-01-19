# Subcommittee Charter: ATS Systems

## Identity
| Field | Value |
|-------|-------|
| **Number** | 06 |
| **Name** | ATS Systems |
| **Chair** | Jennifer Walsh |
| **Category** | Domain |
| **Members** | 11 |

---

## Purpose

The ATS Systems Subcommittee advises on all matters relating to Applicant Tracking Systems — the software platforms that companies use to manage job applications. This includes understanding how different ATS systems work, their quirks, and how to effectively navigate them.

---

## Scope

### In Scope
- Workday, Greenhouse, Lever, Taleo, iCIMS analysis
- Form field mapping and handling
- ATS-specific quirks and workarounds
- Application parsing and processing
- Multi-page form navigation
- ATS detection and identification
- Resume upload handling by ATS

### Out of Scope
- Browser automation mechanics (→ Browser Stealth)
- General form handling patterns (→ Agent Architecture)
- Resume content optimization (→ Resume Optimization)

---

## Key Questions We Address

1. How does [specific ATS] structure its application flow?
2. What are the common fields and how should we handle them?
3. What quirks does [ATS] have that we need to handle?
4. How do we detect which ATS we're on?
5. What's the best strategy for [ATS]-specific challenges?

---

## ATS Coverage

| ATS | URL Pattern | Complexity | Expert |
|-----|-------------|------------|--------|
| Workday | `*.myworkdayjobs.com` | High | Tanya Volkov |
| Greenhouse | `boards.greenhouse.io` | Low | Maria Santos |
| Lever | `jobs.lever.co` | Low | Kevin O'Neill |
| Taleo | `*.taleo.net` | High | Ananya Sharma |
| iCIMS | `careers-*.icims.com` | Medium | Brandon Lee |
| Ashby | `jobs.ashbyhq.com` | Low | Kevin O'Neill |
| SmartRecruiters | `jobs.smartrecruiters.com` | Medium | Brandon Lee |

---

## Archetype Distribution

| Archetype | Members | Names |
|-----------|---------|-------|
| Insider | 2 | Jennifer Walsh (ex-Workday), Tanya Volkov |
| Skeptic | 1 | Greg Simmons |
| Academic | 1 | Dr. Fatima Al-Hassan |
| Practitioner | 7 | Dr. David Park, Maria Santos, Kevin O'Neill, Ananya Sharma, Brandon Lee, Ryan Thompson, Michelle Chen |

---

## Meeting Triggers

This subcommittee should be called when:
- Encountering new ATS systems
- Debugging ATS-specific issues
- Designing ATS detection logic
- Handling unusual form fields
- Planning support for new ATS platforms

