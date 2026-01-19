#!/usr/bin/env python3
"""
View Pending Uploads

Quick utility to see which jobs need manual resume upload.
"""

import os
import json
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).parent.parent
LOGS_DIR = BASE_DIR / "logs" / "pipeline"
TAILORED_DIR = BASE_DIR / "resume" / "tailored"

def main():
    print("=" * 70)
    print("📋 PENDING RESUME UPLOADS")
    print("=" * 70)
    
    # Find all pipeline logs
    log_files = sorted(LOGS_DIR.glob("pipeline_*.jsonl"), reverse=True)
    
    if not log_files:
        print("\nNo pipeline logs found.")
        print(f"Logs directory: {LOGS_DIR}")
        return
    
    pending_jobs = []
    completed_jobs = []
    
    for log_file in log_files:
        with open(log_file) as f:
            for line in f:
                try:
                    event = json.loads(line)
                    if event.get("type") == "pipeline_completed":
                        job_id = event.get("job_id", "unknown")
                        pdf_path = event.get("pdf_path")
                        score = event.get("final_score", 0)
                        
                        job_info = {
                            "job_id": job_id,
                            "score": score,
                            "pdf_path": pdf_path,
                            "timestamp": event.get("timestamp", "")
                        }
                        
                        # Check if PDF exists
                        if pdf_path and Path(pdf_path).exists():
                            completed_jobs.append(job_info)
                        else:
                            pending_jobs.append(job_info)
                            
                except json.JSONDecodeError:
                    continue
    
    print(f"\n📁 Tailored resumes directory: {TAILORED_DIR}")
    
    # Show available PDFs
    pdfs = list(TAILORED_DIR.glob("*_final.pdf"))
    print(f"\n✅ READY RESUMES ({len(pdfs)} PDFs):")
    print("-" * 70)
    
    if pdfs:
        for pdf in sorted(pdfs, reverse=True)[:10]:  # Show latest 10
            # Extract job info from filename
            parts = pdf.stem.replace("_final", "").split("_")
            if len(parts) >= 4:
                timestamp = parts[0] + "_" + parts[1]
                company = parts[2]
                title = "_".join(parts[3:])
                
                # Find corresponding score
                score_file = pdf.parent / f"{pdf.stem.replace('_final', '')}_v1_score.json"
                score = "?"
                for i in range(3, 0, -1):
                    sf = pdf.parent / f"{pdf.stem.replace('_final', '')}_v{i}_score.json"
                    if sf.exists():
                        try:
                            score = json.loads(sf.read_text()).get("overall_score", "?")
                        except:
                            pass
                        break
                
                print(f"  [{score}%] {company} - {title}")
                print(f"        📄 {pdf}")
            else:
                print(f"  📄 {pdf.name}")
        
        if len(pdfs) > 10:
            print(f"  ... and {len(pdfs) - 10} more")
    else:
        print("  No PDFs found")
    
    # Show pending (no PDF)
    tex_only = list(TAILORED_DIR.glob("*_final.tex"))
    tex_only = [t for t in tex_only if not t.with_suffix(".pdf").exists()]
    
    if tex_only:
        print(f"\n⚠️  COMPILATION NEEDED ({len(tex_only)} files):")
        print("-" * 70)
        for tex in tex_only[:5]:
            print(f"  📝 {tex.name}")
            print(f"     Run: cd resume/tailored && pdflatex {tex.name}")
    
    print("\n" + "=" * 70)
    print("💡 To manually upload a resume:")
    print("   1. Find the job tab (should still be open)")
    print("   2. Upload the corresponding *_final.pdf file")
    print("   3. Complete the application")
    print("=" * 70)


if __name__ == "__main__":
    main()

