# MCP Advanced (Server & Client)

Create and run an MCP server with custom tools, then implement an AI Agent with MCP Client that utilizes tools from the created server. 
This task demonstrates the full MCP workflow from server implementation to client integration.

## Learning Goals

By completing this task, you will learn:

- **MCP Protocol Implementation**: Understand the Model Context Protocol specification and JSON-RPC communication
- **Server-Side Tool Development**: Create custom tools that follow MCP standards
- **Client Integration**: Connect AI agents to MCP servers and handle tool execution
- **Session Management**: Implement proper session handling and state management
- **Streaming Responses**: Work with Server-Sent Events in Streamable HTTP for real-time communication
- **Error Handling**: Implement robust error handling in distributed systems

### If the task in the main branch is hard for you, switch to the `main-detailed` branch

---

## Task:

### 1. Create MCP Server:
1. Run User Service [root docker-compose](docker-compose.yml) (Optional step in case if you have it from previous tasks)
2. Open [mcp_server](mcp_server) and review mcp server structure:
   - in [models](mcp_server/models) persist implemented request and response models, details about request and response [official documentation](https://modelcontextprotocol.io/specification/2025-06-18/basic)
   - in [ums_mcp_server.py](mcp_server/ums_mcp_server.py) you need to implement parts described in `TODO` sections
   - in [tools](mcp_server/tools) you will find simple tools
   - lastly, in [server.py](mcp_server/server.py) provide implementations described in `TODO` sections
3. Run MCP server locally
4. Test it with Postman. Import [mcp_custom.postman_collection.json](mcp_custom.postman_collection.json) into postman. (`init` -> `init-notification` -> `tools/list` -> `tools/call`)

<details> 
<summary><b>Test in Postman</b></summary>

![postman.gif](postman-test.gif)

</details>

## 2. Create Agent
1. Provide implementation for the [app.py](agent/app.py) and run it locally with MCPClient
2. Test agent with queries below 👇
3. Provide implementations described in `TODO` sections for [custom_mcp_client.py](agent/clients/custom_mcp_client.py)
4. Test again agent with queries below 👇
```text
Check if Arkadiy Dobkin present as a user, if not then search info about him in the web and add him
```

---

## MCP Protocol Details

### JSON-RPC Structure

**Request Format:**
```json
{
  "jsonrpc": "2.0",
  "id": "unique-request-id",
  "method": "method_name",
  "params": {
    "parameter": "value"
  }
}
```

**Response Format:**
```json
{
  "jsonrpc": "2.0",
  "id": "matching-request-id",
  "result": {
    "data": "response_data"
  }
}
```

---

### MCP Session Flow

1. **Initialize**: Client sends `initialize` request
2. **Notification**: Client sends `notifications/initialized`
3. **Discovery**: Client calls `tools/list` to get available tools
4. **Operation**: Client calls `tools/call` with specific tool and arguments
5. **Shutdown**: `DELETE, {host}, Mcp-Session-Id: {Mcp-Session-Id}`, shutdown is not covered in this practice, but it's simple REST request

---

### Headers

- `Content-Type`: `application/json`
- `Accept`: `application/json, text/event-stream`
- `Mcp-Session-Id`: Session identifier (after initialization)

---

## Implementation Tips

### Custom MCP Client Implementation

1. **Error Handling**: Always check for HTTP session initialization
2. **Session Management**: Store and reuse session IDs properly
3. **SSE Parsing**: Look for `data:` prefixed lines, ignore `[DONE]`
4. **JSON-RPC Errors**: Check for `error` field in responses
5. **Content Extraction**: Tool results are in `result.content[0].text`

### Common Issues

- **Missing Accept Header**: Server requires both JSON and SSE accept types
- **Session ID Missing**: Most operations require a valid session ID
- **Tool Arguments**: Arguments must be properly formatted as per tool schema
- **Async Context**: Use proper async/await patterns for HTTP requests


## 📚 Additional Resources

- [MCP Specification](https://spec.modelcontextprotocol.io/)
- [JSON-RPC 2.0 Specification](https://www.jsonrpc.org/specification)
- [MCP Error Codes](https://www.mcpevals.io/blog/mcp-error-codes)
- [OpenAI Function Calling](https://platform.openai.com/docs/guides/function-calling)
