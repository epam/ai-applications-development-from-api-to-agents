# MCP Advanced (Server & Client)

Create and run an MCP server with custom tools, then implement an AI Agent with MCP Client that utilizes tools from the created server.
This task demonstrates the full MCP workflow from server implementation to client integration.

The task uses the **stateless** MCP protocol version [2026-07-28](https://modelcontextprotocol.io/specification/2026-07-28):
there is no `initialize` handshake and no session. Every request is self-contained.

## Learning Goals

By completing this task, you will learn:

- **MCP Protocol Implementation**: Understand the Model Context Protocol specification and JSON-RPC communication
- **Stateless MCP**: Understand how every request carries its protocol version and client capabilities instead of relying on a session
- **Server-Side Tool Development**: Create custom tools that follow MCP standards
- **Client Integration**: Connect AI agents to MCP servers and handle tool execution
- **Streamable HTTP Transport**: Work with request metadata headers and Server-Sent Events responses
- **Error Handling**: Implement robust error handling in distributed systems

---

## Task:

### 1. Create MCP Server:
1. Run [docker-compose](docker-compose.yml) (`docker compose up -d`). It starts the User Service and the `ddg-mcp-server` (MCP server with WEB Search capabilities, available at http://localhost:8010/mcp)
2. Open [mcp_server](mcp_server) and review mcp server structure:
   - in [models](mcp_server/models) persist implemented request and response models, details about request and response [official documentation](https://modelcontextprotocol.io/specification/2026-07-28/basic)
   - in [ums_mcp_server.py](mcp_server/ums_mcp_server.py) you need to implement parts described in `TODO` sections
   - in [tools](mcp_server/tools) you will find simple tools
   - lastly, in [server.py](mcp_server/server.py) provide implementations described in `TODO` sections
3. Run MCP server locally
4. Test it with Postman. Import [mcp_custom.postman_collection.json](mcp_custom.postman_collection.json) into postman. (`server/discover` -> `tools/list` -> `tools/call`). There is no session, so you can send the requests in any order

<details> 
<summary><b>Test in Postman</b></summary>

![postman.gif](postman-test.gif)

</details>

## 2. Create Agent
1. Run [app.py](agent/app.py) and test it locally with MCPClient
2. Test agent with queries below 👇
3. Provide implementations described in `TODO` sections for [custom_mcp_client.py](agent/clients/custom_mcp_client.py) and for [app.py](agent/app.py)
4. Test again agent with queries below 👇
```text
Check if Arkadiy Dobkin present as a user, if not then search info about him in the web and add him
```

---

## MCP Protocol Details

### JSON-RPC Structure

**Request Format.** Every request carries the protocol version, client info and client capabilities in `params._meta`:
```json
{
  "jsonrpc": "2.0",
  "id": "unique-request-id",
  "method": "method_name",
  "params": {
    "parameter": "value",
    "_meta": {
      "io.modelcontextprotocol/protocolVersion": "2026-07-28",
      "io.modelcontextprotocol/clientInfo": {"name": "my-client", "version": "1.0.0"},
      "io.modelcontextprotocol/clientCapabilities": {}
    }
  }
}
```

**Response Format.** Every result has `resultType` and identifies the server in `_meta`:
```json
{
  "jsonrpc": "2.0",
  "id": "matching-request-id",
  "result": {
    "data": "response_data",
    "resultType": "complete",
    "_meta": {
      "io.modelcontextprotocol/serverInfo": {"name": "my-server", "version": "1.0.0"}
    }
  }
}
```

---

### MCP Request Flow

1. **Discovery** (optional): Client calls `server/discover` to get the server's supported protocol versions, capabilities and server info
2. **Tools**: Client calls `tools/list` to get available tools
3. **Operation**: Client calls `tools/call` with specific tool and arguments

Each request is a separate HTTP POST. The server keeps no state between requests, so there is nothing to initialize or shut down.

---

### What changed compared to the stateful version (2025-11-25)

| Topic                    | 2025-11-25 (stateful)                                     | 2026-07-28 (stateless)                                                          |
|--------------------------|-----------------------------------------------------------|---------------------------------------------------------------------------------|
| Handshake                | `initialize` + `notifications/initialized`                | None (optional `server/discover`)                                               |
| Session                  | `Mcp-Session-Id` header                                   | None                                                                            |
| Protocol version         | Negotiated once in `initialize`                           | In every request: `_meta` + `MCP-Protocol-Version` header                       |
| Client info/capabilities | Sent once in `initialize`                                 | In every request `_meta`                                                        |
| Server info              | `initialize` result                                       | `_meta` of every result and `server/discover`                                   |
| Results                  | Any JSON object                                           | `resultType` is required; `tools/list` and `server/discover` add `ttlMs` and `cacheScope` |
| HTTP GET / DELETE        | Standalone SSE stream / session termination               | Removed (`405 Method Not Allowed`)                                              |

---

### Headers

- `Content-Type`: `application/json`
- `Accept`: `application/json, text/event-stream`
- `MCP-Protocol-Version`: Protocol version. Must match `_meta["io.modelcontextprotocol/protocolVersion"]`
- `Mcp-Method`: JSON-RPC method. Must match `method`
- `Mcp-Name`: Tool name, only for `tools/call`. Must match `params.name` (values that are not plain ASCII are sent as `=?base64?{value}?=`)

---

### Errors

| HTTP status | JSON-RPC code             | When                                                                                     |
|-------------|---------------------------|------------------------------------------------------------------------------------------|
| 403         | `-32600`                  | `Origin` header is present and not allowed (protection against DNS rebinding)             |
| 406         | `-32600`                  | Client doesn't accept both `application/json` and `text/event-stream`                     |
| 400         | `-32602`                  | Required `_meta` field (`protocolVersion`, `clientCapabilities`) is missing               |
| 400         | `-32020` HeaderMismatch   | `MCP-Protocol-Version`, `Mcp-Method` or `Mcp-Name` header is missing or doesn't match body |
| 400         | `-32022` UnsupportedProtocolVersion | Protocol version is not supported, `error.data.supported` lists supported versions |
| 404         | `-32601`                  | Method not found                                                                         |
| 200         | `-32602`                  | Unknown tool (JSON-RPC error in the response)                                            |
| 200         | `result.isError: true`    | Tool execution error (the LLM can read it and retry)                                     |

---

## Implementation Tips

### Custom MCP Client Implementation

1. **No Session**: Add `_meta` with protocol version, client info and client capabilities to `params` of every request
2. **Headers**: Mirror protocol version, method and tool name into `MCP-Protocol-Version`, `Mcp-Method` and `Mcp-Name`
3. **Response Types**: The server decides per request whether to answer with `application/json` or `text/event-stream`. Support both
4. **SSE Parsing**: Look for `data:` prefixed lines, skip `event:` lines and comments. The message with `id` is the response (notifications may come before it)
5. **JSON-RPC Errors**: Check for `error` field in responses
6. **Content Extraction**: Tool results are in `result.content[0].text`

### Common Issues

- **Missing Accept Header**: Server requires both JSON and SSE accept types
- **Missing or Mismatched Headers**: `MCP-Protocol-Version`, `Mcp-Method` and `Mcp-Name` must match the body, otherwise `400` with `-32020`
- **Missing `_meta`**: Every request needs protocol version and client capabilities, otherwise `400` with `-32602`
- **Tool Arguments**: Arguments must be properly formatted as per tool schema
- **Async Context**: Use proper async/await patterns for HTTP requests

### Out of Scope

The custom server and client implement the core of the protocol that is needed for tools. These 2026-07-28 features are not implemented:
[Multi Round-Trip Requests](https://modelcontextprotocol.io/specification/2026-07-28/basic/patterns/mrtr) (`resultType: "input_required"`),
[subscriptions/listen](https://modelcontextprotocol.io/specification/2026-07-28/basic/patterns/subscriptions),
[`x-mcp-header`](https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/streamable-http#custom-headers-from-tool-parameters),
pagination, resources and prompts.


## Additional Resources

- [MCP Specification 2026-07-28](https://modelcontextprotocol.io/specification/2026-07-28)
- [Key Changes in 2026-07-28](https://modelcontextprotocol.io/specification/2026-07-28/changelog)
- [Streamable HTTP Transport](https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/streamable-http)
- [JSON-RPC 2.0 Specification](https://www.jsonrpc.org/specification)
- [MCP Error Codes](https://modelcontextprotocol.io/specification/2026-07-28/basic/index#error-codes)
- [OpenAI Function Calling](https://developers.openai.com/api/docs/guides/function-calling)
