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

Then implement the web search tool in **[task/tools/web_search.py](task/tools/web_search.py)** — it calls an OpenAI search model to answer web queries on the agent's behalf.

---

### 2. Implement the OpenAI agent — [task/agents/openai.py](task/agents/openai.py)

Extend `BaseAgent` ([task/agents/_base.py](task/agents/_base.py)) to call the **OpenAI Chat Completions API**. The agentic loop:

1. Send the conversation + tools to the API
2. If `finish_reason == "tool_calls"` — execute each requested tool and append the results as `tool` messages
3. Recurse until the model returns a plain text response (`finish_reason == "stop"`)

See the **OpenAI API Reference** section at the bottom for the exact request/response shapes.

---

### 3. Write the system prompt — [task/prompts.py](task/prompts.py)

Define a `SYSTEM_PROMPT` that tells the agent its role, which tools it has, and how it should behave (e.g. confirm before deleting, use web search when creating users).

---

### 4. Wire everything up — [task/app.py](task/app.py)

Instantiate `UserServiceClient`, create all tools, create `OpenAIBasedAgent` with `system_prompt`, and run the conversation loop. Try the following sample inputs:
- `Add Andrej Karpathy as a new user`
- `Find all female users`
- `Delete user with id 3`

---

### 5. Implement the Anthropic agent — [task/agents/anthropic.py](task/agents/anthropic.py)

Extend `BaseAgent` again, this time for the **Anthropic Messages API**. Key differences from OpenAI:

- Auth uses `x-api-key` + `anthropic-version: 2023-06-01` headers (no `Bearer` prefix)
- System prompt is a top-level `system` field — not part of the messages array
- Tool schema uses `anthropic_schema` format (`name` / `description` / `input_schema`)
- Response `content` is a list of typed blocks (`"text"` or `"tool_use"`)
- Stop signal is `stop_reason == "tool_use"` (not `"tool_calls"`)
- Tool inputs arrive as a dict (`block["input"]`) — no `json.loads()` needed
- Tool results go back as a `user` message whose content is a list of `"tool_result"` blocks; multiple results must be grouped into a single user turn

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
