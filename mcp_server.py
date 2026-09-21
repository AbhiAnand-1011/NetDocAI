from mcp.server import MCPServer

from rag import search_knowledge
from tools import (
    dns_lookup,
    http_request,
    ping_host,
    tcp_connect,
)


mcp = MCPServer("NetDocAI")


@mcp.tool()
def ping(host: str, count: int = 1) -> str:
    """Check whether a host is reachable using ICMP ping."""
    return ping_host(host, count)


@mcp.tool()
def dns(host: str) -> str:
    """Resolve a hostname and return its IP addresses."""
    return dns_lookup(host)


@mcp.tool()
def tcp(host: str, port: int, timeout: float = 3.0) -> str:
    """Check whether a TCP connection can be established to a host and port."""
    return tcp_connect(host, port, timeout)


@mcp.tool()
def http(url: str, timeout: float = 5.0) -> str:
    """Send an HTTP request and return basic response information."""
    return http_request(url, timeout)


@mcp.tool()
def search_docs(query: str, n_results: int = 3) -> str:
    """Search the NetDocAI networking knowledge base."""
    results = search_knowledge(query, n_results)

    if not results:
        return "No relevant documentation found."

    formatted = []

    for result in results:
        formatted.append(
            f"SOURCE: {result['source']}\n"
            f"CONTENT:\n{result['content']}"
        )

    return "\n\n---\n\n".join(formatted)

if __name__ == "__main__":
    mcp.run()