# Resume Folder

This folder stores your resume files for reference by the application automation system.

## Structure

```
resume/
├── README.md              # This file
├── Your_Resume.pdf        # Your compiled PDF resume
├── resume.tex             # Main LaTeX file (optional)
├── custom-commands.tex    # LaTeX commands (optional)
└── src/                   # LaTeX source files (optional)
    ├── heading.tex
    ├── experience.tex
    ├── projects.tex
    ├── education.tex
    ├── awards.tex
    └── skills.tex
```

## Usage

### For Easy Apply
Your resume should already be uploaded to LinkedIn. The agent uses the filename from `config/personal_profile.md` → Resume section.

### For External Applications  
The agent may need to upload your PDF. Place your compiled resume PDF in this folder.

### LaTeX Source (Optional)
If you maintain your resume in LaTeX, you can store the source files here for version control and future edits.

## Notes

- The PDF is the primary file used for applications
- LaTeX source is optional but recommended for easy editing
- Update `config/resume_content.md` when you update your resume

