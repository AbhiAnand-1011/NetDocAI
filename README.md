# NetDocAI

**An autonomous, AI-powered network troubleshooting agent for your terminal.**

NetDocAI is a Python-based CLI tool that investigates network connectivity problems using real diagnostic tools, autonomous reasoning, and retrieval-augmented generation (RAG).

Built with **LangGraph, Model Context Protocol (MCP), Google Gemini, and ChromaDB**, NetDocAI combines traditional network diagnostics with an AI agent capable of selecting tools, analyzing their results, forming hypotheses, and generating structured diagnostic reports.

Instead of manually running multiple networking commands and interpreting their outputs, users can describe their problem in natural language and let NetDocAI investigate.

---

## Features

- **Autonomous Troubleshooting:** Uses a LangGraph-based agent to plan, execute, and evaluate network diagnostics.
- **Natural Language Interface:** Describe networking problems directly in the terminal.
- **MCP Tool Integration:** Diagnostic utilities are exposed through a local Model Context Protocol server.
- **DNS Diagnostics:** Resolve domain names and inspect DNS resolution results.
- **Ping Diagnostics:** Check host reachability using ICMP.
- **TCP Connectivity Testing:** Test connectivity to specific hosts and ports.
- **HTTP Diagnostics:** Inspect HTTP responses and connection failures.
- **RAG-Powered Knowledge Retrieval:** Retrieve relevant information from bundled networking documentation.
- **Persistent Vector Database:** Store and retrieve knowledge embeddings using ChromaDB.
- **Gemini Integration:** Use Google Gemini for reasoning, tool selection, and knowledge embeddings.
- **First-Run API Key Setup:** Configure your own Gemini API key through an interactive onboarding interface.
- **Automatic Knowledge Indexing:** Initialize the knowledge base when retrieval is first requested.
- **Structured Diagnostic Reports:** Receive an organized summary of observations, retrieved knowledge, assessments, and conclusions.

---

## Installation

### Requirements

- Python 3.11 or newer
- Internet connectivity for Gemini API requests
- A Google Gemini API key
- Network access for running diagnostics
- `pipx` (recommended for CLI installation)

NetDocAI executes its diagnostic tools locally. Internet connectivity is required for AI inference and for diagnostics involving external network resources.

### Install from GitHub

NetDocAI can be installed directly from its GitHub repository using `pipx`:

```bash
pipx install git+https://github.com/AbhiAnand-1011/NetDocAI.git
```

Once installed, launch the application:

```bash
netdocai
```

### Install from PyPI

After the first PyPI release, NetDocAI will also be available through:

```bash
pipx install netdocai
```

Alternatively, it can be installed using `pip` inside a Python virtual environment:

```bash
pip install netdocai
```

**Note:** PyPI distribution is being prepared. Until the package is published, use the GitHub installation method above.

---

## First-Time Setup

NetDocAI uses Google's Gemini API for autonomous reasoning, tool selection, and knowledge embeddings.

Each user must configure their own Gemini API key.

When launching NetDocAI for the first time:

```bash
netdocai
```

The CLI displays an onboarding interface containing a link to Google AI Studio.

**Get your Gemini API key:** https://aistudio.google.com/apikey

The application then prompts you to enter your API key.

NetDocAI attempts to validate the key before saving it. If Google's API is temporarily unavailable or rate-limited, the application allows you to decide whether to save the key without verification.

### API Key Storage

On Linux, API keys entered during onboarding are stored locally at:

```text
~/.config/netdocai/api_key
```

The application creates the configuration directory and restricts access to the credential file using filesystem permissions.

The key is stored as plaintext in a user-restricted file, not encrypted.

NetDocAI also supports reading an API key from the `GEMINI_API_KEY` environment variable or an existing `.env` configuration.

**You do not need to manually create a `.env` file when using the interactive onboarding system.**

The API key is used to communicate with Google's Gemini API. NetDocAI does not require an account on a separate NetDocAI service.

**Note:** The API key input is hidden for security. Characters will not appear while typing or pasting. Press Enter after entering your key.

---

## Usage

Start NetDocAI from your terminal:

```bash
netdocai
```

The CLI prompts you to describe your network problem.

For example:

```text
Describe your network problem: google.com is not working
```

Other example problems include:

```text
I can ping google.com but cannot access it through HTTPS.
```

```text
My DNS resolution seems to be failing.
```

```text
I cannot establish a TCP connection to github.com on port 443.
```

```text
Some websites are reachable, but others keep timing out.
```

NetDocAI determines which diagnostic tools to execute based on the problem and the evidence collected during the investigation.

The specific diagnostic sequence can vary between runs.

### Diagnostic Workflow

During an investigation, NetDocAI may:

1. Resolve domain names through DNS.
2. Test host reachability using ICMP ping.
3. Check TCP connectivity on relevant ports.
4. Perform HTTP requests.
5. Retrieve relevant networking documentation.
6. Assess the collected evidence.
7. Continue investigating or produce a final diagnostic report.

