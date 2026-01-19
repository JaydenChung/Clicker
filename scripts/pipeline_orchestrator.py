#!/usr/bin/env python3
"""
Pipeline Orchestrator - Multi-Agent Resume Tailoring System

This orchestrator runs in the background and coordinates the resume tailoring
pipeline. It watches for job descriptions from Cursor and processes them through
specialized agents with FRESH CONTEXT for each call.

Architecture:
- Cursor Agent: Browser automation (extracts JD, waits, applies)
- This Orchestrator: LLM calls for tailoring/scoring (fresh context each time)
- Communication: File-based message passing via data/pipeline/

Usage:
    python3 scripts/pipeline_orchestrator.py

Requires:
    - ANTHROPIC_API_KEY environment variable
    - pdflatex installed (brew install basictex)
"""

import os
import sys
import json
import time
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Optional

# Add scripts directory to path for agent imports
sys.path.insert(0, str(Path(__file__).parent))

from agents.jd_analyzer import analyze_jd
from agents.resume_tailor import tailor_resume
from agents.ats_scorer import score_resume

# --- Configuration ---
BASE_DIR = Path(__file__).parent.parent
PIPELINE_DIR = BASE_DIR / "data" / "pipeline"
TAILORED_DIR = BASE_DIR / "resume" / "tailored"
LOGS_DIR = BASE_DIR / "logs" / "pipeline"
CONFIG_DIR = BASE_DIR / "config"

# Signal files for communication with Cursor
PENDING_JD_FILE = PIPELINE_DIR / "pending_jd.json"
RESUME_READY_FILE = PIPELINE_DIR / "resume_ready.json"
ORCHESTRATOR_STATUS_FILE = PIPELINE_DIR / "orchestrator_status.json"

# Configuration
MAX_REFINEMENT_ITERATIONS = 3
TARGET_ATS_SCORE = 90
POLL_INTERVAL_SECONDS = 1

# --- Helper Functions ---

def ensure_directories():
    """Create necessary directories if they don't exist."""
    PIPELINE_DIR.mkdir(parents=True, exist_ok=True)
    TAILORED_DIR.mkdir(parents=True, exist_ok=True)
    LOGS_DIR.mkdir(parents=True, exist_ok=True)

def load_content_pool() -> dict:
    """Load all candidate content for resume tailoring."""
    content = {
        "resume_content": "",
        "projects": "",
        "personal_profile": ""
    }
    
    resume_content_path = CONFIG_DIR / "resume_content.md"
    projects_path = CONFIG_DIR / "projects.md"
    personal_profile_path = CONFIG_DIR / "personal_profile.md"
    
    if resume_content_path.exists():
        content["resume_content"] = resume_content_path.read_text()
    
    if projects_path.exists():
        content["projects"] = projects_path.read_text()
    
    if personal_profile_path.exists():
        content["personal_profile"] = personal_profile_path.read_text()
    
    return content

def load_latex_template() -> str:
    """Load the base LaTeX resume template."""
    template_path = BASE_DIR / "resume" / "resume.tex"
    if template_path.exists():
        return template_path.read_text()
    return ""

def compile_latex(tex_file: Path) -> tuple[bool, str]:
    """Compile LaTeX to PDF. Returns (success, error_message)."""
    try:
        result = subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", tex_file.name],
            cwd=tex_file.parent,
            capture_output=True,
            text=True,
            timeout=60
        )
        
        pdf_file = tex_file.with_suffix(".pdf")
        if pdf_file.exists():
            return True, ""
        else:
            return False, result.stdout + result.stderr
    except FileNotFoundError:
        return False, "pdflatex not found. Install with: brew install basictex"
    except subprocess.TimeoutExpired:
        return False, "LaTeX compilation timed out"
    except Exception as e:
        return False, str(e)

