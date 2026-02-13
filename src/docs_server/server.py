from mcp.server.fastmcp import FastMCP

from src.docs_server.config import settings
from src.docs_server.reader import DocsReader

mcp = FastMCP("docbridge")
reader = DocsReader(settings.docs_dir)


@mcp.tool()
def list_libraries() -> str:
    """List all available documentation libraries"""
    libs = reader.list_libraries()
    if not libs:
        return "No libraries found"
    return "\n".join(f"- {lib}" for lib in libs)


@mcp.tool()
def list_files(library: str) -> str:
    """List all files in a specific library"""
    files = reader.list_files(library)
    if not files:
        return f"Library '{library}' not found or empty"
    return "\n".join(f"- {f}" for f in files)


@mcp.tool()
def get_file(library: str, filename: str) -> str:
    """Get the content of a specific documentation file"""
    doc = reader.get_file(library, filename)
    if doc is None:
        return f"File '{filename}' not found in '{library}'"
    return doc.content


@mcp.tool()
def search_docs(query: str, library: str | None = None) -> str:
    """Search across all docs or within a specific library"""
    results = reader.search(query, library)
    if not results:
        return "Nothing found"
    return "\n".join(results)