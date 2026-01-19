"""
JD Analyzer Agent

This agent analyzes job descriptions and extracts structured data.
Each call uses a FRESH LLM context for consistent quality.

Input: Raw job description text
Output: Structured analysis (keywords, skills, requirements)
"""

import os
import json
from typing import Optional

try:
    import anthropic
    HAS_ANTHROPIC = True
except ImportError:
    HAS_ANTHROPIC = False

# System prompt for JD analysis
JD_ANALYZER_SYSTEM_PROMPT = """You are an expert job description analyzer specializing in ATS (Applicant Tracking System) optimization.

Your task is to analyze a job description and extract structured data that will be used to tailor a resume.

IMPORTANT: Output ONLY valid JSON. No explanations, no markdown, just the JSON object.

Extract the following:

1. **job_title**: The exact job title
2. **company**: Company name
3. **required_skills**: List of explicitly required skills/technologies
4. **preferred_skills**: List of nice-to-have skills
5. **years_experience**: Number of years required (integer, or 0 if not specified)
6. **key_responsibilities**: Main job responsibilities (list of strings)
7. **keywords**: ATS keywords - exact phrases and terms from the JD that should appear in the resume
8. **ats_keywords**: The most important keywords that ATS systems will scan for
9. **tone**: The communication tone (formal, casual, technical, startup)
10. **industry**: The industry/sector
11. **education_required**: Required education level
12. **soft_skills**: Any soft skills mentioned

JSON Schema:
{
  "job_title": "string",
  "company": "string",
  "required_skills": ["string"],
  "preferred_skills": ["string"],
  "years_experience": integer,
  "key_responsibilities": ["string"],
  "keywords": ["string"],
  "ats_keywords": ["string"],
  "tone": "string",
  "industry": "string",
  "education_required": "string",
  "soft_skills": ["string"]
}"""


def analyze_jd(job_description: str, api_key: Optional[str] = None) -> dict:
    """
    Analyze a job description and extract structured data.
    
    Args:
        job_description: Raw job description text
        api_key: Optional API key (defaults to ANTHROPIC_API_KEY env var)
    
    Returns:
        dict with structured JD analysis
    """
    if not HAS_ANTHROPIC:
        # Fallback: basic keyword extraction without API
        return _fallback_analyze(job_description)
    
    api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
    
    if not api_key:
        print("  ⚠️  No ANTHROPIC_API_KEY found, using fallback analysis")
        return _fallback_analyze(job_description)
    
    try:
        client = anthropic.Anthropic(api_key=api_key)
        
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2000,
            system=JD_ANALYZER_SYSTEM_PROMPT,
            messages=[{
                "role": "user",
                "content": f"Analyze this job description:\n\n{job_description}"
            }]
        )
        
        # Extract JSON from response
        response_text = response.content[0].text.strip()
        
        # Handle potential markdown code blocks
        if response_text.startswith("```"):
            lines = response_text.split("\n")
            response_text = "\n".join(lines[1:-1])
        
        return json.loads(response_text)
        
    except json.JSONDecodeError as e:
        print(f"  ⚠️  Failed to parse JD analysis JSON: {e}")
        return _fallback_analyze(job_description)
    except Exception as e:
        print(f"  ⚠️  JD analysis API error: {e}")
        return _fallback_analyze(job_description)


def _fallback_analyze(job_description: str) -> dict:
    """
    Basic keyword extraction without API.
    Used as fallback when API is unavailable.
    """
    jd_lower = job_description.lower()
    
    # Common tech keywords to look for
    tech_keywords = [
        "python", "javascript", "react", "node.js", "typescript", "java", 
        "c++", "c#", "go", "rust", "sql", "nosql", "mongodb", "postgresql",
        "aws", "gcp", "azure", "docker", "kubernetes", "ci/cd", "git",
        "agile", "scrum", "jira", "fastapi", "django", "flask", "express",
        "machine learning", "ai", "data science", "api", "rest", "graphql"
    ]
    
    # Extract found keywords
    found_keywords = [kw for kw in tech_keywords if kw in jd_lower]
    
    # Try to extract years of experience
    import re
    years_match = re.search(r'(\d+)\+?\s*years?', jd_lower)
    years = int(years_match.group(1)) if years_match else 0
    
    return {
        "job_title": "Unknown",
        "company": "Unknown",
        "required_skills": found_keywords[:5],
        "preferred_skills": found_keywords[5:10],
        "years_experience": years,
        "key_responsibilities": [],
        "keywords": found_keywords,
        "ats_keywords": found_keywords[:10],
        "tone": "professional",
        "industry": "technology",
        "education_required": "Bachelor's degree",
        "soft_skills": []
    }


if __name__ == "__main__":
    # Test the analyzer
    test_jd = """
    Software Engineer at TechCorp
    
    We're looking for a skilled Software Engineer with 3+ years of experience
    in Python and JavaScript. You'll be working on our cloud platform using
    AWS, Docker, and Kubernetes. Experience with React and FastAPI is a plus.
    
    Requirements:
    - Strong Python skills
    - Experience with cloud services (AWS preferred)
    - Familiarity with containerization
    - Bachelor's degree in Computer Science
    
    Nice to have:
    - Experience with machine learning
    - Agile development experience
    """
    
    result = analyze_jd(test_jd)
    print(json.dumps(result, indent=2))

