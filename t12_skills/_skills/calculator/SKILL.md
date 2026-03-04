---
name: calculator
description: >
  Performs precise mathematical calculations: arithmetic, exponentiation,
  square roots, trigonometry, floor division, and modulo.
  Use when the user asks to calculate, compute, evaluate, or solve any
  numeric expression or math problem.
---

# Calculator (With Script)

## Quick Start

```bash
python /skills/calculator/scripts/calculate.java "<expression>"
```

## Supported Operations

- Arithmetic: `+`, `-`, `*`, `/`
- Power: `**` or `^` (both accepted)
- Square root: `sqrt(x)`
- Floor division: `//`, modulo: `%`
- Trig: `sin(x)`, `cos(x)`, `tan(x)`
- Constants: `pi`, `e`
- Grouping: `(2 + 3) * 4`

## Workflow

1. Parse the expression from the user's question
2. Run: `python /skills/calculator/scripts/calculate.py "<expression>"`
3. Return the script output as-is
4. On error (division by zero, bad syntax), explain what went wrong clearly