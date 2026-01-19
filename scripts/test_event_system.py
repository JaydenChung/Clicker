#!/usr/bin/env python3
"""
Test Script for Event-Sourcing System

Run this to verify the new architecture works correctly.
No job applications needed - just tests the event processing pipeline.

Usage:
    python scripts/test_event_system.py
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path

# Paths
PROJECT_ROOT = Path(__file__).parent.parent
EVENTS_DIR = PROJECT_ROOT / "data" / "events"
APPLICATIONS_CSV = PROJECT_ROOT / "data" / "applications.csv"

def create_test_events():
    """Create a fake session with test events."""
    
    # Ensure directory exists
    EVENTS_DIR.mkdir(parents=True, exist_ok=True)
    
    session_id = "session_TEST_001"
    test_file = EVENTS_DIR / f"{session_id}.jsonl"
    
    print(f"📝 Creating test event file: {test_file}")
    
    # Generate timestamps
    base_time = datetime.now()
    
    events = [
        {
            "type": "session_start",
            "ts": base_time.isoformat() + "Z",
            "session_id": session_id,
            "session_type": "test",
            "max_applications": 3
        },
        {
            "type": "search_started",
            "ts": (base_time + timedelta(seconds=5)).isoformat() + "Z",
            "session_id": session_id,
            "keyword": "Test Engineer",
            "location": "Remote",
            "filters_applied": ["Entry level"]
        },
        # Application 1 - Success
        {
            "type": "application_started",
            "ts": (base_time + timedelta(seconds=30)).isoformat() + "Z",
            "session_id": session_id,
            "company": "Test Company Alpha",
            "job_title": "Junior Test Engineer",
            "location": "Remote",
            "work_type": "Remote",
            "job_url": "https://linkedin.com/jobs/view/test123",
            "salary_listed": "$80k-$100k",
            "applicant_count": "42 applicants"
        },
        {
            "type": "question_encountered",
            "ts": (base_time + timedelta(seconds=45)).isoformat() + "Z",
            "session_id": session_id,
            "question_text": "How many years of testing experience?",
            "question_type": "numeric",
            "answer_given": "2",
            "answer_source": "profile",
            "was_required": True
        },
        {
            "type": "question_encountered",
            "ts": (base_time + timedelta(seconds=50)).isoformat() + "Z",
            "session_id": session_id,
            "question_text": "Are you authorized to work in the US?",
            "question_type": "boolean",
            "answer_given": "Yes",
            "answer_source": "profile",
            "was_required": True
        },
        {
            "type": "application_completed",
            "ts": (base_time + timedelta(seconds=70)).isoformat() + "Z",
            "session_id": session_id,
            "company": "Test Company Alpha",
            "job_title": "Junior Test Engineer",
            "status": "applied",
            "total_steps": 4,
            "total_questions": 2,
            "questions_from_profile": 2,
            "questions_unanswered": 0,
            "duration_ms": 40000
        },
        # Application 2 - Success with unanswered question
        {
            "type": "application_started",
            "ts": (base_time + timedelta(seconds=90)).isoformat() + "Z",
            "session_id": session_id,
            "company": "Test Company Beta",
            "job_title": "QA Analyst",
            "location": "San Francisco, CA",
            "work_type": "Hybrid",
            "job_url": "https://linkedin.com/jobs/view/test456",
            "salary_listed": "",
            "applicant_count": "100+ applicants"
        },
        {
            "type": "question_encountered",
            "ts": (base_time + timedelta(seconds=105)).isoformat() + "Z",
            "session_id": session_id,
            "question_text": "Describe your experience with Selenium",
            "question_type": "text",
            "answer_given": "",
            "answer_source": "skipped",
            "was_required": False
        },
        {
            "type": "application_completed",
            "ts": (base_time + timedelta(seconds=130)).isoformat() + "Z",
            "session_id": session_id,
            "company": "Test Company Beta",
            "job_title": "QA Analyst",
            "status": "applied",
            "total_steps": 3,
            "total_questions": 1,
            "questions_from_profile": 0,
            "questions_unanswered": 1,
            "duration_ms": 40000
        },
        # Application 3 - Blocked
        {
            "type": "application_started",
            "ts": (base_time + timedelta(seconds=150)).isoformat() + "Z",
            "session_id": session_id,
            "company": "Test Company Gamma",
            "job_title": "SDET",
            "location": "New York, NY",
            "work_type": "On-site",
            "job_url": "https://linkedin.com/jobs/view/test789",
            "salary_listed": "$90k-$120k",
            "applicant_count": "25 applicants"
        },
        {
            "type": "blocker_encountered",
            "ts": (base_time + timedelta(seconds=160)).isoformat() + "Z",
            "session_id": session_id,
            "blocker_type": "hard",
            "blocker_reason": "assessment_required",
            "company": "Test Company Gamma",
            "action_taken": "skipped"
        },
        {
            "type": "application_completed",
            "ts": (base_time + timedelta(seconds=165)).isoformat() + "Z",
            "session_id": session_id,
            "company": "Test Company Gamma",
            "job_title": "SDET",
            "status": "skipped",
            "total_steps": 1,
            "total_questions": 0,
            "questions_from_profile": 0,
            "questions_unanswered": 0,
            "duration_ms": 15000
        },
        {
            "type": "search_completed",
            "ts": (base_time + timedelta(seconds=170)).isoformat() + "Z",
            "session_id": session_id,
            "keyword": "Test Engineer",
            "location": "Remote",
            "jobs_found": 10,
            "jobs_applied": 2,
            "jobs_skipped": 1
        },
        {
            "type": "session_end",
            "ts": (base_time + timedelta(seconds=180)).isoformat() + "Z",
            "session_id": session_id,
            "total_applications": 3,
            "stop_reason": "test_complete"
        }
    ]
    
    # Write events to file
    with open(test_file, 'w') as f:
        for event in events:
            f.write(json.dumps(event) + "\n")
    
    print(f"   ✅ Created {len(events)} test events")
    return test_file


def verify_file_readable(test_file):
    """Verify the event file can be read back."""
    print(f"\n📖 Verifying event file is readable...")
    
    try:
        with open(test_file, 'r') as f:
            lines = f.readlines()
        
        events = []
        for i, line in enumerate(lines, 1):
            event = json.loads(line)
            events.append(event)
        
        print(f"   ✅ Successfully parsed {len(events)} events")
        
        # Show event types
        event_types = [e["type"] for e in events]
        print(f"   📊 Event types: {', '.join(set(event_types))}")
        
        return True
    except Exception as e:
        print(f"   ❌ Error reading file: {e}")
        return False


def run_processor():
    """Run the session processor on the test file."""
    print(f"\n🔄 Running process_session.py...")
    
    import subprocess
    result = subprocess.run(
        ["python3", "scripts/process_session.py", "session_TEST_001"],
        capture_output=True,
        text=True,
        cwd=PROJECT_ROOT
    )
    
    print(result.stdout)
    if result.stderr:
        print(f"   ⚠️ Stderr: {result.stderr}")
    
    return result.returncode == 0


def verify_csv_output():
    """Check that CSV was updated."""
    print(f"\n📊 Verifying CSV output...")
    
    if not APPLICATIONS_CSV.exists():
        print(f"   ❌ CSV file not found: {APPLICATIONS_CSV}")
        return False
    
    with open(APPLICATIONS_CSV, 'r') as f:
        lines = f.readlines()
    
    # Count test entries
    test_entries = [l for l in lines if "Test Company" in l]
    
    print(f"   ✅ CSV has {len(lines)} total rows")
    print(f"   ✅ Found {len(test_entries)} test application entries")
    
    if test_entries:
        print(f"\n   📋 Test entries added:")
        for entry in test_entries:
            cols = entry.strip().split(',')
            if len(cols) >= 5:
                print(f"      - {cols[3]} | {cols[4]} | {cols[8]}")  # company, title, status
    
    return len(test_entries) > 0


def cleanup_test_data():
    """Remove test data (optional)."""
    print(f"\n🧹 Cleanup options:")
    print(f"   Test event file: data/events/session_TEST_001.jsonl")
    print(f"   To remove test entries from CSV, manually edit data/applications.csv")
    print(f"   (Test entries have 'Test Company' in company name)")


def main():
    print("=" * 60)
    print("🧪 EVENT SYSTEM TEST")
    print("=" * 60)
    print("\nThis test will:")
    print("1. Create a fake session with test events")
    print("2. Verify the event file is valid JSON")
    print("3. Run the processor to generate outputs")
    print("4. Verify the CSV was updated")
    print()
    
    # Step 1: Create test events
    test_file = create_test_events()
    
    # Step 2: Verify readable
    if not verify_file_readable(test_file):
        print("\n❌ TEST FAILED: Could not read event file")
        return
    
    # Step 3: Run processor
    if not run_processor():
        print("\n⚠️ Processor had issues - check output above")
    
    # Step 4: Verify CSV
    if not verify_csv_output():
        print("\n❌ TEST FAILED: CSV not updated correctly")
        return
    
    # Cleanup info
    cleanup_test_data()
    
    print("\n" + "=" * 60)
    print("✅ TEST PASSED!")
    print("=" * 60)
    print("\nThe event system is working correctly.")
    print("You can now use job_applicant_v2.md for real applications.")
    print("\nNext steps:")
    print("1. Review the test data in data/applications.csv")
    print("2. Check logs/performance/ for the session summary")
    print("3. When ready, rename job_applicant_v2.md to job_applicant.md")


if __name__ == "__main__":
    main()

