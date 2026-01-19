# LLM Tool Calling Patterns

## Overview
This document describes effective patterns for LLM tool calling in automation.

---

## Pattern 1: Explicit Tool Instructions

### Description
Clearly describe when and how to use each tool in the system prompt.

### Example
```
When you need to click an element:
1. First take a snapshot to get element refs
2. Identify the correct ref for the target
3. Use browser_click with the exact ref
4. Verify the action succeeded
```

### Benefits
- Reduces incorrect tool usage
- Improves reliability
- Makes failures easier to debug

---

## Pattern 2: Verification After Action

### Description
After any tool call that changes state, verify the change succeeded.

### Example
```
1. Call browser_click on submit button
2. Call browser_snapshot
3. Verify expected state (confirmation page, etc.)
4. If not expected, handle error
```

### Benefits
- Catches silent failures
- Enables recovery
- Maintains accurate state understanding

---

## Pattern 3: Batched Independent Calls

### Description
When multiple tool calls are independent, make them in parallel.

### Example
```
// Reading multiple files
// Instead of: read file1, then read file2, then read file3
// Do: read file1 AND file2 AND file3 simultaneously
```

### Benefits
- Faster execution
- Better user experience
- Reduced round trips

---

## Pattern 4: Incremental State Building

### Description
Build up understanding of complex pages incrementally.

### Example
```
1. Take initial snapshot (overview)
2. If form detected, identify form fields
3. For each field, determine type and value needed
4. Fill one field at a time with verification
```

### Benefits
- Handles complex pages
- Recovers from partial failures
- Maintains accurate state

---

## Pattern 5: Fallback Chains

### Description
When primary approach fails, have explicit fallbacks.

### Example
```
1. Try clicking "Easy Apply" button by ref
2. If fails, try by text content
3. If fails, try by position
4. If all fail, log and skip
```

### Benefits
- More robust execution
- Handles page variations
- Graceful degradation

---

## Anti-Patterns to Avoid

### Anti-Pattern 1: Tool Calls Without Verification
**Problem**: Assuming success without checking
**Fix**: Always verify important actions

### Anti-Pattern 2: Too Many Sequential Calls
**Problem**: Slow execution, context buildup
**Fix**: Batch independent calls

### Anti-Pattern 3: Vague Tool Descriptions
**Problem**: Model uses tools incorrectly
**Fix**: Explicit, example-rich descriptions

### Anti-Pattern 4: Ignoring Tool Errors
**Problem**: Cascading failures
**Fix**: Handle every error case

---

## Current System Tool Usage

### Browser Tools
- `browser_navigate` — Go to URL
- `browser_snapshot` — Get page state
- `browser_click` — Click element
- `browser_type` — Enter text
- `browser_select_option` — Choose from dropdown

### File Tools
- `read_file` — Read file contents
- `write` — Write file
- `grep` — Search for patterns

### Recommendations
1. Always snapshot before interacting
2. Use explicit element refs, not positions
3. Verify state after important actions
4. Batch independent file reads

