# Apply External Command

Execute the Application Director + External Applicant workflow for non-Easy Apply jobs.

## Prerequisites
- Browser is open and controlled by Cursor
- LinkedIn is loaded and user is SIGNED IN
- Resume PDF available at `resume/` folder for file uploads

## Instructions

1. Activate Application Director (supervisor) and External Applicant (executor) agents
2. Load personal profile from `config/personal_profile.md`
3. Load resume content from `config/resume_content.md`
4. Load projects from `config/projects.md`

### For each non-Easy Apply job:
1. Click "Apply" button on LinkedIn
2. Handle redirect to external site
3. Director analyzes page and identifies ATS system (Workday, Greenhouse, Lever, etc.)

### Page Processing Loop (while not on confirmation page):
1. Director snapshots and analyzes current page
2. Director identifies all form fields
3. For each field:
   - Director provides value/instruction from profile
   - Executor fills the field
   - If open-ended question: Generate response, log to Question Tracker
4. Click Next/Continue/Submit
5. Wait for page load

### Blocker Handling
- Account creation → Create or login if possible
- CAPTCHA → Flag for human, skip job
- File upload → Upload resume from `resume/` folder
- Unknown field → Flag and continue or skip
- Error → Log and attempt recovery

### On Completion
1. Detect confirmation page/message
2. Log to `data/applications.csv` (mark as external)
3. Log to `logs/applications/`
4. Record any flagged questions
5. Return to LinkedIn for next job

## Files to Read
- `config/personal_profile.md` - Personal info
- `config/resume_content.md` - Resume data
- `config/projects.md` - Project portfolio
- `resume/Jayden_APM.pdf` - PDF for file uploads

## Files to Update
- `data/applications.csv` - Add new applications
- `logs/applications/` - Individual application logs
- `logs/questions/unanswered.md` - Flagged questions
- `logs/performance/stuck_log.md` - If stuck events occur

