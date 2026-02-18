# LLMs Output Tuning

In this task, you will experiment with output tuning parameters across different AI providers. The goal is to understand
how parameters like temperature, top_p, structured output, reasoning/thinking, and others affect model responses.

---

🚨 The task is the same as in `main` branch 🚨

---

## Task

### 1. OpenAI Chat Completions
Open [openai_chat_completions_task.py](openai_chat_completions_task.py) and follow TODO 1–10:
- `n`, `temperature`, `top_p`, `max_tokens`, `stop`
- `response_format` (structured JSON output with `json_schema`)
- `frequency_penalty`, `presence_penalty`, `seed`
- `reasoning_effort` (extended thinking)

Parameters are passed as kwargs to `run()`.

### 2. OpenAI Responses API
Open [openai_responses_task.py](openai_responses_task.py) and follow TODO 1–8.

Key differences from Chat Completions:
- `max_tokens` → `max_output_tokens`
- `response_format` → `text` with format object
- `reasoning_effort` → `reasoning={"effort": "..."}`
- New: `instructions` (replaces system message), `store` + `previous_response_id`, `truncation`, `metadata`

Parameters are passed as kwargs to `run()`.

### 3. Anthropic (Optional)
Open [anthropic_task.py](anthropic_task.py) and follow TODO 1–6:
- `temperature`, `top_p`, `top_k`, `stop_sequences`
- `output_config` (structured JSON output)
- `thinking` (extended thinking with budget)

Parameters are passed as kwargs to `run()`.

### 4. Gemini (Optional)
Open [gemini_task.py](gemini_task.py) and follow TODO 1–6:
- `temperature`, `topP`, `topK`, `maxOutputTokens`
- `responseMimeType` + `responseSchema` (structured output)
- `thinkingConfig` (extended thinking with budget)

All parameters must be passed inside `generationConfig={...}`.