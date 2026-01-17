# Plan Search Command

Execute the **Search Strategist Agent** workflow.

---

## ⚡ AGENTS TO ACTIVATE

1. **Search Strategist** (`agents/search_strategist.md`) - Primary for this command

**READ THE AGENT FILE BEFORE STARTING.**

---

## Files to Read FIRST

```
data/applications.csv         - Application history (if exists)
config/job_preferences.md     - Keywords to search
config/locations.md           - Locations to search
logs/sessions/                - Recent session logs (for patterns)
agents/search_strategist.md   - Strategist instructions
```

---

## Execution Flow

### 1. Load All Data

1. Read `data/applications.csv` - Parse all past applications
2. Read `config/job_preferences.md` - Get keyword list
3. Read `config/locations.md` - Get location list
4. Scan `logs/sessions/` - Get recent activity

### 2. Analyze Saturation

For each (keyword, location) combination:
- Count existing applications
- Calculate days since last search
- Identify saturation level:
  - 🔴 **Saturated** (50+ apps): Skip or low priority
  - 🟡 **Moderate** (20-49 apps): Medium priority
  - 🟢 **Fresh** (0-19 apps): High priority

### 3. Generate Priority Score

Score = (Freshness × 40%) + (Recency × 30%) + (Preference × 30%)

Where:
- Freshness: Lower application count = higher score
- Recency: More days since last search = higher score  
- Preference: User's keyword/location priority

### 4. Create Search Plan

Generate `data/current_search_plan.md`:

```markdown
# Current Search Plan

**Generated**: YYYY-MM-DD HH:MM
**Based on**: XXX total applications

---

## Priority Search Queue

| Priority | Keyword | Location | Apps | Last Searched | Score |
|----------|---------|----------|------|---------------|-------|
| 1 | [keyword] | [location] | X | X days ago | XX |
| 2 | [keyword] | [location] | X | X days ago | XX |
...

---

## Skip List (Saturated)

| Keyword | Location | Apps | Reason |
|---------|----------|------|--------|
| [keyword] | [location] | 50+ | Saturated |
...

---

## Session Recommendation

- **Target Applications**: 15-20
- **Estimated Searches**: 3-4
- **Focus Areas**: [top locations]
- **Avoid**: [saturated areas]
```

### 5. Display Report

Output a visual report:

```
📊 SEARCH STRATEGY REPORT
━━━━━━━━━━━━━━━━━━━━━━━━

📈 APPLICATION DISTRIBUTION

By Location:
  Los Angeles      ████████████ 45
  San Francisco    ██████████   38
  San Jose         ████████     28
  Remote           ██████       22

By Keyword:
  Product Manager  ████████████████ 62
  Solutions        ████████████     45
  Engineer         ████████         30

🎯 RECOMMENDED SEARCH ORDER

1. 🟢 Solutions + San Jose (8 apps, 5 days ago)
2. 🟢 Engineer + Los Angeles (12 apps, 3 days ago)  
3. 🟡 Product Manager + Remote (25 apps, 2 days ago)
4. 🔴 SKIP: Product Manager + LA (52 apps - saturated)

💡 SESSION TARGET
- Apply to 15-20 jobs
- Focus on San Jose and Engineer roles
- Avoid Product Manager in LA (saturated)

Ready to apply? Run: /apply-jobs
```

---

## Output Files

| File | Content |
|------|---------|
| `data/current_search_plan.md` | The search plan |
| `data/search_insights.md` | Patterns and learnings (append) |

---

## Notes

- Run this BEFORE `/apply-jobs`
- Re-run after each session to get updated strategy
- Plan is based on actual application data
