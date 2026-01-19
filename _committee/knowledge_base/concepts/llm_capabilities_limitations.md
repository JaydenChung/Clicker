# LLM Capabilities and Limitations

## Overview

Understanding what Large Language Models (LLMs) like Claude can and cannot do is essential for effective agent design.

---

## Capabilities

### What LLMs Do Well
- **Language understanding**: Parse instructions, questions, content
- **Reasoning**: Multi-step logical thinking
- **Code generation**: Write and modify code
- **Tool use**: Call functions with appropriate parameters
- **Context following**: Maintain coherence across conversation
- **Pattern matching**: Recognize similar situations

### Tool Calling
LLMs can use tools when:
- Tool is clearly defined
- Parameters are well-specified
- Examples are provided
- Error handling is described

---

## Limitations

### What LLMs Struggle With
- **Precise counting**: May miscount items
- **Exact text matching**: May paraphrase unexpectedly
- **Long context coherence**: May drift over long conversations
- **Remembering specifics**: May forget earlier details
- **Math**: Complex calculations can be wrong
- **Real-time information**: Training data has cutoff

### Hallucination
LLMs may:
- Generate plausible but false information
- Confidently state incorrect facts
- Invent details not in context
- Fill gaps with assumptions

### Context Limits
- Fixed context window size
- Information at edges may be less accessible
- Very long conversations lose early context

---

## Implications for Agents

### Design Principles
1. **Verify important outputs**: Don't trust without checking
2. **Break down complex tasks**: Smaller steps, more reliable
3. **Provide examples**: Show what you want
4. **Be explicit**: Don't assume understanding
5. **Handle errors**: LLMs will make mistakes

### When to Use LLM vs. Deterministic Code
| Task | Use LLM | Use Code |
|------|---------|----------|
| Understanding intent | ✅ | ❌ |
| Parsing structured data | Depends | ✅ |
| Exact string matching | ❌ | ✅ |
| Decision making | ✅ | Sometimes |
| Calculation | ❌ | ✅ |
| Natural language output | ✅ | ❌ |

---

## Best Practices

1. **Explicit instructions**: Be very clear about expectations
2. **Verification**: Check outputs before acting on them
3. **Fallbacks**: Have backup plans for failures
4. **Iteration**: Expect refinement over time
5. **Monitoring**: Track where LLMs fail

