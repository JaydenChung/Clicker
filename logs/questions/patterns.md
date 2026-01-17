# Question Patterns & Variations

**Purpose**: Map different phrasings of the same underlying question

---

## Work Authorization Questions

All of these mean the same thing → Answer: **Yes** (from profile: work_authorization.us_authorized)

- "Are you legally authorized to work in the United States?"
- "Do you have the legal right to work in the US?"
- "US work authorization?"
- "Authorized to work in the United States for any employer?"
- "Are you authorized to work in the U.S.?"
- "Work authorization status"
- "Do you have unrestricted work authorization in the US?"

---

## Sponsorship Questions

All of these mean the same thing → Answer: **No** (from profile: work_authorization.require_sponsorship)

- "Will you now or in the future require sponsorship for employment visa status?"
- "Do you require visa sponsorship?"
- "Sponsorship required?"
- "Will you require sponsorship to work in the US?"
- "Do you need sponsorship for work authorization?"

---

## Experience - Years Questions

Pattern: Contains skill name + "years" or "experience"

| Pattern | Profile Key |
|---------|-------------|
| "Python" + years | experience.python |
| "JavaScript" + years | experience.javascript |
| "React" + years | experience.react |
| "SQL" + years | experience.sql |
| "AWS" + years | experience.aws |
| Total/overall + experience | experience.total |

---

## Availability Questions

| Pattern | Answer |
|---------|--------|
| "start date" | Immediately / 2 weeks |
| "notice period" | 2 weeks |
| "available immediately" | Yes |
| "Pacific time" + "hours" | Yes |

---

## Salary Questions

| Pattern | Profile Key |
|---------|-------------|
| "expected salary" / "desired salary" | salary.desired |
| "minimum salary" | salary.minimum |
| "salary expectations" | salary.desired |
| "compensation expectations" | salary.desired |
| "hourly rate" | salary.hourly |

---

## Yes/No Skill Questions

Pattern: "Do you have experience with X?" or "X experience?"

Default behavior: If skill is in profile Skills section with "Yes", answer "Yes"

| Skill Pattern | Profile Key |
|---------------|-------------|
| "full-stack" / "fullstack" | skills.fullstack |
| "mobile" + "development" | skills.mobile |
| "AI" / "ML" / "machine learning" | skills.ai_ml |
| "cloud" | skills.cloud |
| "leadership" / "management" | skills.leadership |
| "remote work" | skills.remote |

---

## How Matching Works

1. **Exact Match**: Question text matches a known pattern exactly
2. **Keyword Match**: Question contains key terms (e.g., "Python" + "years")
3. **Category Match**: Question fits a known category (e.g., any sponsorship question)
4. **Fuzzy Match**: Similar phrasing to known questions

---

## Adding New Patterns

When a new question variation is encountered:

1. Add it to the appropriate category above
2. Map it to the correct profile key
3. The system will use this mapping in future sessions

---

## Unknown Patterns

Questions that don't match any pattern are logged to `unanswered.md` for human review.

Common categories of new questions:
- Company-specific questions
- Role-specific technical questions
- Behavioral/cultural fit questions
- Industry-specific requirements

