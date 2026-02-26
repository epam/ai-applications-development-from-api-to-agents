# MCP Fundamentals (Server & Client)

Python implementation for building Users Management Agent with MCP tools and MCP server

## Learning Goals

By exploring and working with this project, you will learn:

- How to configure simple MCP server
- How to configure client and connect to MCP server
- How to create simple Agent with tools from MCP server
- Key features of MCP

### If the task in the main branch is hard for you, switch to the `main-detailed` branch

![](flow.png)

---

# Tasks:

## HTTP

You need to implement the Users Management Agent, that will be able to perform CRUD operations within User Management
Service.

### 1. Create and run HTTP MCP server:

1. Run User Service [root docker-compose](docker-compose.yml) (Optional step in case if you have it from previous tasks)
2. Open [_server.py](mcp_server/_server.py) and implement all ***TODO***
3. Open [http_server.py](mcp_server/http_server.py) and **Run** it

<details> 
<summary><b>OPTIONAL: Work with HTTP MCP server in Postman</b></summary>

![postman_http.gif](postman_http.gif)

</details>

### 2. Create and run Agent:

1. Open [base mcp_client](agent/mcp_clients/base.py) and implement all ***TODO***
2. Open [HTTP mcp_client](agent/mcp_clients/http.py) and implement all ***TODO***
3. Open [agent.py](agent/agent.py) and implement all ***TODO***
4. Open [prompts](agent/prompts.py) and write System prompt
5. Open [app](agent/app.py) and implement all ***TODO***
6. Run application [app.py](agent/app.py) and test that it is connecting to MCP Server and works properly
7. Try with your solution with `fetch MCP` `https://remote.mcpservers.org/fetch/mcp` instead of http://localhost:8005/mcp

### OPTIONAL: Support both (users-management and fetch) MCP servers:

1. Remember that we have 1-to-1 connection between MCP client and MCP server!
2. You need to think of the way how to change current flow to support tools from different MCP servers and implement it
3. In the end you should have the Agent that is able to fetch the info from the WEB about some people and save it to
   Users Service
4. Hint: the problem place is [openai_client](agent/openai_client.py)

---

## STDIO

### 1. Create and run Agent with STDIO MCP Client:

1. Open [STDIO mcp_client](agent/mcp_clients/http.py) and implement all ***TODO***
2. Open [app](agent/app.py) and instead of HttpMCPClient client use this one:
    ```python
        async with StdioMCPClient(
                command=sys.executable,          # use the same venv Python, not bare "python"
                args=[str(STDIO_SERVER_PATH)],
                env={**os.environ, "PYTHONPATH": str(PROJECT_ROOT)}  # inherit env + add project root
        ) as mcp_client:
    ```
3. Run application [app.py](agent/app.py) and test that it is connecting to STDIO MCP Server and works properly

<details> 
<summary><b>Connecting Your STDIO MCP Server to Claude Desktop</b></summary>

This uses your `stdio_server.py` entry point — simplest and most reliable for local development.

### Step 1: Find Claude Desktop config file

| OS          | Path                                                              |
|-------------|-------------------------------------------------------------------|
| **macOS**   | `~/Library/Application Support/Claude/claude_desktop_config.json` |
| **Windows** | `%APPDATA%\Claude\claude_desktop_config.json`                     |

### Step 2: Edit the config

Open the file (create it if it doesn't exist) and add your server:

```json
{
  "mcpServers": {
    "users-management": {
      "command": "{ABSOLUTE_PATH}/ai-applications-development-from-api-to-agents/.venv/bin/python",
      "args": [
        "{ABSOLUTE_PATH}/ai-applications-development-from-api-to-agents/t9_mcp_fundamentals/mcp_server/stdio_server.py"
      ],
      "env": {
        "PYTHONPATH": "{ABSOLUTE_PATH}/ai-applications-development-from-api-to-agents"
      }
    }
  }
}
```

**Important notes:**

- Don't forget to replace `{ABSOLUTE_PATH}` with absolute path to the project on your local machine
- Set `PYTHONPATH` to your project root so imports like `t9_mcp_fundamentals` resolve correctly
- If you're using a virtual environment, point to its Python binary instead:
  ```json
  "command": "/path/to/your/venv/bin/python"
  ```
  On Windows: `"C:\\Users\\you\\project\\.venv\\Scripts\\python.exe"`


<details> 
<summary><b>Sample how it is done on my Mac:</b></summary>

```json
{
  "mcpServers": {
    "users-management": {
      "command": "/Users/pavlokhshanovskyi/dialx/courses/ai-applications-development-from-api-to-agents/.venv/bin/python",
      "args": [
        "/Users/pavlokhshanovskyi/dialx/courses/ai-applications-development-from-api-to-agents/t9_mcp_fundamentals/mcp_server/stdio_server.py"
      ],
      "env": {
        "PYTHONPATH": "/Users/pavlokhshanovskyi/dialx/courses/ai-applications-development-from-api-to-agents"
      }
    }
  }
}
```

![claude_stdio.gif](claude_stdio.gif)
</details>

### Step 3: Restart Claude Desktop

Fully quit and reopen Claude Desktop. While reopen Claude can ask access to project. In connectors section you will be able to find users-management

</details>

<details> 
<summary><b>Play in Postman with your STDIO MCP Server</b></summary>

Configuration is the same as you have for Claude 👆

![postman_stdio.gif](postman_stdio.gif)

</details> 


### 2. Play with STDIO MCP Servers from docker images:

1. Use such mcp_client:
    ```python
    async with StdioMCPClient(docker_image="mcp/duckduckgo:latest") as mcp_client:
    ```
2. It is an MCP Server with WEB Search capabilities, [source code](https://github.com/khshanovskyi/duckduckgo-mcp-server)
3. Try to search `Wthat is the weather in Kyiv now?`