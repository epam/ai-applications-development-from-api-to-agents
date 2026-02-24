# AI Simple Agent Task
Python implementation for building AI-powered chat applications using the OpenAI and Anthropic API with advanced tool integration.

## App Architecture

![](flow.png)

---

## Task

Implement a simple Agent from scratch that works with a User Service. You will practice defining custom tools and driving the agentic loop via the OpenAI and Anthropic APIs.

### If the task in the main branch is hard for you, switch to the `main-detailed` branch

---

### 0. Run [docker-compose.yml](docker-compose.yml) with User Service (can be ignored if it still running from t6_grounding)
The mock user service runs on `localhost:8041` and provides several REST endpoints:
- `GET /v1/users` — list all users
- `GET /v1/users/{id}` — get a specific user
- `GET /v1/users/search` — search users by fields
- `POST /v1/users` — create a user
- `PUT /v1/users/{id}` — update a user
- `DELETE /v1/users/{id}` — delete a user
- `GET /health` — service health check
- Swagger UI 👉 http://localhost:8041/docs
- Use [mock-user-service.postman_collection.json](mock-user-service.postman_collection.json) in Postman to play with API

---

### 1. Implement the tools — [task/tools/](task/tools/)

Each tool extends `BaseTool` ([task/tools/base.py](task/tools/base.py)) and must implement three properties (`name`, `description`, `input_schema`) and one method (`execute`). The `input_schema` follows JSON Schema and is shared by both the OpenAI and Anthropic schema builders already provided in `BaseTool`.

Start with the User Service tools in [task/tools/users/](task/tools/users/). Each one wraps a single User Service endpoint:

- **[get_user_by_id_tool.py](task/tools/users/get_user_by_id_tool.py)** — fetch a user by numeric ID
- **[search_users_tool.py](task/tools/users/search_users_tool.py)** — search users by name / surname / email / gender
- **[create_user_tool.py](task/tools/users/create_user_tool.py)** — create a new user record
- **[update_user_tool.py](task/tools/users/update_user_tool.py)** — update an existing user record
- **[delete_user_tool.py](task/tools/users/delete_user_tool.py)** — delete a user by ID

Then implement the web search tool in **[task/tools/web_search.py](task/tools/web_search.py)** — it calls the OpenAI Responses API (`gpt-5.2` with `tools: [{"type": "web_search"}]`) and extracts the result from the `output_text` block in the response.

---

### 2. Implement `BaseAgent` — [task/agents/_base.py](task/agents/_base.py)

Implement `__init__`:
- Validate `api_key` (raise `ValueError` if empty or blank)
- Assign `self._model`, `self._api_key`, `self._system_prompt`
- Build `self._tools_dict` as `{tool.name: tool}` for fast lookup during execution

`get_response` is abstract — you will implement it in the provider-specific subclasses below.

---

### 3. Implement the OpenAI agent — [task/agents/openai.py](task/agents/openai.py)

Extend `BaseAgent` to call the **OpenAI Chat Completions API**. Implement four methods:

- **`__init__`** — format `api_key` as a Bearer token, build `_tools_schemas` using `tool.openai_schema`, set `_endpoint`
- **`get_response`** — build the request payload (prepend system message locally, not stored in `messages`), POST to the API, parse the response; if `finish_reason == "tool_calls"` append the assistant message + tool results to `messages` and recurse; otherwise return the final `Message`
- **`_process_tool_calls`** — for each tool call extract `id`, `function.name`, parse `function.arguments` with `json.loads`, call `_call_tool`, return a list of `TOOL` messages
- **`_call_tool`** — look up the tool in `_tools_dict` and call `execute`, or return an unknown-function error string

See the **OpenAI API Reference** section at the bottom for the exact request/response shapes.

---

### 4. Write the system prompt — [task/prompts.py](task/prompts.py)

Define a `SYSTEM_PROMPT` that tells the agent its role, which tools it has, and how it should behave (e.g. confirm before deleting, use web search when creating users).

---

### 5. Wire everything up — [task/app.py](task/app.py)

Implement `main()`:
- Create `UserServiceClient` and all tools
- Create `OpenAIBasedAgent` with `system_prompt`
- Create `Conversation` and run the input loop: read user input, add it to the conversation, call `agent.get_response`, add the reply and print it

Try the following sample inputs:
- `Add Andrej Karpathy as a new user`
- `Find all female users`
- `Delete user with id 3`

---

### 6. Implement the Anthropic agent — [task/agents/anthropic.py](task/agents/anthropic.py)

Extend `BaseAgent` for the **Anthropic Messages API**. Implement five methods:

- **`__init__`** — set `_endpoint`, build `_tools_schemas` using `tool.anthropic_schema` (flat format, no `"type": "function"` wrapper)
- **`get_response`** — build headers (`x-api-key`, `anthropic-version: 2023-06-01`), add `system` as a top-level field (not inside messages), POST to the API; if `stop_reason == "tool_use"` append messages and recurse; otherwise return the final `Message`
- **`_to_anthropic_messages`** — convert the internal `Message` list to Anthropic format: group consecutive `TOOL` messages into a single user message with `tool_result` blocks; replay full content blocks for `AI` messages that had tool calls
- **`_process_tool_calls`** — same as OpenAI but `block["input"]` is already a dict (no `json.loads` needed)
- **`_call_tool`** — identical to the OpenAI agent

