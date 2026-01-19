# Browser Automation Fundamentals

## Overview

Browser automation involves controlling a web browser programmatically to perform actions that a human would normally do manually.

---

## Key Concepts

### Browser Control
- **Headless**: Browser runs without visible window
- **Headed**: Browser runs with visible window (more stealth)
- **Browser Context**: Isolated session with own cookies, storage

### Page Interaction
- **Navigation**: Going to URLs
- **Clicking**: Triggering click events
- **Typing**: Entering text into fields
- **Selecting**: Choosing dropdown options
- **Waiting**: Pausing for page loads

### Element Finding
- **Selectors**: CSS, XPath, text content
- **Refs**: Accessibility tree references
- **Coordinates**: Screen position (fragile)

---

## Tools Used

### MCP Browser Extension
The system uses Cursor's MCP browser extension:
- `browser_navigate`: Go to URL
- `browser_snapshot`: Get page state
- `browser_click`: Click element
- `browser_type`: Enter text
- `browser_select_option`: Choose dropdown

### Workflow Pattern
```
1. Navigate to page
2. Snapshot to get element refs
3. Interact using refs
4. Snapshot to verify
5. Repeat as needed
```

---

## Detection Risks

Browser automation can be detected by:
- **JavaScript checks**: navigator.webdriver, etc.
- **Behavioral analysis**: Mouse patterns, timing
- **Network analysis**: Request patterns
- **Fingerprinting**: Canvas, WebGL, fonts

See Anti-Detection Techniques for countermeasures.

---

## Best Practices

1. **Use headed browser**: Less detectable than headless
2. **Add realistic delays**: Humans don't click instantly
3. **Verify after actions**: Ensure actions succeeded
4. **Handle errors**: Pages change, elements move
5. **Respect rate limits**: Too fast = detected

