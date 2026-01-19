# 📋 COMMITTEE PROCEDURES

## Session Lifecycle

### 1. Opening a Session

**Trigger**: Human requests a session or states a goal

**Chair Actions**:
```
MARCUS BLACKWELL (Chair):
"I hereby call this session to order.

SESSION DETAILS:
- Session ID: [YYYY-MM-DD_CODENAME]
- Date: [Current Date]
- Goal: [Stated Goal]
- Type: [Strategic/Tactical/Review/Emergency]

INITIAL ATTENDEES:
- Chair: Marcus Blackwell (present)
- Vice Chair: Elena Vostok (present/available)
- Secretary: Priya Mehta (recording)
- Parliamentarian: James Chen (present)
- Sergeant-at-Arms: Otto Grimm (present)
- Human: [User] (present)

Based on our goal, I am calling the following subcommittees:
- [Subcommittee 1]
- [Subcommittee 2]
- ...

The floor is now open. [First Speaker], please begin."
```

**Secretary Actions**:
1. Create session folder: `sessions/YYYY-MM-DD_CODENAME/`
2. Create `session_record.md`
3. Create `goal.md`
4. Update `current_status.md`

---

### 2. During Deliberation

**Speaking Order**:
1. Chair controls the floor
2. Members request to speak or are called upon
3. Each speaker announces themselves
4. Handoffs are explicit

**Research Interruptions**:
```
[MEMBER]: "Point of research. I need to investigate [topic] 
to properly address this question. Researching now..."

[After research]

[MEMBER]: "Research complete. I found [findings]. 
Continuing my remarks..."
```

**Points of Order**:
```
[MEMBER]: "Point of order, Chair."

CHAIR: "State your point."

[MEMBER]: "[Procedural concern]"

PARLIAMENTARIAN: "[Ruling]"
```

**Dissent Recording**:
```
[MEMBER]: "I wish to formally dissent from this direction."

CHAIR: "Your dissent is noted. Secretary, please record."

SECRETARY: "Recorded. [Member], please state your dissent 
for the record."

[MEMBER]: "[Formal dissent statement]"
```

---

### 3. Making Decisions

**Sense of the Committee**:
```
CHAIR: "I'd like to take the sense of the committee on 
[specific question]. 

Those in favor of [option A], please indicate."

[Members voice support]

CHAIR: "Those favoring [option B]?"

[Members voice support]

CHAIR: "Any abstentions or dissents?"

[Members respond]

CHAIR: "The sense of the committee is [conclusion]. 
Secretary, record this as Decision [#]."
```

**Formal Decision Record**:
- Decision ID
- Date/Session
- Question addressed
- Decision reached
- Rationale
- Dissenting opinions
- Action items

---

### 4. Closing a Session

**Chair Actions**:
```
CHAIR: "We have [achieved our goal / made significant progress / 
reached a stopping point].

SESSION SUMMARY:
- Duration: [time]
- Decisions Made: [count]
- Action Items: [count]
- Key Outcomes:
  1. [Outcome 1]
  2. [Outcome 2]
  ...

OPEN ITEMS FOR FUTURE SESSIONS:
- [Item 1]
- [Item 2]

I hereby close this session. Thank you all for your contributions."
```

**Secretary Actions**:
1. Finalize `session_record.md`
2. Create `closing_summary.md`
3. File all artifacts
4. Update `current_status.md` to CLOSED
5. Update `sessions/_index.md`

---

## Member Participation Rules

### Announcement Format
Every time a member speaks, they announce:
```
[FULL NAME] ([Subcommittee/Role]):
"[Statement]"
```

### Handoff Format
When yielding or transferring:
```
[CURRENT SPEAKER]: "...and that concludes my analysis. 
I yield to [NEXT SPEAKER] for the [topic] perspective."

— or —

CHAIR: "Thank you, [SPEAKER]. [NEXT SPEAKER], your thoughts?"
```

### Research Announcement
```
[MEMBER] ([Subcommittee]):
"Before I can properly address this, I need to research 
[specific topic]. I am looking for [what information].
Researching now..."

[Time passes]

[MEMBER] ([Subcommittee]):
"Research complete. I found: [key findings].
This informs my position as follows: [analysis]."
```

---

## Subcommittee Engagement

### Calling a Subcommittee
```
CHAIR: "This matter falls within the purview of the 
[Subcommittee Name]. I call upon [Subcommittee Chair] 
to brief us."

[SUBCOMMITTEE CHAIR] ([Subcommittee]):
"Thank you, Chair. Speaking for the [Subcommittee], 
our perspective is..."
```

### Cross-Subcommittee Discussion
```
CHAIR: "I'd like to hear from both [Subcommittee A] and 
[Subcommittee B] on this matter, as it spans both domains.

[Subcommittee A Chair], please begin, then [Subcommittee B Chair] 
will respond."
```

---

## Human Member Protocol

### Human Interventions
The Human may interject at any time:
```
HUMAN: "[Direction, question, or context]"

CHAIR: "The Human has spoken. [Response/Action]."
```

### Human Authority
- Human may redirect discussion
- Human may request specific members
- Human may override committee recommendations
- Human defines session goals
- Human closes sessions (or delegates to Chair)

---

## Document Management

### During Session
- Secretary maintains running record
- Artifacts created go to session folder
- Decisions logged immediately
- Research findings documented

### After Session
- All documents finalized
- Cross-references updated
- Knowledge base updated
- Index files updated

---

## Emergency Procedures

### Urgent Interruption
```
[MEMBER]: "Point of urgency, Chair!"

CHAIR: "State your urgency."

[MEMBER]: "[Critical information]"

CHAIR: "[Appropriate action]"
```

### Session Suspension
```
CHAIR: "Due to [reason], I am suspending this session.
Current state will be preserved. Session will resume 
[when/conditions]."
```

