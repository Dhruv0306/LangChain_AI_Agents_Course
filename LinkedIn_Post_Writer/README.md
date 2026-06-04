# LinkedIn Post Writer Agent

An intelligent multi-agent AI system for generating professional, factual LinkedIn posts using LangChain, LLMs, and web search capabilities.

## Overview

This project implements a sophisticated AI agent orchestrator that automates LinkedIn post creation through a collaborative multi-agent workflow. The main orchestrator delegates specialized tasks to sub-agents (writer, validator, scorer) while managing a virtual file system for state persistence and task tracking.

**Key Features:**
- 🤖 **Multi-Agent Architecture**: Separate specialized agents for writing, validation, and scoring
- 🔍 **Web Search Integration**: Real-time fact verification using Tavily search API
- 📋 **Task Management**: Built-in TODO system for workflow tracking
- 💾 **Virtual File System**: Persistent state management across agent handoffs
- 🔄 **Context Isolation**: Sub-agents maintain isolated state for clean delegation
- 🎯 **Quality Control**: Automated validation and scoring pipeline
- 📊 **LLM-Powered**: Uses Ollama for local LLM inference

## Architecture

```
┌─────────────────────────────────────────┐
│   Main LinkedIn Orchestrator Agent      │
│  (Coordinates workflow and delegates)   │
└──────────────┬──────────────────────────┘
               │
      ┌────────┼────────┬────────┐
      │        │        │        │
      ▼        ▼        ▼        ▼
   Writer   Validator  Scorer   Tools
   Agent      Agent     Agent    (LS, Read, Write, etc.)
```

### Components

| Module | Purpose |
|--------|---------|
| `main.py` | Entry point and main agent orchestrator |
| `state.py` | Extended agent state (todos, file system) |
| `prompts.py` | System prompts and instructions for agents |
| `subagents.py` | Sub-agent configurations (writer, validator, scorer) |
| `file_tools.py` | Virtual file system tools (ls, read, write) |
| `todo_tools.py` | Task management tools (read_todos, write_todos) |
| `task_tools.py` | Sub-agent delegation framework |
| `webSearch_tools.py` | Web search and content processing (Tavily) |
| `llm_utils.py` | LLM utilities (message formatting, prompt display) |

## Prerequisites

- **Python 3.10+**
- **Ollama** running locally (for local LLM inference)
  - Download from: https://ollama.ai
  - Required model: `qwen3.5:latest`
  - Default endpoint: `http://localhost:11434`
- **API Keys**: 
  - Tavily Search API key (for web search)
  - Set in `.env` file

## Installation

1. **Clone or navigate to the project**:
   ```bash
   cd LinkedIn_Post_Writer
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/Scripts/activate  # Windows
   # or
   source venv/bin/activate      # macOS/Linux
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   Create or update `.env` file with your API keys:
   ```env
   TAVILY_API_KEY=your_tavily_api_key_here
   LINKEDIN_AGENT_DEBUG=1  # Set to 0 to disable debug logging
   ```

5. **Start Ollama**:
   ```bash
   ollama serve
   ```

   In another terminal, pull the required model:
   ```bash
   ollama pull qwen3.5:latest
   ```

## Usage

### Command Line

Run the agent with a custom query:

```bash
python main.py "Write a LinkedIn post about earning a certificate in deep agents"
```

Or with full details:

```bash
python main.py "Write a LinkedIn post about earning a certificate in deep agents. Link to Course: https://example.com, Link to Certificate: https://example.com, Link to project: https://github.com/example"
```

### Default Behavior

If no arguments provided, the agent uses the default query:

```bash
python main.py
```

### Python API

```python
from main import run_agent

result = run_agent("Your LinkedIn post topic here")

