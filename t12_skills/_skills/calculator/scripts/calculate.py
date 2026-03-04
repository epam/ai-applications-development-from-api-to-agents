#!/usr/bin/env python3
"""
Safe math expression evaluator using AST parsing.
No eval() on raw strings — only whitelisted operations are allowed.
Usage: python calculate.py "<expression>"
"""

import sys
import math
import ast

SAFE_NAMES = {
    "sqrt": math.sqrt, "abs": abs, "round": round,
    "floor": math.floor, "ceil": math.ceil,
    "log": math.log, "log10": math.log10,
    "sin": math.sin, "cos": math.cos, "tan": math.tan,
    "pi": math.pi, "e": math.e,
}

ALLOWED_NODES = (
    ast.Expression, ast.BinOp, ast.UnaryOp, ast.Num, ast.Constant,
    ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Pow, ast.Mod,
    ast.FloorDiv, ast.USub, ast.UAdd, ast.Call, ast.Name, ast.Load,
)


def safe_eval(expression: str) -> float:
    expression = expression.replace("^", "**")
    try:
        tree = ast.parse(expression, mode="eval")
    except SyntaxError as e:
        raise ValueError(f"Invalid syntax: {e}")
    for node in ast.walk(tree):
        if not isinstance(node, ALLOWED_NODES):
            raise ValueError(f"Unsafe operation: {type(node).__name__}")
        if isinstance(node, ast.Name) and node.id not in SAFE_NAMES:
            raise ValueError(f"Unknown name '{node.id}'")
    return eval(compile(tree, "<expr>", "eval"), {"__builtins__": {}}, SAFE_NAMES)


def main():
    if len(sys.argv) < 2:
        print("Usage: python calculate.py \"<expression>\"")
        sys.exit(1)
    expression = " ".join(sys.argv[1:])
    try:
        result = safe_eval(expression)
        fmt = str(int(result)) if isinstance(result, float) and result.is_integer() else f"{result:.10g}"
        print(f"Expression: {expression}")
        print(f"Result: {fmt}")
    except ZeroDivisionError:
        print(f"Error: Division by zero in: {expression}")
        sys.exit(1)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()