A simplified execution trace may look like:

```text
NetDocAI
Autonomous Network Troubleshooter

Describe your network problem: google.com is not working

Investigating...

[Agent] dns
[Tool] Executing dns...
[Tool] dns completed.

[Agent] ping, tcp
[Tool] Executing ping...
[Tool] ping completed.
[Tool] Executing tcp...
[Tool] tcp completed.

[Agent] Finalizing diagnosis...
```

Tool selection and execution depend on the agent's decisions and the reported problem.

---

## Architecture

NetDocAI combines a stateful LangGraph agent, Gemini reasoning, MCP diagnostic tools, and a local RAG knowledge base.

```text
                        User
                         |
                         v
                    NetDocAI CLI
                         |
                         v
                  LangGraph Agent
                         |
                         v
                   Gemini Reasoning
                         |
              +----------+----------+
              |                     |
              v                     v
          MCP Server          Agent Assessment
              |                     |
      +-------+-------+             |
      |       |       |             |
      v       v       v             |
     DNS     Ping     TCP           |
      |       |       |             |
      +-------+-------+             |
              |                     |
              v                     |
             HTTP                   |
              |                     |
              v                     |
          search_docs               |
              |                     |
              v                     |
          ChromaDB                  |
              |                     |
              v                     |
       Gemini Embeddings            |
              |                     |
              +----------+----------+
                         |
                         v
                  Evidence Analysis
                         |
                         v
                 Diagnostic Report
```

### LangGraph Agent

The LangGraph agent maintains the investigation state, including:

- The original networking problem
- Conversation and tool-call history
- Available MCP tools
- Pending tool executions
- Collected observations
- Current diagnostic hypothesis
- Investigation progress
- Final response

The workflow consists of four primary nodes:

| Node | Responsibility |
|---|---|
| `plan` | Uses Gemini to reason about the problem and select tools |
| `execute_tools` | Executes selected MCP tools and records observations |
| `assess` | Evaluates diagnostic evidence and updates the hypothesis |
| `finalize` | Produces a report when the investigation reaches its configured step limit |

The agent can repeat the planning and assessment process until it reaches a conclusion or its diagnostic step limit.

### Model Context Protocol (MCP)

NetDocAI uses MCP to expose its networking utilities to the agent.

The MCP server runs locally as a Python subprocess and communicates with the agent using standard input and output.

Five tools are currently available:

| Tool | Description |
|---|---|
| `ping` | Tests host reachability using ICMP |
| `dns` | Resolves a hostname to its IP addresses |
| `tcp` | Tests TCP connectivity to a specified host and port |
| `http` | Performs an HTTP request and returns response information |
| `search_docs` | Retrieves relevant networking documentation through RAG |

These tools perform actual diagnostic operations rather than simulated checks.

### Retrieval-Augmented Generation (RAG)

NetDocAI includes a networking knowledge base used to support its diagnostic reasoning.

The retrieval pipeline consists of:

1. Reading bundled Markdown documentation.
2. Dividing the documents into text chunks.
3. Generating embeddings using Google's Gemini embedding model.
4. Storing the embeddings in ChromaDB.
5. Performing semantic searches against the indexed documents.
6. Returning relevant documentation to the agent through MCP.

The vector database is stored locally and reused between executions.

Knowledge indexing is triggered automatically when the RAG search tool is used and the collection is empty.

**Gemini API access is required for embedding generation.** Initial indexing may require multiple embedding requests.

---

## Knowledge Base

NetDocAI ships with networking documentation covering four areas:

| Document | Topic |
|---|---|
| `dns.md` | Domain Name System and name resolution |
| `tcp.md` | TCP connections and networking concepts |
| `http.md` | HTTP communication and related diagnostics |
| `linux_networking.md` | Linux networking fundamentals and troubleshooting |

The documents are bundled with the Python package.

Users do not need to download them separately or manually create the ChromaDB collection.

### Local Database Storage

On Linux, the default ChromaDB storage location is:

```text
~/.local/share/netdocai/chroma_db/
```

NetDocAI supports the `XDG_DATA_HOME` environment variable for configuring its application-data location.

The vector database persists across application launches.

---

## Diagnostic Reports

After an investigation, NetDocAI generates a structured report.

Reports contain the following sections:

| Section | Description |
|---|---|
| Problem | The original issue provided by the user |
| Network Observations | Results collected from diagnostic tools |
| Knowledge Retrieved | Sources retrieved from the networking knowledge base |
| Current Assessment | The agent's current hypothesis based on available evidence |
| Diagnosis | The final conclusion or investigation-limit message |

The report is displayed directly in the terminal using Rich.

Diagnoses are generated from the information available during execution and may not always identify the underlying problem conclusively.

---

## Tech Stack

