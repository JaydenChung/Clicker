#!/usr/bin/env python3
"""
Session Event Processor

Processes events from a session file and generates:
- CSV entries for applications.csv
- Question logs
- Performance reports
- Session summary

Usage:
    python scripts/process_session.py                    # Process latest session
    python scripts/process_session.py session_2026-01-19_01  # Process specific session
    python scripts/process_session.py --all              # Process all unprocessed sessions

Part of the Event-Sourcing Architecture (DECISION-001)
"""

import json
import csv
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field, asdict

# Paths
PROJECT_ROOT = Path(__file__).parent.parent
EVENTS_DIR = PROJECT_ROOT / "data" / "events"
APPLICATIONS_CSV = PROJECT_ROOT / "data" / "applications.csv"
QUESTIONS_LOG = PROJECT_ROOT / "logs" / "questions" / "all_questions.md"
PERFORMANCE_DIR = PROJECT_ROOT / "logs" / "performance"
PROCESSED_MARKER_DIR = PROJECT_ROOT / "data" / "events" / ".processed"


@dataclass
class Application:
    """Represents a single job application reconstructed from events."""
    application_id: str = ""
    session_id: str = ""
    date_applied: str = ""
    time_applied: str = ""
    company: str = ""
    job_title: str = ""
    location: str = ""
    work_type: str = ""
    job_url: str = ""
    status: str = ""
    salary_listed: str = ""
    applicant_count: str = ""
    search_keyword: str = ""
    search_location: str = ""
    questions_count: int = 0
    questions_from_profile: int = 0
    questions_unanswered: int = 0
    time_to_apply_seconds: int = 0
    steps_count: int = 0
    notes: str = ""
    
    # Internal tracking (not in CSV)
    questions: List[Dict] = field(default_factory=list)
    steps: List[Dict] = field(default_factory=list)
    start_ts: Optional[datetime] = None
    end_ts: Optional[datetime] = None
    is_complete: bool = False


@dataclass 
class SessionSummary:
    """Summary statistics for a session."""
    session_id: str
    session_type: str
    start_time: str
    end_time: str
    duration_minutes: float
    total_applications: int
    successful: int
    skipped: int
    pending_manual: int
    errors: int
    total_questions: int
    questions_unanswered: int
    searches_performed: int
    stop_reason: str


def parse_timestamp(ts: str) -> datetime:
    """Parse ISO timestamp to datetime."""
    # Handle both Z and +00:00 formats
    ts = ts.replace("Z", "+00:00")
    try:
        return datetime.fromisoformat(ts)
    except ValueError:
        # Fallback for other formats
        return datetime.strptime(ts[:19], "%Y-%m-%dT%H:%M:%S")


