# NetDocAI

### Autonomous AI-Powered Network Troubleshooting CLI

NetDocAI is an autonomous network troubleshooting agent that investigates connectivity problems using real diagnostic tools, AI-powered reasoning, and retrieval-augmented generation (RAG).

Built with **Python, LangGraph, Model Context Protocol (MCP), Google Gemini, and ChromaDB**, NetDocAI allows users to diagnose network issues directly from their terminal using natural language.

Instead of manually executing multiple networking commands and interpreting their outputs, users can describe a problem and let NetDocAI investigate.

The agent selects appropriate diagnostic tools, analyzes the collected evidence, develops hypotheses, and generates structured troubleshooting reports.

---

## Features

### Autonomous Network Troubleshooting

- LangGraph-based agent for stateful diagnostic workflows.
- Gemini-powered reasoning and tool selection.
- Autonomous execution of network diagnostic tools.
- Evidence-based hypothesis generation and assessment.
- Multi-step investigation with configurable execution limits.
- Structured diagnostic reports.

### Network Diagnostic Tools

NetDocAI provides five MCP tools:

| Tool | Description |
|------|-------------|
| `ping` | Tests host reachability using ICMP |
| `dns` | Resolves domain names and retrieves DNS information |
| `tcp` | Tests TCP connectivity to specific hosts and ports |
| `http` | Performs HTTP requests and inspects responses |
| `search_docs` | Retrieves relevant networking documentation using RAG |

All diagnostic tools are exposed through a local Model Context Protocol server.

### AI and Knowledge Retrieval

- Google Gemini integration for autonomous reasoning.
- Configurable Gemini reasoning model.
- Gemini embeddings for semantic knowledge retrieval.
- ChromaDB for persistent vector storage.
- Bundled networking documentation.
- Automatic knowledge-base initialization.
- RAG-powered contextual assistance.

### CLI Experience

- Interactive terminal interface built with Rich.
- Natural-language problem descriptions.
- First-time Gemini API key onboarding.
- API key validation and local credential storage.
- User-selectable Gemini models.
- Persistent model preferences.
- CLI command for changing models.
- Installable Python package distributed through PyPI.

---

## Installation

### Requirements

- Python 3.11 or newer
- Internet connectivity
- Google Gemini API key
- `pipx` (recommended)

NetDocAI has been tested on Linux and Windows.

### Install from PyPI

Install NetDocAI using pipx:

```bash
pipx install netdocai
```

Launch the application:

```bash
netdocai
```

Alternatively, install using pip inside a Python virtual environment:

```bash
pip install netdocai
```

### Install from GitHub

To install the latest development version directly from GitHub:

```bash
pipx install git+https://github.com/AbhiAnand-1011/NetDocAI.git
```

### Upgrade NetDocAI

To upgrade an existing pipx installation:

```bash
pipx upgrade netdocai
```

---

## First-Time Setup

NetDocAI uses Google's Gemini API for AI reasoning, diagnostic planning, and knowledge embeddings.

Each user must configure their own Gemini API key.

### Step 1: Obtain a Gemini API Key

Generate an API key using Google AI Studio:

