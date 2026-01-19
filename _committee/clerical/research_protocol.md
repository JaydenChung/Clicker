# 🔍 RESEARCH PROTOCOL

## Purpose
Committee members often need to research topics during deliberation to provide informed perspectives. This protocol ensures research is:
- Announced transparently
- Conducted systematically
- Reported clearly
- Documented for future reference

---

## When to Research

Research is appropriate when:
- A factual question arises that members cannot answer from knowledge
- Technical details are needed to inform a decision
- Historical precedent in the codebase is relevant
- External best practices should be consulted
- A claim needs verification

Research is NOT appropriate when:
- Delaying to avoid taking a position
- The information is already in the knowledge base
- The question is purely speculative
- It would derail the session from its goal

---

## Research Announcement Format

### Starting Research
```
[MEMBER NAME] ([Affiliation]):
"I need to conduct research before I can properly address this.

RESEARCHING: [Topic/Question]
LOOKING FOR: [Specific information sought]
SEARCH SCOPE: [Where looking - codebase, external, knowledge base]
RATIONALE: [Why this research is necessary for the discussion]

Please stand by..."
```

### During Research
The member conducts their search. Other members may:
- Continue discussing other aspects
- Wait for findings if critical
- Suggest additional search terms

### Reporting Findings
```
[MEMBER NAME] ([Affiliation]):
"Research complete.

QUERY: [What was searched]
FINDINGS:
1. [Finding 1]
2. [Finding 2]
...

SOURCES:
- [Source 1]
- [Source 2]

IMPLICATIONS FOR OUR DISCUSSION:
[How this affects the current topic]

Based on these findings, my position is..."
```

---

## Research Types

### 1. Codebase Research
Investigating the existing automation system:
```
RESEARCHING: How the current agent handles rate limiting
LOOKING FOR: Error handling code, retry logic, timing patterns
SEARCH SCOPE: /agents/, /config/, /logs/
```

### 2. Knowledge Base Research
Checking committee history:
```
RESEARCHING: Past decisions on parallel execution
LOOKING FOR: Previous session discussions, recorded decisions
SEARCH SCOPE: _committee/knowledge_base/, _committee/sessions/
```

### 3. External Research
Consulting outside sources:
```
RESEARCHING: Best practices for browser fingerprint evasion
LOOKING FOR: Current techniques, detection methods, countermeasures
SEARCH SCOPE: External web search, academic papers, industry blogs
```

### 4. Historical Research
Examining past sessions:
```
RESEARCHING: What we learned from the last external application session
LOOKING FOR: Failure patterns, blockers encountered, lessons learned
SEARCH SCOPE: /logs/, _committee/sessions/
```

---

## Research Depth Levels

### Quick Lookup (< 1 minute)
Simple fact-finding:
```
"Quick lookup: checking the current max_applications_per_session value..."
"Found: Currently set to 10 in /config/job_preferences.md"
```

### Standard Research (1-5 minutes)
Thorough investigation:
```
"Conducting standard research on ATS detection patterns...
This may take a few moments."
```

### Deep Dive (5+ minutes)
Extensive analysis:
```
"This requires a deep dive. I'll need to analyze multiple 
files and cross-reference patterns. 

Chair, do you want me to proceed now or would you prefer 
I complete this outside the session and report back?"
```

---

## Research Documentation

### Session Artifact
Significant research should be captured:

```markdown
# Research Report: [Topic]

**Researcher**: [Member Name]
**Session**: [Session ID]
**Date**: [Date]

## Question
[What prompted the research]

## Method
[How the research was conducted]

## Findings
[Detailed findings]

## Sources
[References]

## Conclusions
[What this means for the committee]

## Recommendations
[Suggested actions based on findings]
```

### Knowledge Base Update
Important findings should be added to the knowledge base:
- New concepts → `knowledge_base/concepts/`
- External research → `knowledge_base/external_research/`
- Lessons learned → `knowledge_base/lessons_learned/`

---

## Collaborative Research

### Research Teams
For complex topics:
```
CHAIR: "This requires expertise from multiple areas. 
[Member A] and [Member B], please collaborate on researching 
[topic]. Report back jointly."

[MEMBER A]: "I'll investigate [aspect 1]."
[MEMBER B]: "I'll cover [aspect 2]."
```

### Research Handoff
```
[MEMBER A]: "I've found information on [aspect], but this 
leads to questions in [Member B]'s domain."

[MEMBER B]: "I'll pick up from there and research [follow-up]."
```

---

## Research Quality Standards

### Good Research
✅ Specific question clearly stated
✅ Relevant sources identified
✅ Findings directly address the question
✅ Implications for discussion explained
✅ Limitations acknowledged

### Poor Research
❌ Vague topic ("researching agents")
❌ No clear findings reported
❌ Findings don't connect to discussion
❌ Sources not identified
❌ Research used to delay decisions

---

## Chair's Role in Research

The Chair may:
- Authorize or defer research requests
- Set time limits on research
- Redirect research scope
- Request research from specific members
- Table discussion pending research completion

```
CHAIR: "[Member], your research request is approved. 
Please complete within [time] and report back.

In the meantime, let's discuss [other aspect]..."
```