Key differences from OpenAI summarised:

| | OpenAI | Anthropic |
|---|---|---|
| Auth header | `Authorization: Bearer ...` | `x-api-key: ...` + `anthropic-version` |
| System prompt | message with `role: system` | top-level `system` field |
| Tool schema | `openai_schema` (`parameters`) | `anthropic_schema` (`input_schema`) |
| Stop signal | `finish_reason: "tool_calls"` | `stop_reason: "tool_use"` |
| Tool input | JSON string → `json.loads` | dict directly (`block["input"]`) |
| Tool results | separate `tool` messages | grouped into one `user` message |

Switch `app.py` to `AnthropicBasedAgent` and run the same queries.

See the **Anthropic API Reference** section below for the exact request/response shapes.

---

## OpenAI Chat Completions API Reference

📖 Full docs: https://developers.openai.com/api/reference/resources/chat/subresources/completions/methods/create
🔧 Tool calling guide: https://developers.openai.com/api/docs/guides/function-calling

### Request Format
```json
{
  "model": "gpt-5.2",
  "system": "You are a helpful assistant.",
  "messages": [
    {
      "role": "system",
      "content": "You are a helpful assistant."
    },
    {
      "role": "user",
      "content": "Who is Andrej Karpathy?"
    }
  ],
  "tools": [
    {
      "type": "function",
      "function": {
        "name": "web_search_tool",
        "description": "Tool for WEB searching.",
        "parameters": {
          "type": "object",
          "properties": {
            "request": {
              "type": "string",
              "description": "The search query or question to search for on the web"
            }
          },
          "required": [
            "request"
          ]
        }
      }
    },
    {
      "type": "function",
      "function": {
        "name": "get_user_by_id",
        "description": "Provides full user information",
        "parameters": {
          "type": "object",
          "properties": {
            "id": {
              "type": "number",
              "description": "User ID"
            }
          },
          "required": [
            "id"
          ]
        }
      }
    },
    ...
  ]
}
```

### Response — with tool calls
```json
{
  "choices": [
    {
      "message": {
        "role": "assistant",
        "content": "",
        "tool_calls": [
          {
            "id": "call_6JriK7u5DL2heJ1lkw08WUFd",
            "function": {
              "arguments": "{\"request\":\"Andrej Karpathy profile\"}",
              "name": "web_search_tool"
            },
            "type": "function"
          }
        ]
      },
      "finish_reason": "tool_calls"
    }
  ]
}
```

### Tool result message (added to the conversation before the next call)
```json
{
  "role": "tool",
  "tool_call_id": "call_6JriK7u5DL2heJ1lkw08WUFd",
  "name": "web_search_tool",
  "content": "Andrej Karpathy is a Slovak-Canadian computer scientist..."
}
```

### Response — final answer
```json
{
  "choices": [
    {
      "message": {
        "role": "assistant",
        "content": "Andrej Karpathy is..."
      },
      "finish_reason": "stop"
    }
  ]
}
```

---

## Anthropic Messages API Reference

📖 Full docs: https://platform.claude.com/docs/en/api/messages/create
🔧 Tool calling guide: https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview

### Request Format
```json
{
  "model": "claude-sonnet-4-5",
  "max_tokens": 8096,
  "system": "You are a helpful assistant.",
  "messages": [
    {
      "role": "user",
      "content": "Who is Andrej Karpathy?"
    }
  ],
  "tools": [
    {
      "name": "web_search_tool",
      "description": "Tool for WEB searching.",
      "input_schema": {
        "type": "object",
        "properties": {
          "request": {
            "type": "string",
            "description": "The search query or question to search for on the web"
          }
        },
        "required": [
          "request"
        ]
      }
    },
    {
      "name": "get_user_by_id",
      "description": "Provides full user information",
      "input_schema": {
        "type": "object",
        "properties": {
          "id": {
            "type": "number",
            "description": "User ID"
          }
        },
        "required": [
          "id"
        ]
      }
    },
    ...
  ]
}
```

### Response — with tool calls
```json
{
  "role": "assistant",
  "content": [
    {
      "type": "text",
      "text": "I'll search for information about Andrej Karpathy."
    },
    {
      "type": "tool_use",
      "id": "toolu_01A09q90qw90lq917835lq9",
      "name": "web_search_tool",
      "input": {
        "request": "Andrej Karpathy profile"
      }
    }
  ],
  "stop_reason": "tool_use"
}
```

### Sending the assistant turn + tool results back (one user message per round)
```json
{
  "role": "assistant",
  "content": [
    {
      "type": "text",
      "text": "I'll search for information about Andrej Karpathy."
    },
    {
      "type": "tool_use",
      "id": "toolu_01A09q90qw90lq917835lq9",
      "name": "web_search_tool",
      "input": { "request": "Andrej Karpathy profile" }
    }
  ]
},
{
  "role": "user",
  "content": [
    {
      "type": "tool_result",
      "tool_use_id": "toolu_01A09q90qw90lq917835lq9",
      "content": "Andrej Karpathy is a Slovak-Canadian computer scientist..."
    }
  ]
}
```

### Response — final answer
```json
{
  "role": "assistant",
  "content": [
    {
      "type": "text",
      "text": "Andrej Karpathy is..."
    }
  ],
  "stop_reason": "end_turn"
}
```
