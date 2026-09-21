# NetDocAI

NetDocAI is an autonomous CLI network troubleshooting agent that investigates connectivity problems using real network diagnostics, a networking knowledge base, and an LLM-driven reasoning loop.

The user describes a network problem in natural language. NetDocAI gathers evidence, selects diagnostic tools, retrieves relevant networking documentation, evaluates the observations, and produces a structured diagnostic report.

## Architecture

```text
User Problem
     |
     v
Rich CLI
     |
     v
LangGraph Agent
     |
     +--------------------+
     |                    |
     v                    v
 Gemini Reasoning      MCP Tools
                            |
             +--------------+--------------+
             |              |              |
            Ping           DNS            TCP
                                           |
                                          HTTP
             |
             v
      ChromaDB Knowledge Base
             |
             v
     Gemini Embeddings
             |
             v
      Diagnostic Report
```

## How It Works

1. The user describes a network problem.
2. The LangGraph agent sends the problem to Gemini.
3. Gemini decides which diagnostics are useful.
4. Network tools are exposed through MCP.
5. The selected tools execute real diagnostics on the machine.
6. NetDocAI retrieves relevant networking documentation using RAG.
7. Gemini evaluates the collected evidence.
8. The investigation repeats until a diagnosis is reached or the step limit is hit.
9. A structured diagnostic report is displayed in the terminal.

## Features

- Autonomous network troubleshooting loop
- LangGraph-based stateful agent
- MCP tool integration
- Ping diagnostics
- DNS resolution checks
- TCP connectivity checks
- HTTP request diagnostics
- RAG-based networking documentation retrieval
- ChromaDB vector database
- Gemini-powered embeddings
- Gemini reasoning and tool selection
- Retry handling for transient Gemini API failures
- Structured terminal diagnostic reports

## Tech Stack

- Python
- Google Gemini API
- LangGraph
- MCP
- ChromaDB
- Rich
- Python `socket`
- Python `subprocess`
- Python `urllib`

## Project Structure

```text
NetDocAI/
├── agent.py
├── config.py
├── gemini.py
├── main.py
├── mcp_server.py
├── prompts.py
├── rag.py
├── report.py
├── tools.py
├── knowledge/
│   ├── dns.md
│   ├── http.md
│   ├── linux_networking.md
│   └── tcp.md
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## Setup

Clone the repository:

```bash
git clone https://github.com/AbhiAnand-1011/NetDocAI.git
cd NetDocAI
```

Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file:

```env
GEMINI_API_KEY=your_api_key_here
GEMINI_MODEL=gemini-3.6-flash
```

## Build the Knowledge Index

The networking knowledge base is stored in the `knowledge/` directory and indexed into a local ChromaDB database.

After creating your `.env` file, build the index:

```bash
python -c "from rag import build_index; print(f'Indexed {build_index()} knowledge chunks.')"
```

This creates the local `chroma_db/` runtime directory, which is intentionally excluded from Git.

## Running NetDocAI

Start the CLI:

```bash
python main.py
```

Example:

```text
NetDocAI
Autonomous Network Troubleshooter

Describe your network problem:
google.com is slow and some websites are timing out
```

NetDocAI will investigate the problem and display a diagnostic report containing:

- the original problem
- observed network results
- relevant knowledge-base sources
- the current assessment
- the final diagnosis

## Knowledge Base

Networking documentation is stored in the `knowledge/` directory.

Current topics include:

- DNS
- HTTP
- Linux networking
- TCP

The documents are chunked, embedded, and stored in ChromaDB for semantic retrieval.

## Limitations

NetDocAI is currently designed as a local CLI project and is intentionally small.

It currently does not provide:

- a web dashboard
- distributed execution
- long-term conversation memory
- automated remediation
- production-grade monitoring
- large-scale knowledge ingestion

Network diagnostics also depend on the environment in which the program is executed.

## Future Improvements

Possible extensions include:

- richer network measurements
- additional diagnostic tools
- improved hypothesis tracking
- larger networking knowledge bases
- persistent investigation history
- automated remediation suggestions
- web-based observability
- richer agent evaluation and benchmarking

## Security Notes

The Gemini API key is loaded from `.env` and should never be committed to Git.

The generated ChromaDB database is excluded from Git because it is a local runtime artifact.

## Status

NetDocAI is a portfolio-scale experimental project focused on combining:

**LLM reasoning + LangGraph + MCP + RAG + real network diagnostics**