# Access the generated post
final_post = result.get("files", {}).get("final_linkedin_post.md", "")
print(final_post)
```

## Workflow

The agent follows this orchestrated workflow:

1. **Parse Request** → Main agent receives user request
2. **Create TODO List** → Break down task into stages (collect sources, draft, validate, score)
3. **Gather Evidence** → Search web for relevant information
4. **Draft Post** → Writer sub-agent creates initial LinkedIn post
5. **Validate** → Validator sub-agent checks factual accuracy and tone
6. **Score** → Scorer sub-agent evaluates quality with pass/fail decision
7. **Revise** (if needed) → Return to writer for improvements
8. **Finalize** → Output final LinkedIn post

All work is persisted to the virtual file system, allowing agents to reference previous outputs and decisions.

## Configuration

### Model Settings

Edit `main.py` to change LLM configuration:

```python
MODEL_NAME = "qwen3.5:latest"          # Ollama model to use
MODEL_BASE_URL = "http://localhost:11434"  # Ollama endpoint
TEMPERATURE = 0.0                       # Deterministic responses
NUM_CTX = 16384 * 2                     # Context window size
```

### Debug Logging

Enable debug logging by setting:

```bash
LINKEDIN_AGENT_DEBUG=1
```

Or disable:

```bash
LINKEDIN_AGENT_DEBUG=0
```

Debug logs include:
- Agent workflow transitions
- Sub-agent delegations
- File operations
- Timing information

## Output Files

All outputs are stored in the virtual file system (accessed via the `files` state field):

- `final_linkedin_post.md` - Final generated LinkedIn post
- `raw_search_*.md` - Web search results
- `draft_post.md` - Initial draft
- `validator_feedback.md` - Validation results
- `scorer_decision.md` - Quality score and recommendations

## Dependencies

Core dependencies:

- `langchain` - AI agent framework
- `langchain-ollama` - Ollama LLM integration
- `langchain-core` - Core LangChain utilities
- `langgraph` - Agentic workflow orchestration
- `tavily-python` - Web search API client
- `markdownify` - HTML to Markdown conversion
- `python-dotenv` - Environment variable management
- `httpx` - HTTP client for web requests

## Troubleshooting

### Issue: Connection refused to `http://localhost:11434`

**Solution**: Ensure Ollama is running:
```bash
ollama serve
```

### Issue: Model not found error

**Solution**: Pull the required model:
```bash
ollama pull qwen3.5:latest
```

### Issue: Tavily API key invalid

**Solution**: 
1. Verify your API key in `.env` file
2. Check that the key is not expired
3. Ensure no extra whitespace in the key

### Issue: No `requirements.txt` file found

**Solution**: Create one with the dependencies listed above, or install directly:
```bash
pip install langchain langchain-ollama langchain-core langgraph tavily-python markdownify python-dotenv httpx
```

## Project Structure

```
LinkedIn_Post_Writer/
├── main.py                 # Main agent entry point
├── state.py               # Extended agent state management
├── prompts.py             # System prompts for all agents
├── subagents.py           # Sub-agent configurations
├── file_tools.py          # Virtual file system tools
├── todo_tools.py          # Task management tools
├── task_tools.py          # Sub-agent delegation
├── webSearch_tools.py     # Web search tools (Tavily)
├── llm_utils.py           # LLM utilities
├── __init__.py            # Package initialization
├── .env                   # Environment configuration (not in git)
└── README.md              # This file
```

## State Management

The agent uses an extended `DeepAgentState` that includes:

- **messages**: Conversation history
- **todos**: Task list tracking workflow progress
- **files**: Virtual file system for state persistence

```python
class DeepAgentState(AgentState):
    todos: list[Todo]  # [{"content": "...", "status": "pending|in_progress|completed"}]
    files: dict[str, str]  # {"filename": "content", ...}
```

## Key Concepts

### Virtual File System

Agents work with a virtual file system stored in state. This allows:
- Persistent data across agent handoffs
- Evidence gathering and reference
- Audit trail of decisions

### Sub-Agent Delegation

The main agent delegates specialized tasks:
- **Writer**: Drafts content with web research
- **Validator**: Checks factual accuracy and tone
- **Scorer**: Evaluates quality and readiness

Each sub-agent has isolated state but shares access to the virtual file system.

### TODO Tracking

Workflows use a structured TODO system:
- Tracks what needs to be done (stages of post creation)
- Maintains progress (pending → in_progress → completed)
- Provides an audit trail of work

## Contributing

To extend this agent:

1. **Add new tools** in dedicated `*_tools.py` modules
2. **Create new sub-agents** in `subagents.py` with clear instructions
3. **Update prompts** in `prompts.py` to guide agent behavior
4. **Test workflows** by running with various LinkedIn post topics

## License

This project is part of the LangChain course materials.

## References

- [LangChain Documentation](https://python.langchain.com/)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [Ollama](https://ollama.ai/)
- [Tavily Search API](https://tavily.com/)

## Contact

For issues or questions about this project, refer to the LangChain course materials or documentation.
