"""
Resume Tailor Agent

This agent creates tailored LaTeX resumes based on JD analysis and candidate content.
Each call uses a FRESH LLM context for consistent quality.

Uses the XYZ formula: "Accomplished [X] as measured by [Y], by doing [Z]"

Input: JD analysis, candidate content pool, LaTeX template
Output: Complete, compilable LaTeX resume
"""

import json
from typing import Optional

from .llm_client import call_llm, get_available_provider

# System prompt for resume tailoring (based on recruiter persona)
RESUME_TAILOR_SYSTEM_PROMPT = """You are a Senior Technical Recruiter & ATS Optimization Expert.

Your task is to generate a complete, ready-to-compile LaTeX resume tailored for a specific job description.

## Your Process

1. **Analyze the JD requirements** - keywords, skills, technologies
2. **Select relevant experiences** - Match candidate's experiences to JD requirements
3. **Rewrite bullet points** - Use XYZ formula with JD keywords naturally integrated
4. **Prioritize content** - Most relevant experiences first
5. **Ensure ATS optimization** - Keywords appear naturally, standard formatting

## The XYZ Formula (Google Standard)
Every bullet point should follow: "Accomplished [X] as measured by [Y], by doing [Z]."

Example:
- Before: "Worked on a mobile app using React Native"
- After: "Accomplished 37% reduction in app memory usage as measured by profiling tools, by developing a React Native mobile app with backend deployed on cloud infrastructure"

## Keyword Injection Rules
- Use EXACT phrases from the JD when possible
- Integrate keywords naturally into experience sections
- Match JD terminology exactly (e.g., if JD says "cross-functional collaboration", use that exact phrase)
- Never fabricate - only use candidate's actual tech stack and experiences

## Critical Rules
✅ Output ONLY the complete LaTeX code - no explanations
✅ Use the exact template structure provided
✅ Keep to 1 page maximum
✅ Use XYZ formula for bullet points
✅ Inject JD keywords naturally
✅ Ensure LaTeX compiles with no errors
✅ Properly escape special characters ($, %, &, #, _, {, }, ~, ^, \\)
❌ Never fabricate experiences or technologies
❌ Never include explanations in output
❌ Never output incomplete LaTeX code
❌ Never exceed 1 page

## LaTeX Output Requirements
- Start with \\documentclass
- Include all necessary packages
- Define all custom commands before use
- End with \\end{document}
- Use standard packages available on any LaTeX distribution"""


def tailor_resume(
    jd_analysis: dict,
    content_pool: dict,
    latex_template: str = "",
    previous_feedback: str = ""
) -> str:
    """
    Create a tailored LaTeX resume for a specific job.
    
    Args:
        jd_analysis: Structured JD analysis from jd_analyzer
        content_pool: Dict with resume_content, projects, personal_profile
        latex_template: Base LaTeX template to use
        previous_feedback: Feedback from previous scoring iteration
    
    Returns:
        Complete LaTeX resume code
    """
    provider = get_available_provider()
    
    if provider == "none":
        print("  ⚠️  No LLM API available, using fallback")
        return _fallback_tailor(content_pool, latex_template)
    
    # Build the user prompt
    user_prompt = f"""Create a tailored LaTeX resume for this job.

## JD ANALYSIS
```json
{json.dumps(jd_analysis, indent=2)}
```

## CANDIDATE EXPERIENCES AND CONTENT
{content_pool.get('resume_content', '')}

## CANDIDATE PROJECTS
{content_pool.get('projects', '')}

## BASE LATEX TEMPLATE (for reference - use this structure)
```latex
{latex_template[:3000] if latex_template else 'Use standard LaTeX resume template'}
```
"""
    
    if previous_feedback:
        user_prompt += f"""

## FEEDBACK FROM PREVIOUS ITERATION (IMPORTANT - Address these issues)
{previous_feedback}
"""
    
    user_prompt += """

## INSTRUCTIONS
Generate a complete, compilable LaTeX resume that:
1. Targets the specific job requirements from the JD analysis
2. Uses the candidate's actual experiences and projects
3. Incorporates ATS keywords from the JD naturally
4. Uses the XYZ formula for achievement bullets
5. Fits on 1 page

Output ONLY the complete LaTeX code. Start with \\documentclass and end with \\end{document}."""

    try:
        response = call_llm(
            system_prompt=RESUME_TAILOR_SYSTEM_PROMPT,
            user_prompt=user_prompt,
            max_tokens=8000
        )
        
        latex_code = response.strip()
        
        # Clean up potential markdown code blocks
        if latex_code.startswith("```"):
            lines = latex_code.split("\n")
            # Remove first line (```latex) and last line (```)
            if lines[0].startswith("```"):
                lines = lines[1:]
            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]
            latex_code = "\n".join(lines)
        
        return latex_code
        
    except Exception as e:
        print(f"  ⚠️  Resume tailoring error: {e}")
        return _fallback_tailor(content_pool, latex_template)


def _fallback_tailor(content_pool: dict, latex_template: str) -> str:
    """
    Return template as-is when API is unavailable.
    """
    if latex_template:
        return latex_template
    
    # Minimal fallback template
    return r"""
\documentclass[letterpaper,11pt]{article}
\usepackage[empty]{fullpage}
\usepackage{titlesec}
\usepackage{enumitem}
\usepackage[hidelinks]{hyperref}

\addtolength{\oddsidemargin}{-0.5in}
\addtolength{\evensidemargin}{-0.5in}
\addtolength{\textwidth}{1in}
\addtolength{\topmargin}{-.5in}
\addtolength{\textheight}{1.0in}

\begin{document}

\begin{center}
\textbf{\Huge Resume} \\
\small Tailored resume generation requires API key
\end{center}

\section*{Note}
This is a fallback template. Set GOOGLE\_API\_KEY environment variable to enable AI-powered resume tailoring.

\end{document}
"""


if __name__ == "__main__":
    print(f"Using provider: {get_available_provider()}")
    
    # Test the tailor
    test_jd_analysis = {
        "job_title": "Software Engineer",
        "company": "TechCorp",
        "required_skills": ["Python", "AWS", "Docker"],
        "keywords": ["cloud platform", "microservices", "agile"]
    }
    
    test_content = {
        "resume_content": "Sample resume content...",
        "projects": "Sample projects..."
    }
    
    result = tailor_resume(test_jd_analysis, test_content)
    print(result[:500])
