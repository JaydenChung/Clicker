# Plan Search Command

Execute the Search Strategist Agent workflow.

## Instructions

1. Read the application history from `data/applications.csv`
2. Read job preferences from `config/job_preferences.md`
3. Read target locations from `config/locations.md`
4. Analyze saturation by keyword + location combination
5. Generate a prioritized search plan
6. Save the plan to `data/current_search_plan.md`
7. Display the search strategy report showing:
   - Application distribution by location and keyword
   - Recommended search order with priorities
   - Which combinations to skip (saturated)
   - Suggested session target

## Files to Read
- `data/applications.csv` - Application history
- `config/job_preferences.md` - Keywords to search
- `config/locations.md` - Locations to search

## Output
- Update `data/current_search_plan.md` with the new plan
- Display the strategy report to the user

