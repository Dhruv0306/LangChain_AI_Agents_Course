"""Task delegation tools for LinkedIn post sub-agents."""

from typing import Annotated, NotRequired
from datetime import datetime
from typing_extensions import TypedDict

from langchain.agents import create_agent
from langchain_core.messages import ToolMessage
from langchain_core.tools import BaseTool, InjectedToolCallId, tool
from langgraph.prebuilt import InjectedState
from langgraph.types import Command

from prompts import TASK_DESCRIPTION_PREFIX
from state import DeepAgentState


class SubAgent(TypedDict):
    """Configuration for a specialized sub-agent."""

    name: str
    description: str
    prompt: NotRequired[str]
    system_prompt: NotRequired[str]
    tools: NotRequired[list[str | BaseTool]]


def _create_task_tool(tools, subagents: list[SubAgent], model, state_schema):
    """Create a task delegation tool that enables context isolation through sub-agents."""
    agents = {}

    tools_by_name = {}
    for tool_ in tools:
        if not isinstance(tool_, BaseTool):
            tool_ = tool(tool_)
        tools_by_name[tool_.name] = tool_

    def resolve_tool(item):
        if isinstance(item, BaseTool):
            return item
        return tools_by_name[item]

    def debug_log(message: str) -> None:
        """Print lightweight delegation traces."""
        stamp = datetime.now().strftime("%H:%M:%S")
        print(f"[LinkedIn DEBUG {stamp}] {message}", flush=True)

    for _agent in subagents:
        if "tools" in _agent:
            _tools = [resolve_tool(t) for t in _agent["tools"]]
        else:
            _tools = tools
        system_prompt = _agent.get("system_prompt") or _agent.get("prompt")
        if system_prompt is None:
            raise KeyError(
                f"Sub-agent {_agent['name']} must define either 'system_prompt' or 'prompt'"
            )
        agents[_agent["name"]] = create_agent(
            model, system_prompt=system_prompt, tools=_tools, state_schema=state_schema
        )

    other_agents_string = [
        f"- {_agent['name']}: {_agent['description']}" for _agent in subagents
    ]

    @tool(description=TASK_DESCRIPTION_PREFIX.format(other_agents=other_agents_string))
    def task(
        description: str,
        subagent_type: str,
        state: Annotated[DeepAgentState, InjectedState],
        tool_call_id: Annotated[str, InjectedToolCallId],
    ):
        """Delegate a task to a specialized sub-agent with isolated context."""
        if subagent_type not in agents:
            return f"Error: invoked agent of type {subagent_type}, the only allowed types are {[f'`{k}`' for k in agents]}"

        sub_agent = agents[subagent_type]
        debug_log(f"task tool: delegating to sub-agent '{subagent_type}'")
        state["messages"] = [{"role": "user", "content": description}]
        result = sub_agent.invoke(state)
        debug_log(
            f"task tool: sub-agent '{subagent_type}' returned with {len(result.get('messages', []))} messages"
        )

        return Command(
            update={
                "files": result.get("files", {}),
                "messages": [
                    ToolMessage(
                        result["messages"][-1].content, tool_call_id=tool_call_id
                    )
                ],
            }
        )

    return task
