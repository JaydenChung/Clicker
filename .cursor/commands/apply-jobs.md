# Apply to Jobs Command

Execute the Job Applicant Agent workflow for Easy Apply applications.

## Prerequisites
- Browser is open and controlled by Cursor
- LinkedIn is loaded and user is SIGNED IN
- Search plan exists at `data/current_search_plan.md` (run `/plan-search` first if needed)

## Instructions

1. Verify browser is on LinkedIn and signed in
2. Read the search plan from `data/current_search_plan.md`
3. Read personal profile from `config/personal_profile.md`
4. Read resume content from `config/resume_content.md`
5. Create a new session log in `logs/sessions/`
6. Navigate to LinkedIn Jobs if not already there

### For each search in the plan:
1. Enter the keyword in the job search box
2. Enter the location
3. Execute the search
4. For each job with "Easy Apply" button (skip jobs with "Applied" badge):
   - Click on the job listing
   - Click "Easy Apply" button
   - Fill out the application form using personal_profile.md
   - Submit the application
   - Click "Done"
   - Log to `data/applications.csv`
   - Log to `logs/applications/`
5. Mark search as complete in the plan
6. Move to next search

### Session End Triggers
- Context usage exceeds 80%
- Search plan exhausted
- Rate limit detected
- User interrupts

### On Session End
1. Save all data to CSV
2. Finalize all logs
3. Update search plan progress
4. Output session summary with applications count

## Files to Read
- `data/current_search_plan.md` - Search plan
- `config/personal_profile.md` - Personal info for forms
- `config/resume_content.md` - Resume data for questions

## Files to Update
- `data/applications.csv` - Add new applications
- `logs/sessions/session_YYYY-MM-DD_HH-MM.md` - Session log
- `logs/applications/` - Individual application logs
- `logs/questions/unanswered.md` - Questions without answers