def generate_job_id(company: str, job_title: str) -> str:
    """Generate a unique job ID for file naming."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_company = "".join(c if c.isalnum() else "_" for c in company)[:20]
    safe_title = "".join(c if c.isalnum() else "_" for c in job_title)[:20]
    return f"{timestamp}_{safe_company}_{safe_title}"

def log_pipeline_event(event: dict):
    """Log pipeline events for debugging and analytics."""
    event["timestamp"] = datetime.now().isoformat()
    
    log_file = LOGS_DIR / f"pipeline_{datetime.now().strftime('%Y-%m-%d')}.jsonl"
    with open(log_file, "a") as f:
        f.write(json.dumps(event) + "\n")

def update_status(status: str, details: dict = None):
    """Update orchestrator status file for Cursor to read."""
    status_data = {
        "status": status,
        "timestamp": datetime.now().isoformat(),
        "details": details or {}
    }
    ORCHESTRATOR_STATUS_FILE.write_text(json.dumps(status_data, indent=2))

def cleanup_old_signals():
    """Clean up any stale signal files from previous runs."""
    if RESUME_READY_FILE.exists():
        RESUME_READY_FILE.unlink()
    # Don't delete pending_jd - Cursor may have just written it

# --- Main Pipeline ---

def process_job(jd_data: dict, content_pool: dict, latex_template: str) -> dict:
    """
    Process a single job through the full tailoring pipeline.
    Each phase uses a FRESH LLM context for consistent quality.
    
    Returns:
        dict with keys: success, job_id, score, pdf_path, iterations, error
    """
    company = jd_data.get("company", "Unknown")
    job_title = jd_data.get("job_title", "Unknown")
    job_description = jd_data.get("description", "")
    job_url = jd_data.get("job_url", "")
    
    job_id = generate_job_id(company, job_title)
    
    log_pipeline_event({
        "type": "pipeline_started",
        "job_id": job_id,
        "company": company,
        "job_title": job_title
    })
    
    update_status("analyzing", {"job_id": job_id, "phase": "jd_analysis"})
    
    try:
        # === PHASE 1: JD ANALYSIS (Fresh Context) ===
        print(f"  📋 Phase 1: Analyzing JD for {company} - {job_title}")
        
        jd_analysis = analyze_jd(job_description)
        
        log_pipeline_event({
            "type": "jd_analyzed",
            "job_id": job_id,
            "keywords_found": len(jd_analysis.get("keywords", [])),
            "required_skills": jd_analysis.get("required_skills", [])
        })
        
        # Save JD analysis for reference
        analysis_file = TAILORED_DIR / f"{job_id}_jd_analysis.json"
        analysis_file.write_text(json.dumps(jd_analysis, indent=2))
        
        # === PHASE 2 & 3: TAILORING + SCORING LOOP ===
        best_resume = None
        best_score = 0
        feedback = ""
        
        for iteration in range(1, MAX_REFINEMENT_ITERATIONS + 1):
            update_status("tailoring", {
                "job_id": job_id, 
                "phase": "resume_tailoring",
                "iteration": iteration
            })
            
            # === PHASE 2: RESUME TAILORING (Fresh Context) ===
            print(f"  ✏️  Phase 2: Tailoring resume (iteration {iteration})")
            
            tailored_latex = tailor_resume(
                jd_analysis=jd_analysis,
                content_pool=content_pool,
                latex_template=latex_template,
                previous_feedback=feedback
            )
            
            # Save this iteration
            tex_file = TAILORED_DIR / f"{job_id}_v{iteration}.tex"
            tex_file.write_text(tailored_latex)
            
            log_pipeline_event({
                "type": "resume_tailored",
                "job_id": job_id,
                "iteration": iteration
            })
            
            # === PHASE 3: ATS SCORING (Fresh Context) ===
            update_status("scoring", {
                "job_id": job_id,
                "phase": "ats_scoring", 
                "iteration": iteration
            })
            
            print(f"  📊 Phase 3: Scoring resume (iteration {iteration})")
            
            score_result = score_resume(
                resume_latex=tailored_latex,
                jd_analysis=jd_analysis
            )
            
            current_score = score_result.get("overall_score", 0)
            
            log_pipeline_event({
                "type": "resume_scored",
                "job_id": job_id,
                "iteration": iteration,
                "score": current_score,
                "keyword_score": score_result.get("keyword_score", 0),
                "skills_score": score_result.get("skills_score", 0)
            })
            
            # Save score
            score_file = TAILORED_DIR / f"{job_id}_v{iteration}_score.json"
            score_file.write_text(json.dumps(score_result, indent=2))
            
            print(f"      Score: {current_score}% (target: {TARGET_ATS_SCORE}%)")
            
            # Track best version
            if current_score > best_score:
                best_score = current_score
                best_resume = tailored_latex
            
            # Check if we've passed
            if current_score >= TARGET_ATS_SCORE:
                print(f"  ✅ Score {current_score}% meets target!")
                break
            
            # Prepare feedback for next iteration
            if iteration < MAX_REFINEMENT_ITERATIONS:
                feedback = f"""
