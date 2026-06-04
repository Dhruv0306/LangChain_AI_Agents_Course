# Learning How to Build Multi-Agents Systems using LangChain Framework

A comprehensive educational framework for building sophisticated LangChain agents with advanced context management, multi-agent orchestration, and production-grade patterns inspired by systems like Manus, Anthropic's research system, and Hugging Face's Open Deep Research.

📚 **[Take the Course: Deep Agents with LangGraph](https://academy.langchain.com/courses/deep-agents-with-langgraph)**

## 🎯 Project Overview

This repository teaches **context engineering** — the art of managing token budgets and information flow in large language model systems. You'll learn three progressive patterns:

1. **TODO Lists** → Prevent agent mission drift
2. **Virtual Filesystems** → Offload token-heavy results
3. **Sub-agents** → Isolate contexts for specialized tasks

These patterns combine into a production-grade multi-agent system capable of complex research, validation, and quality scoring workflows.

## 📚 Learning Progression

Start with `0_create_agent.ipynb` and progress sequentially. Each notebook builds on the previous, introducing one new concept at a time.

### Notebooks (0-4)

| Notebook | Focus | What You'll Learn |
|----------|-------|-------------------|
| **0_create_agent.ipynb** | ReAct Agent Fundamentals | Basic agent creation, the reasoning loop, LangGraph state/messages, tools |
| **1_todo.ipynb** | TODO Planning System | Task tracking, attention management, preventing agent hallucination/drift |
| **2_files.ipynb** | Context Offloading | Virtual filesystem in agent state, managing 50+ tool calls without token explosion |
| **3_subagents.ipynb** | Context Isolation | Sub-agent delegation with independent contexts, specialized tool sets |
| **4_full_agent.ipynb** | Full Research Agent | Integration: TODOs + files + sub-agents + web search in a complete system |

Each notebook is ~200 lines, runnable end-to-end, and demonstrates patterns applicable to production systems.

## 📁 Project Structure

```
e:\LangChain/
├── README.md                           # This file
├── llm_utils.py                        # Shared LLM utilities
├── 0_create_agent.ipynb                # Tutorial: Agent basics
├── 1_todo.ipynb                        # Tutorial: TODO system
├── 2_files.ipynb                       # Tutorial: Virtual filesystem
├── 3_subagents.ipynb                   # Tutorial: Sub-agents
├── 4_full_agent.ipynb                  # Tutorial: Full integration
├── assets/                             # Sample outputs
├── deep_agents_from_scratch/           # Reusable framework module
│   ├── __init__.py
│   ├── state.py                        # DeepAgentState with TODOs + files
│   ├── file_tools.py                   # ls(), read_file(), write_file()
│   ├── todo_tools.py                   # read_todos(), write_todos()
│   ├── task_tools.py                   # Sub-agent delegation
│   ├── research_tools.py               # Web search + summarization
│   └── prompts.py                      # System prompts & tool descriptions
└── LinkedIn_Post_Writer/               # Production example: multi-agent orchestrator
    ├── main.py                         # Entry point & orchestrator agent
    ├── subagents.py                    # Writer, Validator, Scorer configs
    ├── state.py                        # Extended state for post workflow
    ├── file_tools.py                   # File operations for agents
    ├── todo_tools.py                   # Task tracking
    ├── task_tools.py                   # Sub-agent management
    ├── webSearch_tools.py              # Tavily search integration
    ├── prompts.py                      # Role-specific prompts
    ├── llm_utils.py                    # LLM configuration
    ├── README.md                       # Project-specific docs
    └── assets/                         # Generated posts, reports, summaries
```

## 🧠 Key Modules

### `deep_agents_from_scratch/` — The Framework

A reusable, production-ready agent framework providing:

- **State Management** (`state.py`): Extended LangGraph state with TODO lists and virtual filesystem
- **File Tools** (`file_tools.py`): `ls()`, `read_file()`, `write_file()` for managing context
- **TODO Tools** (`todo_tools.py`): `read_todos()`, `write_todos()` for task tracking
- **Task Tools** (`task_tools.py`): Framework for delegating to sub-agents with isolated contexts
- **Research Tools** (`research_tools.py`): Web search (Tavily) with LLM-powered summarization
- **Prompts** (`prompts.py`): System prompts and tool descriptions for all agent types

### `LinkedIn_Post_Writer/` — Production Example

A complete multi-agent orchestrator demonstrating the framework in action:

**Architecture:**
- **Main Orchestrator**: Coordinates workflow, manages state, delegates tasks
- **Writer Sub-agent**: Researches and drafts posts from sources
- **Validator Sub-agent**: Verifies factual accuracy and tone
- **Scorer Sub-agent**: Evaluates quality and gates release

**How it works:**
1. Orchestrator receives request (topic + links)
2. Creates TODO list for context management
3. Delegates writing to Writer agent with web search
4. Passes draft to Validator for fact-checking
5. Sends validated draft to Scorer for quality assessment
6. Saves artifacts (drafts, reports, final post) to `assets/`

**Run example:**
```bash
cd LinkedIn_Post_Writer
python main.py "Write a LinkedIn post about [topic]. Link to Course: [URL]"
```

## 🚀 Quick Start

### Prerequisites

- **Python 3.10+**
- **LangChain** & **LangGraph**
- **Ollama** (for local LLM inference)
- **Tavily API key** (for web search)

### Setup

1. Install dependencies:
```bash
pip install -r requirements.txt  # If available, otherwise:
pip install langchain langgraph langchain-community langchain-ollama tavily-python
```

2. Ensure Ollama is running with `qwen3.5:latest`:
```bash
ollama pull qwen3.5:latest
ollama serve
```

3. Set environment variables:
```bash
export TAVILY_API_KEY="your-key-here"
```

### Tutorial Path

Start with the notebooks in order:

```bash
# Terminal 1: Start Ollama
ollama serve

# Terminal 2: Open notebook 0 and run cells
jupyter notebook 0_create_agent.ipynb
```

Then progress to notebooks 1-4, each taking ~15 minutes.

### Run Production Example

After completing tutorials, try the multi-agent orchestrator:

```bash
cd LinkedIn_Post_Writer
python main.py "Write about AI agents. Link: https://example.com"
```

Outputs save to `LinkedIn_Post_Writer/assets/`.

## 🔑 Key Concepts

### Context Management Patterns

**1. TODO Lists**
- Agent reads a structured task list at each step
- Prevents hallucination by keeping focus narrow
- Essential for long-running workflows

**2. Virtual Filesystem**
- Store results in agent state (as dictionary of files)
- Tools: `read_file()`, `write_file()`, `ls()`
- Keeps context window alive even with 50+ tool calls
- Example: Save research results, validation reports, drafts

**3. Sub-agents**
- Delegate specialized tasks to isolated agent instances
- Each has independent state and customized tools
- Prevents context clash (Writer doesn't see Validator's logic)
- Example: Writer searches, Validator fact-checks, Scorer evaluates

### ReAct Framework

The underlying reasoning loop: **Reason** → **Act** → **Observe**

- Agent thinks about what to do
- Executes a tool call
- Observes the result
- Repeats until task is complete

## 🏗️ Architecture Patterns

### State Structure
```python
class DeepAgentState(TypedDict):
    messages: list[BaseMessage]      # Conversation history
    todos: list[str]                  # Current task list
    files: dict[str, str]             # Virtual filesystem
    iteration_count: int              # Prevent infinite loops
```

### Tool Design
- **Deterministic**: Same input always produces same output
- **Observable**: Result clearly visible to agent
- **Composable**: Tools work well together
- **Bounded**: Prevent runaway token usage

### Reducer Functions
- Efficiently merge state updates
- Example: `file_reducer` appends to files instead of rewriting
- Optimized for token management

## 📊 Example Workflow (LinkedIn Post Writer)

```
User Request
    ↓
[Orchestrator Agent]
├─ Create TODO list
├─ Store request in files
    ↓
    └─→ [Writer Sub-agent] (isolated context)
        ├─ Search web for sources
        ├─ Summarize findings
        └─ Draft post → save to files
    ↓
    └─→ [Validator Sub-agent] (isolated context)
        ├─ Fact-check claims
        ├─ Verify tone
        └─ Report issues → save to files
    ↓
    └─→ [Scorer Sub-agent] (isolated context)
        ├─ Evaluate quality
        ├─ Rate engagement
        └─ Gate decision → save to files
    ↓
Final Post + Reports (in assets/)
```

## 💡 Use Cases

This framework is ideal for:

- **Research Agents**: Gather, synthesize, and validate information
- **Content Generation**: Multi-stage workflows with quality gates
- **Code Assistants**: Specialized agents for different tasks
- **Task Orchestration**: Complex multi-step processes with context isolation
- **Learning**: Understanding how production LLM systems manage context

## 🔧 Configuration

### LLM Settings
Edit model selection in each notebook or `llm_utils.py`:
- Default: `qwen3.5:latest` (via Ollama)
- Supports any LangChain LLM provider

### Tool Customization
- Add new tools to any module by defining functions with `@tool` decorator
- Update `prompts.py` with tool descriptions
- Pass to agent via `tools` parameter in `create_agent()`

### Sub-agent Creation
See `LinkedIn_Post_Writer/subagents.py` for pattern:
```python
writer_agent = create_agent(
    model=model,
    tools=[read_files, search_web, write_files],
    system_prompt=WRITER_SYSTEM_PROMPT
)
```

## 📖 Learning Resources

- **LangChain Docs**: https://python.langchain.com/
- **LangGraph**: https://langchain-ai.github.io/langgraph/
- **ReAct Paper**: https://arxiv.org/abs/2210.03629
- **Tavily Search**: https://tavily.com/

## 🤝 Contributing

This is an educational framework. Feel free to:
- Extend it with new tools or modules
- Adapt patterns for your own agents
- Share improvements back

## 📝 License

MIT (adjust as needed)

## 🎓 Course Context

This repository is part of the **[LangChain Academy: Deep Agents with LangGraph](https://academy.langchain.com/courses/deep-agents-with-langgraph)** course. It implements production patterns from research systems at:
- Anthropic (Claude research)
- Hugging Face (Open Deep Research)
- Manus (multi-agent orchestration)

---

**Start learning**: Open `0_create_agent.ipynb` and run the first cell! 🚀
