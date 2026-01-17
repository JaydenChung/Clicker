# Session Stop Log

This log tracks **every time an application session stops** and the reason why. This is critical for improving the system and understanding blockers.

---

## 🚨 WHY THIS LOG EXISTS

The autonomous applicant should run until:
- All planned applications are done
- Context window is nearly full
- User manually stops it

**A session should NEVER stop because:**
- A job seemed like a bad fit
- Experience requirements didn't match
- Salary was outside range
- Any other "quality" judgment

If a suboptimal job is encountered, **complete it and continue**.

---

## Session Stop Categories

### ✅ COMPLETED
Session finished naturally - all planned applications submitted or search exhausted.

### ⏸️ SOFT BLOCKER (Continue Session, Leave Tab Open)
Blockers that require human intervention but should NOT end the session:
- Email verification required
- Phone verification required
- Account creation requires email confirmation
- Multi-factor authentication
- "We'll contact you" confirmation pages

**Action**: Log → Leave tab open → Return to LinkedIn → Continue applying to other jobs

### 🛑 HARD BLOCKER (Skip Application, Continue Session)
Blockers that prevent completing ONE application but session continues:
- CAPTCHA requiring human intervention
- Mandatory assessment/test required
- Video interview scheduling required
- Broken/non-functional form

**Action**: Log → Skip this job → Continue with next job

### ⚠️ SYSTEM LIMIT
Technical limitations that end the session:
- Context window approaching limit (>80%)
- Rate limiting detected
- Browser disconnected
- Error cascade (3+ consecutive failures)

### 🚫 USER INTERRUPT
User manually stopped the session.

---

## Session Stop Log

<!-- Add entries below as sessions end -->

### Template

```markdown
### [DATE] - Session [#] ([Type: Easy Apply / External])

| Time | Company | Job Title | Stop Type | Reason | Tab Left Open | Resume Action |
|------|---------|-----------|-----------|--------|---------------|---------------|
| HH:MM | [Company] | [Title] | [Category] | [Details] | ✅/❌ | [What to do] |

**Session Status**: [COMPLETED / PAUSED / ENDED]
**Applications Attempted**: X
**Applications Completed**: X
**Applications Pending Manual**: X
**Applications Skipped**: X

**Stop Reason**: [Detailed explanation]

**Notes**:
- [Any additional context for future improvement]
```

---

## Soft Blocker Resolution Checklist

When returning to complete a soft-blocked application:

- [ ] Switch to the left-open tab
- [ ] Complete the verification step
- [ ] Submit the application
- [ ] Update `applications.csv` status from "Pending Manual" to "Applied"
- [ ] Update the application log with resolution
- [ ] Mark entry in this log as resolved

