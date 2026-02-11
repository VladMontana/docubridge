# docubridge 

> MCP server for instant access to your local documentation libraries

**docubridge** is a [Model Context Protocol (MCP)](https://modelcontextprotocol.io) server that gives AI assistants (like Qwen, Claude, etc.) direct access to documentation you specify. Instead of the model guessing or hallucinating API details — it reads the actual docs.

---

## Why?

When working with an LLM in your terminal, the model doesn't know:
- which version of FastAPI you're using
- what your internal project docs say
- any documentation you've added yourself

**docubridge** solves this by exposing your local Markdown documentation as MCP tools — the model can list, read, and search through them on demand.

---

## Features

| Tool | Description |
|---|---|
| `list_libraries` | Show all available documentation libraries |
| `list_files` | List all files inside a specific library |
| `get_file` | Read the full content of a specific file |
| `search_docs` | Search by keyword across all docs or within a library |

---

## Project Structure

```
mcp-docs-server/
├── pyproject.toml
├── .env
├── README.md
└── src/
    └── docs_server/
        ├── __init__.py
        ├── main.py
        ├── server.py
        ├── config.py
        └── reader.py
```

---

## Installation

```bash
git clone https://github.com/yourname/docubridge.git
cd docubridge
pip install -e .
```

---

## Adding Documentation

Clone any documentation that has Markdown sources. For example, FastAPI:

```bash
git clone --depth=1 --filter=blob:none --sparse https://github.com/fastapi/fastapi.git
cd fastapi
git sparse-checkout set docs/en/docs
```

Then move the folder into your `docs/` directory:

```
docs/
└── fastapi/
    ├── index.md
    ├── tutorial/
    └── advanced/
```

You can add as many libraries as you want — just drop a folder into `docs/`.

---

## Configuration

Create a `.env` file in the project root:

```env
DOCS_DIR=./docs
```

---

## Connecting to Qwen CLI

Add the following to your `.qwen/settings.json`:

```json
{
  "mcpServers": {
    "docubridge": {
      "command": "docs-server",
      "timeout": 15000
    }
  }
}
```

Then verify the connection:

```bash
qwen mcp list
```

You should see `docubridge` in the list.

---

## Usage Examples

Once connected, you can ask your AI assistant:

- *"What libraries do you have access to?"*
- *"Show me all files in the fastapi docs"*
- *"Find everything about dependency injection in fastapi"*
- *"Read the content of tutorial/path-params.md"*

The model will call the appropriate tool and answer based on the actual documentation.

---

## Requirements

- Python 3.11+
- `mcp[cli]` >= 1.0.0
- `pydantic-settings`

---

## License

MIT