def load_events(session_file: Path) -> List[Dict]:
    """Load events from a JSONL file."""
    events = []
    with open(session_file, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                events.append(json.loads(line))
            except json.JSONDecodeError as e:
                print(f"  ⚠️  Warning: Invalid JSON on line {line_num}: {e}")
                # Record error but continue processing
                events.append({
                    "type": "parse_error",
                    "line_num": line_num,
                    "error": str(e),
                    "raw": line[:100]
                })
    return events


def reconstruct_applications(events: List[Dict]) -> tuple[List[Application], SessionSummary]:
    """
    Reconstruct application records from event stream.
    
    Handles:
    - Normal start→complete flows
    - Orphaned starts (no completion event)
    - Questions and steps within applications
    """
    applications: List[Application] = []
    current_app: Optional[Application] = None
    current_search = {"keyword": "", "location": ""}
    session_info = {
        "session_id": "",
        "session_type": "",
        "start_time": "",
        "end_time": "",
        "max_applications": 0,
        "stop_reason": "unknown",
        "searches": 0
    }
    
    for event in events:
        event_type = event.get("type", "")
        
        # Session events
        if event_type == "session_start":
            session_info["session_id"] = event.get("session_id", "")
            session_info["session_type"] = event.get("session_type", "easy_apply")
            session_info["start_time"] = event.get("ts", "")
            session_info["max_applications"] = event.get("max_applications", 0)
            
        elif event_type == "session_end":
            session_info["end_time"] = event.get("ts", "")
            session_info["stop_reason"] = event.get("stop_reason", "unknown")
            
        # Search events
        elif event_type == "search_started":
            current_search["keyword"] = event.get("keyword", "")
            current_search["location"] = event.get("location", "")
            session_info["searches"] += 1
            
        # Application events
        elif event_type == "application_started":
            # If there's an orphaned previous application, finalize it
            if current_app and not current_app.is_complete:
                current_app.status = "incomplete"
                current_app.notes = "Orphaned - no completion event"
                current_app.is_complete = True
                applications.append(current_app)
            
            # Start new application
            ts = parse_timestamp(event.get("ts", ""))
            current_app = Application(
                session_id=event.get("session_id", session_info["session_id"]),
                company=event.get("company", ""),
                job_title=event.get("job_title", ""),
                location=event.get("location", ""),
                work_type=event.get("work_type", ""),
                job_url=event.get("job_url", ""),
                salary_listed=event.get("salary_listed", ""),
                applicant_count=event.get("applicant_count", ""),
                search_keyword=current_search["keyword"],
                search_location=current_search["location"],
                date_applied=ts.strftime("%Y-%m-%d"),
                time_applied=ts.strftime("%H:%M:%S"),
                start_ts=ts
            )
            
        elif event_type == "step_started" and current_app:
            current_app.steps.append({
                "step_number": event.get("step_number", 0),
                "step_name": event.get("step_name", ""),
                "start_ts": event.get("ts", "")
            })
            
        elif event_type == "step_completed" and current_app:
            current_app.steps_count = max(current_app.steps_count, event.get("step_number", 0))
            
        elif event_type == "question_encountered" and current_app:
            q = {
                "question": event.get("question_text", ""),
                "type": event.get("question_type", ""),
                "answer": event.get("answer_given", ""),
                "source": event.get("answer_source", ""),
                "required": event.get("was_required", True)
            }
            current_app.questions.append(q)
            current_app.questions_count += 1
            if q["source"] == "profile":
                current_app.questions_from_profile += 1
            elif q["source"] in ("skipped", ""):
                current_app.questions_unanswered += 1
                
        elif event_type == "application_completed" and current_app:
            ts = parse_timestamp(event.get("ts", ""))
            current_app.end_ts = ts
            current_app.status = event.get("status", "applied")
            current_app.is_complete = True
            
            # Calculate duration
            if current_app.start_ts:
                duration = (ts - current_app.start_ts).total_seconds()
                current_app.time_to_apply_seconds = int(duration)
            
            # Use event's counts if available (more accurate)
            current_app.steps_count = event.get("total_steps", current_app.steps_count)
            current_app.questions_count = event.get("total_questions", current_app.questions_count)
            
            # Generate application ID
            current_app.application_id = f"{current_app.date_applied.replace('-', '')}-{current_app.time_applied.replace(':', '')}-{len(applications)+1:03d}"
            
            applications.append(current_app)
            current_app = None
            
        elif event_type == "blocker_encountered" and current_app:
            current_app.notes = f"Blocker: {event.get('blocker_reason', 'unknown')}"
            
        elif event_type == "error_occurred" and current_app:
            if not current_app.notes:
                current_app.notes = f"Error: {event.get('error_message', 'unknown')}"
    
    # Handle final orphaned application
    if current_app and not current_app.is_complete:
        current_app.status = "incomplete"
        current_app.notes = "Session ended during application"
        applications.append(current_app)
    
    # Build session summary
    start_dt = parse_timestamp(session_info["start_time"]) if session_info["start_time"] else datetime.now()
    end_dt = parse_timestamp(session_info["end_time"]) if session_info["end_time"] else datetime.now()
    duration = (end_dt - start_dt).total_seconds() / 60
    
    summary = SessionSummary(
        session_id=session_info["session_id"],
        session_type=session_info["session_type"],
        start_time=session_info["start_time"],
        end_time=session_info["end_time"],
        duration_minutes=round(duration, 1),
        total_applications=len(applications),
        successful=len([a for a in applications if a.status == "applied"]),
        skipped=len([a for a in applications if a.status == "skipped"]),
        pending_manual=len([a for a in applications if a.status == "pending_manual"]),
        errors=len([a for a in applications if a.status in ("error", "incomplete")]),
        total_questions=sum(a.questions_count for a in applications),
        questions_unanswered=sum(a.questions_unanswered for a in applications),
        searches_performed=session_info["searches"],
        stop_reason=session_info["stop_reason"]
    )
    
    return applications, summary


def write_to_csv(applications: List[Application], csv_path: Path):
    """Append applications to the master CSV file."""
    # CSV columns
    fieldnames = [
        "application_id", "date_applied", "time_applied", "company", "job_title",
        "location", "work_type", "job_url", "status", "salary_listed",
        "applicant_count", "search_keyword", "search_location", "session_id",
        "questions_count", "questions_unanswered", "time_to_apply_seconds",
        "steps_count", "notes"
    ]
    
    # Check if file exists and has header
    file_exists = csv_path.exists() and csv_path.stat().st_size > 0
    
    with open(csv_path, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        
        if not file_exists:
            writer.writeheader()
        
        for app in applications:
            row = {
                "application_id": app.application_id,
                "date_applied": app.date_applied,
                "time_applied": app.time_applied,
                "company": app.company,
                "job_title": app.job_title,
                "location": app.location,
                "work_type": app.work_type,
                "job_url": app.job_url,
                "status": app.status,
                "salary_listed": app.salary_listed,
                "applicant_count": app.applicant_count,
                "search_keyword": app.search_keyword,
                "search_location": app.search_location,
                "session_id": app.session_id,
                "questions_count": app.questions_count,
                "questions_unanswered": app.questions_unanswered,
                "time_to_apply_seconds": app.time_to_apply_seconds,
                "steps_count": app.steps_count,
                "notes": app.notes
            }
            writer.writerow(row)


def write_questions_log(applications: List[Application], log_path: Path):
    """Append questions to the questions log."""
    if not any(app.questions for app in applications):
        return
    
    log_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(log_path, 'a', encoding='utf-8') as f:
        for app in applications:
            if app.questions:
                f.write(f"\n## {app.company} - {app.job_title}\n")
                f.write(f"**Date**: {app.date_applied} | **Session**: {app.session_id}\n\n")
                
                for q in app.questions:
                    status = "✅" if q["source"] == "profile" else "⚠️" if q["source"] == "generated" else "❓"
                    f.write(f"- {status} **{q['question']}**\n")
                    f.write(f"  - Answer: `{q['answer']}` (source: {q['source']})\n")
                
                f.write("\n---\n")


def write_session_summary(summary: SessionSummary, output_dir: Path):
    """Write session summary to performance logs."""
    output_dir.mkdir(parents=True, exist_ok=True)
    summary_file = output_dir / f"{summary.session_id}_summary.md"
    
    content = f"""# Session Summary: {summary.session_id}

**Type**: {summary.session_type}
**Date**: {summary.start_time[:10] if summary.start_time else 'Unknown'}
**Duration**: {summary.duration_minutes} minutes
**Stop Reason**: {summary.stop_reason}

---

## Applications

| Metric | Count |
|--------|-------|
| Total | {summary.total_applications} |
| Successful | {summary.successful} |
| Skipped | {summary.skipped} |
| Pending Manual | {summary.pending_manual} |
| Errors | {summary.errors} |

---

## Questions

- **Total Questions**: {summary.total_questions}
- **Unanswered**: {summary.questions_unanswered}

---

## Searches

- **Searches Performed**: {summary.searches_performed}

---

*Generated by process_session.py*
"""
    
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return summary_file


def mark_as_processed(session_file: Path):
    """Mark a session file as processed to avoid reprocessing."""
    PROCESSED_MARKER_DIR.mkdir(parents=True, exist_ok=True)
    marker = PROCESSED_MARKER_DIR / f"{session_file.stem}.processed"
    marker.touch()


def is_processed(session_file: Path) -> bool:
    """Check if a session file has already been processed."""
    marker = PROCESSED_MARKER_DIR / f"{session_file.stem}.processed"
    return marker.exists()


def find_latest_session() -> Optional[Path]:
    """Find the most recent session file."""
    if not EVENTS_DIR.exists():
        return None
    
    session_files = list(EVENTS_DIR.glob("session_*.jsonl"))
    if not session_files:
        return None
    
    return max(session_files, key=lambda f: f.stat().st_mtime)


def find_unprocessed_sessions() -> List[Path]:
    """Find all session files that haven't been processed."""
    if not EVENTS_DIR.exists():
        return []
    
    return [f for f in EVENTS_DIR.glob("session_*.jsonl") if not is_processed(f)]


def process_session(session_file: Path, force: bool = False) -> bool:
    """
    Process a single session file.
    
    Returns True if processing succeeded.
    """
    if not session_file.exists():
        print(f"❌ Session file not found: {session_file}")
        return False
    
    if is_processed(session_file) and not force:
        print(f"⏭️  Already processed: {session_file.name}")
        return True
    
    print(f"📂 Processing: {session_file.name}")
    
    # Load events
    events = load_events(session_file)
    if not events:
        print("  ⚠️  No events found in file")
        return False
    
    print(f"  📊 Loaded {len(events)} events")
    
    # Reconstruct applications
    applications, summary = reconstruct_applications(events)
    print(f"  📝 Reconstructed {len(applications)} applications")
    
    # Write to CSV
    write_to_csv(applications, APPLICATIONS_CSV)
    print(f"  ✅ Updated {APPLICATIONS_CSV.name}")
    
    # Write questions log
    write_questions_log(applications, QUESTIONS_LOG)
    print(f"  ✅ Updated questions log")
    
    # Write session summary
    summary_file = write_session_summary(summary, PERFORMANCE_DIR)
    print(f"  ✅ Created {summary_file.name}")
    
    # Mark as processed
    mark_as_processed(session_file)
    
    # Print summary
    print(f"\n  📈 Session Summary:")
    print(f"     Applications: {summary.successful} applied, {summary.skipped} skipped, {summary.errors} errors")
    print(f"     Questions: {summary.total_questions} total, {summary.questions_unanswered} unanswered")
    print(f"     Duration: {summary.duration_minutes} minutes")
    
    return True


def main():
    """Main entry point."""
    print("🔄 Session Event Processor")
    print("=" * 40)
    
    # Parse arguments
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        
        if arg == "--all":
            # Process all unprocessed sessions
            sessions = find_unprocessed_sessions()
            if not sessions:
                print("✅ No unprocessed sessions found")
                return
            
            print(f"Found {len(sessions)} unprocessed sessions\n")
            for session_file in sorted(sessions):
                process_session(session_file)
                print()
                
        elif arg == "--force":
            # Force reprocess latest
            session_file = find_latest_session()
            if session_file:
                process_session(session_file, force=True)
            else:
                print("❌ No session files found")
                
        else:
            # Process specific session
            session_name = arg if arg.endswith(".jsonl") else f"{arg}.jsonl"
            session_file = EVENTS_DIR / session_name
            process_session(session_file, force=True)
    else:
        # Process latest session
        session_file = find_latest_session()
        if session_file:
            process_session(session_file)
        else:
            print("❌ No session files found in data/events/")
            print("   Run an application session first to generate events.")


if __name__ == "__main__":
    main()

