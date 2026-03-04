# MCP Python Code Interpreter

A stateful Python code execution environment with Jupyter kernel support, built on the Model Context Protocol (MCP). Execute Python code with persistent state, automatic visualization handling, and secure session management.

## Features

- **Stateful Execution**: Variables, imports, and state persist across multiple code executions within a session
- **Jupyter Kernel Backend**: Full Jupyter kernel support with IPython features
- **Session Management**: Secure session IDs with automatic 30-minute timeout
- **Visualization Support**: Automatic capture and export of matplotlib, seaborn, and Plotly figures
- **File Generation**: Access generated files (images, data files, plots) via MCP resources
- **Scientific Computing**: Pre-configured with pandas, numpy, matplotlib, seaborn, plotly, and sympy
- **Automatic Cleanup**: Background task removes expired sessions and orphaned files

---

## Architecture

```
┌─────────────────┐
│  MCP Client     │
│  (Claude, etc)  │
└────────┬────────┘
         │
         │ MCP Protocol
         │
┌────────▼────────┐
│    MCP Server   │
│  (server.py)    │
└────────┬────────┘
         │
         │ Manages
         │
┌────────▼────────┐
│ Session Manager │
│ - Create/Track  │
│ - Cleanup       │
└────────┬────────┘
         │
         │ Controls
         │
┌────────▼────────┐
│ Jupyter Kernels │
│ (per session)   │
└─────────────────┘
```

---

## Usage

The server exposes three tools and a resource endpoint for file access.

### 1. Execute Code

Execute Python code in a persistent Jupyter kernel environment.

**First execution (creates new session):**
```python
{
  "code": "import pandas as pd\nx = 42\nprint('Hello, World!')",
  "session_id": ""  # Empty string or "0" for new session
}
```

**Response:**
```json
{
  "success": true,
  "output": ["Hello, World!\n"],
  "result": null,
  "session_info": {
    "session_id": "abc123xyz456",
    "instructions": "Use this `session_id` in subsequent requests..."
  }
}
```

**Subsequent executions (reuse session):**
```python
{
  "code": "print(x * 2)  # Variable persists from previous execution",
  "session_id": "abc123xyz456"
}
```

### 2. Create Visualizations

Matplotlib, seaborn, and Plotly figures are automatically captured and saved.

```python
{
  "code": """
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 10, 100)
plt.plot(x, np.sin(x))
plt.title('Sine Wave')
plt.savefig('sine_wave.png')
plt.show()
""",
  "session_id": "abc123xyz456"
}
```

**Response includes file references:**
```json
{
  "success": true,
  "output": ["📊 File created: sine_wave.png (image/png, 45231 bytes)"],
  "files": [
    {
      "uri": "kernel://abc123xyz456/sine_wave.png",
      "mime_type": "image/png",
      "name": "sine_wave.png",
      "size": 45231
    }
  ]
}
```

### 3. List Session Files

```python
{
  "session_id": "abc123xyz456"
}
```

### 4. Clear Session

Manually remove a session and all its files:

```python
{
  "session_id": "abc123xyz456"
}
```

### 5. Access Files

Files are accessed via the MCP resource protocol:

```
kernel://{session_id}/{filename}
```

Example: `kernel://abc123xyz456/sine_wave.png`

---

## Session Management

### Session Lifecycle

1. **Creation**: First call with empty `session_id` generates a secure 16-character ID
2. **Active**: Session remains active while being used
3. **Timeout**: Sessions expire after **30 minutes of inactivity**
4. **Cleanup**: Expired sessions are automatically removed (background task runs every 5 minutes)

### Session Expiration

If you try to use an expired session, you'll receive a `SessionExpiredError`:

```json
{
  "success": false,
  "error": "SessionExpiredError: Session abc123xyz456 not found or has expired...",
  "traceback": []
}
```

**Solution**: Create a new session and re-execute your setup code.

---

## Available Libraries

The following libraries are pre-installed:

- **Data Science**: pandas, numpy
- **Visualization**: matplotlib, seaborn, plotly, kaleido
- **Mathematics**: sympy
- **Jupyter**: ipykernel, jupyter-client

---

## API Reference

### Tools

#### `execute_code`

Execute Python code in a persistent Jupyter kernel environment.

**Parameters:**
- `code` (str): Python code to execute (multi-line supported)
- `session_id` (str, optional): Session identifier (empty or "0" for new session)

**Returns:**
- `success` (bool): Execution status
- `output` (list): stdout/stderr text
- `result` (str|None): Last expression value
- `error` (str|None): Error message if failed
- `traceback` (list): Full traceback if error
- `files` (list): File references with URIs
- `session_info` (dict|None): Session info for new sessions

#### `list_session_files`

List all files generated in a session.

**Parameters:**
- `session_id` (str): Session identifier

**Returns:**
- `session_id` (str): The session ID
- `files` (list): List of file references
- `error` (str): Error message if session not found

#### `clear_session`

Manually clear a session and shutdown its kernel.

**Parameters:**
- `session_id` (str): Session identifier to clear

**Returns:**
- `success` (bool): Operation status
- `message` (str): Status message

### Resources

#### `kernel://{session_id}/{filename}`

Retrieve file content from a session.

**URI Format:** `kernel://session_id/filename`

**Returns:** File content (binary for images, text for text files)