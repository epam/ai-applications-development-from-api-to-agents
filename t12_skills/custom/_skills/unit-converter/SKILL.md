---
name: unit-converter
description: >
  Converts values between units of measurement across categories: length (km, miles,
  feet, inches), weight (kg, lbs, oz, stone), temperature (Celsius, Fahrenheit, Kelvin),
  volume (liters, gallons, cups, ml), area (m², acres, ft²), speed (km/h, mph, knots),
  time (seconds to years), data storage (bytes to petabytes), pressure, and energy.
  Use when the user asks to convert, calculate, or express a measurement in different units.
license: Apache-2.0
metadata:
  author: ai-powered-apps-development-expert
  version: "1.0"
allowed-tools: execute_code
---

# Unit Converter

For usage examples see [examples.md](examples.md).
For details on how `execute_code` works see [references/how-code-execution-works.md](references/how-code-execution-works.md).
Script with convertor see [scripts/convert.py](scripts/convert.py).


## Workflow

### Step 1: Load the script (first call only, session_id = "")

Use `read_skill` to get the content of `scripts/convert.py`, then call `execute_code` with:
- `script_path = "unit-converter/scripts/convert.py"` — the tool will read the file and prepend its content before your `code` (combined as `<script content>` + `\n\n` + `code`)
- `code` — the conversion call you want to run (see Step 2)
- `session_id = ""` — empty string to create a new session

> **Why `script_path`?** Saves tokens — you don't need to copy the script code into the request. The tool loads it from disk automatically.

You will get `session_id` in the response and must reuse it for every subsequent call in this conversation.

### Step 2: Write the conversion call (code parameter)

Pass as `code` the conversion call for the user's request:

```python
result, category = convert_units(<value>, "<from_unit>", "<to_unit>")
print(f"Category: {category}")
print(f"Input:    {fmt(<value>)} <from_unit>")
print(f"Result:   {fmt(result)} <to_unit>")
```

Replace `<value>`, `<from_unit>`, `<to_unit>` with the parsed values from the user's request.

On the **first call** this `code` is passed together with `script_path` (Step 1) — the tool combines them into one execution.
On **subsequent calls** omit `script_path` and just pass `code` with the saved `session_id` — the script is already loaded in the session.

### Step 3: Return output

Return the printed output as-is. Do not reformat or paraphrase the numbers.

### Step 4: Reuse session for follow-up conversions

If the user asks another conversion in the same conversation, skip Step 1 — the script is already loaded in the session. Call `execute_code` with only `code` and the saved `session_id`.

### Step 5: Error handling

- Unknown unit or incompatible categories: report the error message from the script and list the supported units for the relevant category (see examples.md).
- Invalid number: ask the user to clarify.
- Session expired (`session_id` no longer valid): silently restart from Step 1.