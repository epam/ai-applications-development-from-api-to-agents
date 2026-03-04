---
name: unit-converter
description: >
  # TODO: Write when the agent should activate this skill.
  # Cover: what unit categories it handles and what user actions trigger it.
license: Apache-2.0
metadata:
  author: ai-powered-apps-development-expert
  version: "1.0"
allowed-tools: execute_code
---

# Unit Converter

<!--
TODO: Fill in the workflow for the agent. The script is at scripts/convert.py.
See references/how-code-execution-works.md to understand how execute_code works.
See examples.md for invocation examples and supported units.

## Workflow

### Step 1: Load the script (first call, session_id = "")
Call execute_code with script_path, the conversion code, and session_id = "".
Save the returned session_id for reuse.

### Step 2: Write the conversion call
Pass as code: call convert_units(value, from_unit, to_unit) and print Category, Input, Result.

### Step 3: Return output
Return the printed output as-is.

### Step 4: Reuse session
On follow-up conversions skip Step 1 — pass only code + saved session_id.

### Step 5: Error handling
Unknown unit / incompatible categories: report the error and list supported units from examples.md.
Invalid number: ask to clarify. Expired session: silently restart from Step 1.
-->