**[Get a Gemini API Key](https://aistudio.google.com/apikey)**

### Step 2: Launch NetDocAI

```bash
netdocai
```

If no API key is configured, NetDocAI displays its onboarding interface.

```text
╭──────────────────────────────────────╮
│ Welcome to NetDocAI!                 │
│                                      │
│ To get started, you need a Google    │
│ Gemini API key.                      │
│                                      │
│ https://aistudio.google.com/apikey   │
╰──────────────────────────────────────╯

Enter your Gemini API key:
```

Enter your API key and press Enter.

The input is hidden for security. Typed or pasted characters will not appear in the terminal.

NetDocAI attempts to validate the key before saving it.

If Google's API is temporarily unavailable or rate-limited, users can choose whether to save the key without verification.

### Step 3: Configure the Gemini Model

Starting with v0.1.1, NetDocAI supports interactive Gemini model selection.

If no model preference has been configured, the application prompts the user to choose a model.

```text
Gemini Model Configuration

Default: gemini-3.6-flash

Gemini model (gemini-3.6-flash): gemini-2.5-flash

✓ Model configured: gemini-2.5-flash
```

Press Enter without typing a model name to use the default.

The selected model is saved locally and reused during subsequent executions.

---

## Gemini Model Configuration

NetDocAI allows users to select their preferred Gemini model without modifying the source code.

### Default Model

The default reasoning model is:

```text
gemini-3.6-flash
```

### Change the Gemini Model

Starting with v0.1.1, users can change their model at any time using:

```bash
netdocai config model
```

Example:

```text
Current model: gemini-2.5-flash

Enter new Gemini model: gemini-2.5-pro

✓ Model updated successfully: gemini-2.5-pro
```

The new preference is saved locally.

Users do not need to re-enter their API key when changing models.

### Model Selection Priority

NetDocAI determines the reasoning model using the following priority:

| Priority | Configuration Source |
|----------|----------------------|
| 1 | `GEMINI_MODEL` environment variable |
| 2 | Locally saved model preference |
| 3 | Default model |

On Linux, the model preference is stored at:

```text
~/.config/netdocai/model
```

### Model Compatibility

NetDocAI accepts user-provided Gemini model identifiers without performing capability validation.

Users can select models supported by their Gemini API access.

If a model does not support an operation required by NetDocAI, Google's API may return an error.

NetDocAI does not automatically switch models or maintain a predefined list of compatible models.

The selected model controls AI reasoning and tool selection. The RAG embedding model is configured separately.

---

## Usage

Launch NetDocAI:

```bash
netdocai
```

Describe the network issue when prompted.

### Example 1: Website Connectivity

```text
Describe your network problem: google.com is not working
```

### Example 2: DNS Problems

```text
Describe your network problem: My DNS resolution keeps failing.
```

### Example 3: TCP Connectivity

```text
Describe your network problem: I cannot connect to github.com on port 443.
```

### Example 4: HTTP Connectivity

```text
Describe your network problem: I can ping a website but cannot access it through HTTPS.
```

NetDocAI uses Gemini to analyze the request and determine which diagnostic tools to execute.

### Example Execution

```text
NetDocAI
Autonomous Network Troubleshooter

Using Gemini model: gemini-2.5-flash

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

The diagnostic sequence depends on the problem and the agent's decisions.

After investigating, NetDocAI displays a structured diagnostic report.

---

## Architecture

NetDocAI combines LangGraph-based agent orchestration, Gemini reasoning, MCP diagnostic tools, and retrieval-augmented generation.

```text
                         USER
                           |
                           v
                    NetDocAI CLI
                           |
                           v
                 Configuration Setup
                  API Key + Model
                           |
                           v
                    LangGraph Agent
                           |
                           v
                     Gemini API
                           |
                           v
                 Diagnostic Planning
                           |
                           v
                     MCP Client
                           |
                           v
                      MCP Server
                           |
          +----------------+----------------+
          |                |                |
          v                v                v
        Ping              DNS              TCP
          |                |                |
          +----------------+----------------+
                           |
                    +------+------+
                    |             |
                    v             v
                   HTTP       search_docs
                                  |
                                  v
                             RAG Pipeline
                                  |
                                  v
                               ChromaDB
                                  |
                                  v
                         Knowledge Documents
                           |
                           v
                    Tool Observations
                           |
                           v
                    Agent Assessment
                           |
                           v
                 Continue or Finalize
                           |
                           v
                    Diagnostic Report
```

The diagram illustrates the major components. The agent can invoke available diagnostic tools independently based on its reasoning.

### LangGraph Agent

The LangGraph agent maintains the investigation state, including:

- User-provided networking problem
- Conversation history
- Available MCP tools
- Pending tool calls
- Diagnostic observations
- Current hypothesis
- Agent responses
- Investigation step count

The workflow includes four primary nodes:

| Node | Responsibility |
|------|----------------|
| `plan` | Uses Gemini to select diagnostic tools or produce a conclusion |
| `execute_tools` | Executes MCP tools and records their results |
| `assess` | Analyzes evidence and updates the diagnostic hypothesis |
| `finalize` | Generates a report when the investigation reaches its step limit |

The agent can repeat the planning and assessment process as additional diagnostic evidence becomes available.

### Model Context Protocol

NetDocAI uses MCP to separate the agent's reasoning workflow from the implementation of network diagnostic tools.

The MCP server runs locally as a Python subprocess.

The agent communicates with the server using MCP over standard input and output.

This architecture allows diagnostic tools to be discovered and executed through a consistent interface.

---

## Retrieval-Augmented Generation

NetDocAI includes a local networking knowledge base to support diagnostic investigations.

The RAG implementation uses:

- Bundled Markdown documentation
- Text chunking
- Gemini embeddings
- ChromaDB vector storage
- Semantic similarity search
- MCP-based knowledge retrieval

### Retrieval Workflow

```text
Networking Documentation
          |
          v
      Text Chunking
          |
          v
     Gemini Embeddings
          |
          v
        ChromaDB
          |
          v
    Semantic Retrieval
          |
          v
       search_docs
          |
          v
     LangGraph Agent
```

### Automatic Knowledge Indexing

NetDocAI automatically initializes its knowledge index when the `search_docs` tool is used and the ChromaDB collection is empty.

The indexing process:

1. Reads bundled Markdown documents.
2. Splits the documents into chunks.
3. Generates embeddings.
4. Stores the resulting vectors in ChromaDB.
5. Makes the indexed knowledge available for semantic retrieval.

The database is reused across application executions.

No manual indexing command is required.

### Knowledge Base

The bundled documentation covers:

| Document | Subject |
|----------|---------|
| `dns.md` | DNS resolution and troubleshooting |
| `tcp.md` | TCP networking and connectivity |
| `http.md` | HTTP communication and diagnostics |
| `linux_networking.md` | Linux networking fundamentals |

### Local Database Storage

On Linux, ChromaDB data is stored at:

```text
~/.local/share/netdocai/chroma_db/
```

The application also supports the `XDG_DATA_HOME` environment variable for configuring its data-storage location.

---

## Diagnostic Reports

NetDocAI generates structured reports using observations collected during the investigation.

Reports contain:

| Section | Description |
|---------|-------------|
| Problem | Original networking issue |
| Network Observations | Results of executed diagnostic tools |
| Knowledge Retrieved | Documentation sources retrieved through RAG |
| Current Assessment | Agent's current hypothesis |
| Diagnosis | Final conclusion or investigation-limit message |

Reports are displayed directly in the terminal using Rich.

---

## Tech Stack

| Technology | Purpose |
|------------|---------|
| Python | Application development |
| LangGraph | Stateful agent orchestration |
| Google Gemini | Reasoning and diagnostic planning |
| Google Gen AI SDK | Gemini API integration |
| Model Context Protocol | Diagnostic tool communication |
| ChromaDB | Vector database and knowledge retrieval |
| Gemini Embeddings | Semantic text embeddings |
| Rich | Terminal interface |
| setuptools | Python packaging |
| GitHub Actions | Automated PyPI publishing |

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
├── .github/
│   └── workflows/
│       └── release.yml
│
├── knowledge/
├── .env.example
├── .gitignore
├── pyproject.toml
├── requirements.txt
└── README.md
```

### Core Modules

| Module | Responsibility |
|--------|----------------|
| `agent.py` | LangGraph workflow and diagnostic reasoning |
| `config.py` | Gemini configuration and model preferences |
| `gemini.py` | Asynchronous Gemini API integration and retries |
| `main.py` | CLI entry point and model configuration commands |
| `mcp_server.py` | MCP server and tool registration |
| `onboarding.py` | API key onboarding and model selection |
| `prompts.py` | System instructions and prompt construction |
| `rag.py` | Knowledge indexing and retrieval |
| `report.py` | Diagnostic report generation |
| `tools.py` | Network diagnostic implementations |

---

## Development

### Clone the Repository

```bash
git clone https://github.com/AbhiAnand-1011/NetDocAI.git
cd NetDocAI
```

### Create a Virtual Environment

#### Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

#### Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### Install in Editable Mode

```bash
python -m pip install -e .
```

### Run NetDocAI

```bash
netdocai
```

### Configure the Gemini Model

Starting with v0.1.1:

```bash
netdocai config model
```

### Build the Distribution

Install the build tool:

```bash
python -m pip install build
```

Build the wheel and source distribution:

```bash
python -m build
```

Generated distribution files are placed in:

```text
dist/
```

---

## Configuration

NetDocAI supports environment-based configuration and locally saved user preferences.

### Environment Variables

| Variable | Description |
|----------|-------------|
| `GEMINI_API_KEY` | Gemini API credential |
| `GEMINI_MODEL` | Gemini reasoning model override |
| `XDG_CONFIG_HOME` | Application configuration directory |
| `XDG_DATA_HOME` | Application data-storage directory |

### Local Configuration

On Linux, NetDocAI stores user configuration under:

```text
~/.config/netdocai/
```

The directory may contain:

```text
api_key
model
```

The API key is stored as plaintext with restricted filesystem permissions.

Saved model preferences are loaded automatically during subsequent executions.

If an API key is already provided through the environment, NetDocAI uses it without prompting for a new key.

---

## Troubleshooting

### API Key Not Configured

Run:

```bash
netdocai
```

NetDocAI launches onboarding when no API key is available.

Generate an API key using:

[Google AI Studio](https://aistudio.google.com/apikey)

### Change the Gemini Model

Starting with v0.1.1:

```bash
netdocai config model
```

Enter a new model identifier when prompted.

### Gemini API Rate Limit

If Gemini returns:

```text
429 RESOURCE_EXHAUSTED
```

Your Gemini API project may have reached its applicable request quota.

Check your usage and rate limits through Google AI Studio.

### Temporary Gemini API Failure

If Gemini returns:

```text
503 UNAVAILABLE
```

The requested Gemini model may be temporarily unavailable.

NetDocAI includes retry handling for transient API failures.

### Knowledge Index Initialization

The first RAG search may take longer because NetDocAI generates embeddings and initializes the ChromaDB collection.

Once indexed, the stored knowledge is reused.

---

## Contributing

Contributions, bug reports, and suggestions are welcome.

To contribute:

1. Fork the repository.
2. Create a development branch.
3. Implement and test your changes.
4. Open a pull request describing your modifications.

Bug reports and feature requests can be submitted through:

[GitHub Issues](https://github.com/AbhiAnand-1011/NetDocAI/issues)

---

## Author

**Abhishek Anand**

GitHub: [AbhiAnand-1011](https://github.com/AbhiAnand-1011)

---

## Links

- **GitHub:** https://github.com/AbhiAnand-1011/NetDocAI
- **PyPI:** https://pypi.org/project/netdocai/
- **Gemini API Key:** https://aistudio.google.com/apikey

---

**NetDocAI — Autonomous network troubleshooting, directly from your terminal.**
