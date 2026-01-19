"""
ATS Scorer Agent

This agent scores tailored resumes against job requirements.
Each call uses a FRESH LLM context for consistent quality.

Input: Tailored resume LaTeX, JD analysis
Output: Score (0-100) and improvement suggestions
"""

import os
import json
from typing import Optional

try:
    import anthropic
    HAS_ANTHROPIC = True
except ImportError:
    HAS_ANTHROPIC = False

# System prompt for ATS scoring
ATS_SCORER_SYSTEM_PROMPT = """You are an expert ATS (Applicant Tracking System) analyzer and resume scorer.

Your task is to score a resume against a job description and provide actionable improvement suggestions.

## Scoring Rubric (Total: 100 points)

### Keyword Match (40 points)
- Count how many JD keywords appear in the resume
- Exact matches score higher than synonyms
- Formula: (keywords_found / total_jd_keywords) * 40

### Skills Match (30 points)
- Required skills present: +6 points each (max 24)
- Preferred skills present: +2 points each (max 6)

### Experience Relevance (20 points)
- Job titles relevance: 0-8 points
- Years of experience match: 0-6 points
- Responsibilities alignment: 0-6 points

### Formatting/Parseability (10 points)
- Standard section headers: +3 points
- Clean formatting (no tables in main content): +3 points
- Contact info present: +2 points
- Consistent date format: +2 points

## Output Format
Output ONLY valid JSON with this exact structure:

{
  "overall_score": <integer 0-100>,
  "keyword_score": <integer 0-100>,
  "skills_score": <integer 0-100>,
  "experience_score": <integer 0-100>,
  "formatting_score": <integer 0-100>,
  "keywords_found": ["list", "of", "found", "keywords"],
  "missing_keywords": ["list", "of", "missing", "important", "keywords"],
  "required_skills_found": ["list"],
  "required_skills_missing": ["list"],
  "suggestions": [
    "Specific actionable suggestion 1",
    "Specific actionable suggestion 2",
    "Specific actionable suggestion 3"
  ],
  "strengths": [
    "What the resume does well 1",
    "What the resume does well 2"
  ],
  "passed": <boolean - true if overall_score >= 90>
}

## Critical Rules
- Be objective and consistent in scoring
- Suggestions must be specific and actionable (e.g., "Add 'Python' to skills section" not "improve skills")
- Look for EXACT keyword matches from the JD
- Consider both technical skills and soft skills
- Output ONLY the JSON - no explanations before or after"""


def score_resume(
    resume_latex: str,
    jd_analysis: dict,
    api_key: Optional[str] = None
) -> dict:
    """
    Score a tailored resume against JD requirements.
    
    Args:
        resume_latex: The tailored resume in LaTeX format
        jd_analysis: Structured JD analysis from jd_analyzer
        api_key: Optional API key (defaults to ANTHROPIC_API_KEY env var)
    
    Returns:
        dict with score breakdown and suggestions
    """
    if not HAS_ANTHROPIC:
        return _fallback_score(resume_latex, jd_analysis)
    
    api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
    
    if not api_key:
        print("  ⚠️  No ANTHROPIC_API_KEY found, using fallback scoring")
        return _fallback_score(resume_latex, jd_analysis)
    
    user_prompt = f"""Score this resume against the job requirements.

## JD ANALYSIS (what the job requires)
```json
{json.dumps(jd_analysis, indent=2)}
```

## RESUME TO SCORE (LaTeX format)
```latex
{resume_latex}
```

Score the resume using the rubric and output ONLY the JSON result."""

    try:
        client = anthropic.Anthropic(api_key=api_key)
        
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2000,
            system=ATS_SCORER_SYSTEM_PROMPT,
            messages=[{
                "role": "user",
                "content": user_prompt
            }]
        )
        
        response_text = response.content[0].text.strip()
        
        # Handle potential markdown code blocks
        if response_text.startswith("```"):
            lines = response_text.split("\n")
            response_text = "\n".join(lines[1:-1])
        
        return json.loads(response_text)
        
    except json.JSONDecodeError as e:
        print(f"  ⚠️  Failed to parse score JSON: {e}")
        return _fallback_score(resume_latex, jd_analysis)
    except Exception as e:
        print(f"  ⚠️  Scoring API error: {e}")
        return _fallback_score(resume_latex, jd_analysis)


def _fallback_score(resume_latex: str, jd_analysis: dict) -> dict:
    """
    Basic keyword counting without API.
    Used as fallback when API is unavailable.
    """
    resume_lower = resume_latex.lower()
    
    # Count keyword matches
    keywords = jd_analysis.get("keywords", []) + jd_analysis.get("ats_keywords", [])
    keywords = list(set(keywords))  # Dedupe
    
    found = [kw for kw in keywords if kw.lower() in resume_lower]
    missing = [kw for kw in keywords if kw.lower() not in resume_lower]
    
    # Simple scoring
    keyword_score = int((len(found) / max(len(keywords), 1)) * 100)
    
    # Check required skills
    required_skills = jd_analysis.get("required_skills", [])
    skills_found = [s for s in required_skills if s.lower() in resume_lower]
    skills_missing = [s for s in required_skills if s.lower() not in resume_lower]
    skills_score = int((len(skills_found) / max(len(required_skills), 1)) * 100)
    
    # Basic formatting check
    formatting_score = 70
    if "\\section" in resume_latex:
        formatting_score += 10
    if "\\begin{document}" in resume_latex and "\\end{document}" in resume_latex:
        formatting_score += 10
    if "@" in resume_latex:  # Likely has email
        formatting_score += 10
    
    overall = int(
        keyword_score * 0.4 +
        skills_score * 0.3 +
        70 * 0.2 +  # Experience score placeholder
        formatting_score * 0.1
    )
    
    return {
        "overall_score": min(overall, 100),
        "keyword_score": keyword_score,
        "skills_score": skills_score,
        "experience_score": 70,
        "formatting_score": formatting_score,
        "keywords_found": found,
        "missing_keywords": missing[:10],
        "required_skills_found": skills_found,
        "required_skills_missing": skills_missing,
        "suggestions": [
            f"Add missing keyword: {missing[0]}" if missing else "Keywords look good",
            f"Add missing skill: {skills_missing[0]}" if skills_missing else "Skills look good",
            "Consider using more quantified achievements"
        ],
        "strengths": [
            f"Found {len(found)}/{len(keywords)} keywords",
            f"Found {len(skills_found)}/{len(required_skills)} required skills"
        ],
        "passed": overall >= 90
    }


if __name__ == "__main__":
    # Test the scorer
    test_resume = r"""
    \documentclass{article}
    \begin{document}
    \section{Skills}
    Python, AWS, Docker, Kubernetes
    \section{Experience}
    Software Engineer - Built cloud platform using Python and AWS
    \end{document}
    """
    
    test_jd = {
        "required_skills": ["Python", "AWS", "Docker"],
        "keywords": ["cloud platform", "microservices", "agile"],
        "ats_keywords": ["python", "aws", "docker", "kubernetes"]
    }
    
    result = score_resume(test_resume, test_jd)
    print(json.dumps(result, indent=2))

