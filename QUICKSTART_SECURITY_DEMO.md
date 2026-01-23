# 🎓 Quick Start Guide: Prompt Injection Demonstration

## What Was Added

This educational security demonstration adds three new modes to the Travel Planner app:

### 1. **Normal Mode** (Default)
- Standard travel planning with basic validation
- Uses the existing `/plan` endpoint
- Safe for general use

### 2. **⚠️ Vulnerable Mode** (Educational)
- Demonstrates unsafe handling of user input
- Uses the new `/plan-vulnerable` endpoint
- Shows how prompt injection attacks work
- **For educational purposes only!**

### 3. **✅ Secure Mode** (Best Practice)
- Demonstrates proper security mitigations
- Uses the new `/plan-secure` endpoint
- Shows how to protect against prompt injection
- Input validation, sanitization, and structured prompts

## How to Use

### Step 1: Access the Application
Open your browser to: `http://localhost:5002/`

### Step 2: Choose a Security Mode
In the form, find the "🔒 Security Demo Mode" section and select one of:
- Normal Mode (standard validation)
- ⚠️ Vulnerable Mode (demo: no sanitization)
- ✅ Secure Mode (demo: strict validation)

### Step 3: Try an Attack (Optional)
1. Click "View attack examples →" link or visit `/attacks`
2. Copy one of the 8 pre-built attack payloads
3. Select "⚠️ Vulnerable Mode"
4. Paste the attack into the "Special Requests" field
5. Submit and observe how the AI responds to the injection

### Step 4: Compare Security Modes
Try the same attack payload with:
- Vulnerable Mode: See the AI follow the malicious instructions
- Secure Mode: See the input rejected or sanitized

## Attack Examples Available

Visit `/attacks` to see 8 different attack types:
1. **Role Hijacking** - Make AI adopt different persona
2. **System Prompt Extraction** - Try to reveal system instructions
3. **Task Override** - Replace travel planning with different task
4. **Sentiment Manipulation** - Force negative responses
5. **Context Switch** - Break format and change context
6. **Jailbreak Attempt** - Multi-step bypass attempt
7. **Data Extraction** - Try to access other users' data
8. **Subtle Manipulation** - Blend malicious with legitimate requests

## Files Added/Modified

### New Files:
- `SECURITY_DEMO.md` - Complete security documentation (8,665 chars)
- `templates/attacks.html` - Interactive attack examples page (15,846 chars)
- `test_security_demo.py` - Test suite (6,869 chars)

### Modified Files:
- `web_app.py` - Added 3 endpoints and 2 helper functions (~200 lines)
- `templates/index.html` - Added security mode selector
- `templates/result.html` - Added security mode indicator
- `README.md` - Added security demo documentation section

## Key Features

### Detection & Logging
The app includes pattern-based detection that logs potential injection attempts:
```python
injection_patterns = [
    'ignore instructions', 'disregard', 'system override',
    'new instructions', 'you are now', 'forget everything',
    'pretend to be', 'act as', 'game mode', 'jailbreak'
]
```

### Input Sanitization
The secure mode includes:
- Length validation (max 500 chars)
- Character whitelisting (alphanumeric + basic punctuation)
- Pattern detection and blocking
- XML-style prompt boundaries

### Structured Prompts
Secure mode uses clear boundaries:
```xml
<system_instructions>
  You are a travel assistant. Only plan travel.
</system_instructions>

<user_travel_request>
  {sanitized user input}
</user_travel_request>
```

## Educational Value

This demonstration teaches:
- ✅ How prompt injection attacks work
- ✅ Common attack patterns and techniques
- ✅ Why direct string concatenation is dangerous
- ✅ How to identify vulnerable code
- ✅ Proper input validation and sanitization
- ✅ Defense-in-depth strategies for AI applications

## Testing

Run the test suite:
```bash
python test_security_demo.py
```

All tests pass:
- ✅ File Structure (6/6)
- ✅ Endpoint Definitions (5/5)
- ✅ Injection Detection (9/9)
- ✅ Input Sanitization (5/5)

## Security Summary

✅ **CodeQL Scan**: No vulnerabilities detected
✅ **Code Review**: All feedback addressed
✅ **Syntax Validation**: Passed
✅ **Test Suite**: 100% passing

## Important Disclaimer

⚠️ **This vulnerable endpoint is for EDUCATIONAL PURPOSES ONLY.**

**DO NOT** deploy the vulnerable endpoint to production. It intentionally contains security vulnerabilities to demonstrate how prompt injection attacks work.

The purpose is to help developers understand:
- What prompt injection is
- How to recognize it in code
- How to implement proper mitigations

Use this knowledge to build more secure AI applications! 🛡️