| Technology | Purpose |
|---|---|
| Python | Application implementation |
| LangGraph | Stateful agent workflow and execution |
| Google Gemini API | AI reasoning and tool selection |
| Google Gen AI SDK | Gemini API integration |
| Model Context Protocol | Diagnostic tool communication |
| ChromaDB | Persistent vector storage and retrieval |
| Gemini Embeddings | Semantic embedding generation |
| Rich | Terminal interface and formatted output |
| setuptools | Python package building and distribution |

---

## Project Structure

```text
NetDocAI/
|
├── netdocai/
│   ├── __init__.py
│   ├── agent.py
│   ├── config.py
│   ├── gemini.py
│   ├── main.py
│   ├── mcp_server.py
│   ├── onboarding.py
│   ├── prompts.py
│   ├── rag.py
│   ├── report.py
│   ├── tools.py
│   │
│   └── knowledge/
│       ├── dns.md
│       ├── http.md
│       ├── linux_networking.md
│       └── tcp.md
│
├── knowledge/
├── .env.example
├── .gitignore
├── pyproject.toml
├── requirements.txt
└── README.md
```

### Key Modules

- **`agent.py`** — LangGraph agent definition, planning, tool execution, and assessment.
- **`config.py`** — Gemini configuration and environment-based settings.
- **`gemini.py`** — Asynchronous Gemini API communication and retry handling.
- **`main.py`** — Rich-based terminal interface and CLI entry point.
- **`mcp_server.py`** — Local MCP server and registered diagnostic tools.
- **`onboarding.py`** — First-time API key configuration and validation.
- **`prompts.py`** — Agent instructions and prompt construction.
- **`rag.py`** — Knowledge indexing, embeddings, ChromaDB, and retrieval.
- **`report.py`** — Structured diagnostic report generation.
- **`tools.py`** — Network diagnostic implementations.

The packaged application uses the documentation inside `netdocai/knowledge/`.

---

## Development

### Clone the Repository

```bash
git clone https://github.com/AbhiAnand-1011/NetDocAI.git
cd NetDocAI
```

### Create a Virtual Environment

On Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Install the Package in Editable Mode

```bash
python -m pip install -e .
```

### Run NetDocAI

```bash
netdocai
```

The same first-time API key onboarding flow is available during development.

### Build the Distribution

Install the Python build tool:

```bash
python -m pip install build
```

Build the source distribution and wheel:

```bash
python -m build
```

Generated distribution files are placed in the `dist/` directory.

The wheel includes the `netdocai` Python package and its bundled networking documentation.

---

## Configuration

NetDocAI supports the following environment variables:

| Variable | Purpose |
|---|---|
| `GEMINI_API_KEY` | Gemini API credential |
| `GEMINI_MODEL` | Override the configured Gemini reasoning model |
| `XDG_CONFIG_HOME` | Override the application configuration directory |
| `XDG_DATA_HOME` | Override the local application-data directory |

When no Gemini API key is available through the environment or previously saved configuration, NetDocAI launches its interactive onboarding flow.

Users are responsible for their own Gemini API usage and any applicable charges.

---


## Troubleshooting

### Gemini API Key Not Configured

Launch NetDocAI:

```bash
netdocai
```

If no API key is found, the onboarding interface will request one.

Obtain a key from:

https://aistudio.google.com/apikey

### Gemini API Rate Limit

If Gemini returns:

```text
429 RESOURCE_EXHAUSTED
```

Your API project may have reached its applicable request quota.

Check your usage and rate limits through Google AI Studio.

### Temporary Gemini API Failure

If Gemini returns:

```text
503 UNAVAILABLE
```

The requested model may be temporarily unavailable or experiencing high demand.

NetDocAI includes retry handling for transient Gemini API failures.

### First-Time Knowledge Indexing

The first RAG search may take longer because NetDocAI needs to generate embeddings and populate its local ChromaDB collection.

Subsequent searches reuse the stored index.

Indexing may fail if the Gemini embedding API is unavailable or its applicable quota is exhausted.

---

## Future Improvements

Potential future development areas include:

- Additional network diagnostic tools
- Support for multiple LLM providers
- More comprehensive networking documentation
- Improved error handling and retry strategies
- More flexible CLI arguments and configuration commands
- Improved cross-platform compatibility
- Expanded automated testing

These are planned possibilities rather than features currently implemented.

---

## Contributing

Contributions, issue reports, and suggestions are welcome.

To contribute:

1. Fork the repository.
2. Create a branch for your changes.
3. Implement and test your modifications.
4. Open a pull request describing your changes.

Bugs and feature requests can be submitted through the [GitHub Issues](https://github.com/AbhiAnand-1011/NetDocAI/issues) page.

---

## Author

**Abhishek Anand**

GitHub: [AbhiAnand-1011](https://github.com/AbhiAnand-1011)

---

## Project Repository

[github.com/AbhiAnand-1011/NetDocAI](https://github.com/AbhiAnand-1011/NetDocAI)

---

**NetDocAI — Autonomous network troubleshooting, directly from your terminal.**