Previous score: {current_score}%
Missing keywords: {', '.join(score_result.get('missing_keywords', []))}
Suggestions: {' '.join(score_result.get('suggestions', []))}
"""
                print(f"      Refining with feedback...")
        
        # Use best version for final output
        final_tex_file = TAILORED_DIR / f"{job_id}_final.tex"
        final_tex_file.write_text(best_resume)
        
        # === PHASE 4: COMPILE PDF ===
        update_status("compiling", {"job_id": job_id, "phase": "pdf_compilation"})
        print(f"  📄 Phase 4: Compiling PDF")
        
        success, error = compile_latex(final_tex_file)
        
        if success:
            final_pdf = final_tex_file.with_suffix(".pdf")
            print(f"  ✅ PDF ready: {final_pdf}")
            
            log_pipeline_event({
                "type": "pipeline_completed",
                "job_id": job_id,
                "final_score": best_score,
                "iterations": iteration,
                "pdf_path": str(final_pdf)
            })
            
            return {
                "success": True,
                "job_id": job_id,
                "score": best_score,
                "pdf_path": str(final_pdf),
                "tex_path": str(final_tex_file),
                "iterations": iteration,
                "company": company,
                "job_title": job_title,
                "job_url": job_url
            }
        else:
            print(f"  ⚠️  PDF compilation failed: {error[:100]}")
            
            # Still return success if we have the tex file
            log_pipeline_event({
                "type": "compilation_failed",
                "job_id": job_id,
                "error": error[:500]
            })
            
            return {
                "success": True,  # Tailoring succeeded, just compilation failed
                "job_id": job_id,
                "score": best_score,
                "pdf_path": None,
                "tex_path": str(final_tex_file),
                "iterations": iteration,
                "company": company,
                "job_title": job_title,
                "job_url": job_url,
                "compilation_error": error
            }
            
    except Exception as e:
        log_pipeline_event({
            "type": "pipeline_error",
            "job_id": job_id,
            "error": str(e)
        })
        
        return {
            "success": False,
            "job_id": job_id,
            "error": str(e)
        }

def main():
    """Main orchestrator loop."""
    print("=" * 60)
    print("🚀 Pipeline Orchestrator Started")
    print("=" * 60)
    print(f"Watching: {PENDING_JD_FILE}")
    print(f"Output:   {TAILORED_DIR}")
    print(f"Target:   {TARGET_ATS_SCORE}% ATS score")
    print(f"Max iterations: {MAX_REFINEMENT_ITERATIONS}")
    print("-" * 60)
    print("Waiting for job descriptions from Cursor agent...")
    print("(Cursor writes to pending_jd.json, I process and write resume_ready.json)")
    print("-" * 60)
    
    ensure_directories()
    cleanup_old_signals()
    
    # Load content pool once at startup (can be refreshed)
    content_pool = load_content_pool()
    latex_template = load_latex_template()
    
    print(f"✅ Content pool loaded: {len(content_pool['resume_content'])} chars resume, {len(content_pool['projects'])} chars projects")
    
    update_status("ready", {"message": "Waiting for jobs"})
    
    jobs_processed = 0
    
    try:
        while True:
            if PENDING_JD_FILE.exists():
                print(f"\n{'=' * 60}")
                print(f"📥 New job description detected!")
                print(f"{'=' * 60}")
                
                # Read the pending JD
                try:
                    jd_data = json.loads(PENDING_JD_FILE.read_text())
                except json.JSONDecodeError as e:
                    print(f"❌ Invalid JSON in pending_jd.json: {e}")
                    PENDING_JD_FILE.unlink()
                    continue
                
                # Process through pipeline
                result = process_job(jd_data, content_pool, latex_template)
                
                # Write result for Cursor to pick up
                RESUME_READY_FILE.write_text(json.dumps(result, indent=2))
                
                # Delete pending file to signal completion
                PENDING_JD_FILE.unlink()
                
                jobs_processed += 1
                
                if result["success"]:
                    print(f"\n✅ Resume ready for {result.get('company', 'Unknown')}")
                    print(f"   Score: {result.get('score', 0)}%")
                    print(f"   PDF: {result.get('pdf_path', 'N/A')}")
                else:
                    print(f"\n❌ Pipeline failed: {result.get('error', 'Unknown error')}")
                
                update_status("ready", {
                    "message": "Waiting for next job",
                    "jobs_processed": jobs_processed,
                    "last_job": result.get("job_id")
                })
                
                print(f"\n{'=' * 60}")
                print(f"Waiting for next job... (processed {jobs_processed} so far)")
                print(f"{'=' * 60}")
            
            time.sleep(POLL_INTERVAL_SECONDS)
            
    except KeyboardInterrupt:
        print("\n\n🛑 Orchestrator stopped by user")
        update_status("stopped", {"message": "User interrupted"})
        
    except Exception as e:
        print(f"\n\n❌ Orchestrator error: {e}")
        update_status("error", {"message": str(e)})
        raise

if __name__ == "__main__":
    main()

