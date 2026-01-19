# Subcommittee Charter: LLM Orchestration

## Identity
| Field | Value |
|-------|-------|
| **Number** | 04 |
| **Name** | LLM Orchestration |
| **Chair** | Dr. Angela Chen |
| **Category** | Technical |
| **Members** | 9 |

---

## Purpose

The LLM Orchestration Subcommittee advises on all matters relating to how the system uses large language models, including context management, tool calling, prompt engineering, and multi-turn interactions.

---

## Scope

### In Scope
- Context window management
- Tool calling patterns and best practices
- Prompt engineering for agents
- Multi-turn orchestration
- Token efficiency
- Error handling for LLM calls
- Chain-of-thought patterns
- LLM limitations and hallucination risks

### Out of Scope
- Agent architecture (→ Agent Architecture)
- Browser control (→ Browser Stealth)
- Application form content (→ ATS Systems)

---

## Key Questions We Address

1. How should agents use their context window efficiently?
2. What tool calling patterns are most effective?
3. How do we handle LLM errors and hallucinations?
4. How should we structure prompts for reliability?
5. When should we use multiple LLM calls vs. one?
6. How do we maintain coherent multi-turn interactions?

---

## Current System Context

The system uses Claude via Cursor's interface:
- Agent personas defined in markdown files
- Tool calls via MCP browser extension
- Multi-turn conversations for complex tasks
- Context includes codebase, rules, and memory

Challenges:
- Context window limits during long sessions
- Tool call reliability
- Hallucination risks
- Maintaining agent "persona" consistency

---

## Archetype Distribution

| Archetype | Members | Names |
|-----------|---------|-------|
| Visionary | 1 | Dr. Angela Chen |
| Skeptic | 2 | Dr. Rachel Green, Thomas Wright |
| Academic | 2 | Dr. Samuel Osei, Dr. Angela Chen |
| Practitioner | 5 | Boris Novak, Kira Yamamoto, Nina Petrov, Alejandro Ruiz, Ji-Yeon Park |

---

## Meeting Triggers

This subcommittee should be called when:
- Designing new agent prompts
- Optimizing token usage
- Debugging LLM-related failures
- Adding new tool calling patterns
- Addressing hallucination issues
- Planning multi-agent LLM coordination

---

## Relationships to Other Subcommittees

| Subcommittee | Relationship |
|--------------|--------------|
| Agent Architecture | We define how agents use LLMs |
| Cost & Resources | Token usage = cost |
| Reliability Engineering | LLM errors affect reliability |
| Quality Assurance | LLM outputs need validation |
| Future Systems | LLM capabilities evolving rapidly |

