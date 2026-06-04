"""Runnable main agent for the LinkedIn post writing workflow."""

from __future__ import annotations

import sys
import os
from pathlib import Path
from datetime import datetime
from typing import Any

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_ollama import ChatOllama

from llm_utils import format_messages, show_prompt
MODEL_NAME = "qwen3.5:latest"
MODEL_BASE_URL = "http://localhost:11434"
DEBUG = os.getenv("LINKEDIN_AGENT_DEBUG", "1").strip().lower() not in {
    "0",
    "false",
    "no",
}

BASE_DIR = Path(__file__).resolve().parent
ENV_PATH = BASE_DIR / ".env"
if not ENV_PATH.exists():
    ENV_PATH = BASE_DIR.parent / ".env"

load_dotenv(ENV_PATH)

from prompts import (
    FILE_USAGE_INSTRUCTIONS,
    LINKEDIN_MAIN_AGENT_INSTRUCTIONS,
    SUBAGENT_USAGE_INSTRUCTIONS,
    TODO_USAGE_INSTRUCTIONS,
)
from state import DeepAgentState
from subagents import build_main_tools, build_subagents
from task_tools import _create_task_tool


def build_model() -> ChatOllama:
    """Create the chat model used by the main agent and all sub-agents."""
    return ChatOllama(
        model=MODEL_NAME,
        base_url=MODEL_BASE_URL,
        temperature=0.0,
        num_ctx=16384 * 2,
    )


def build_instructions() -> str:
    """Assemble the system prompt for the main LinkedIn orchestrator."""
    return (
        "# TODO MANAGEMENT\n"
        + TODO_USAGE_INSTRUCTIONS
        + "\n\n"
        + "=" * 80
        + "\n\n"
        + "# FILE SYSTEM USAGE\n"
        + FILE_USAGE_INSTRUCTIONS
        + "\n\n"
        + "=" * 80
        + "\n\n"
        + "# SUB-AGENT DELEGATION\n"
        + SUBAGENT_USAGE_INSTRUCTIONS
        + "\n\n"
        + "=" * 80
        + "\n\n"
        + "# LINKEDIN ORCHESTRATION\n"
        + LINKEDIN_MAIN_AGENT_INSTRUCTIONS
    )


def _extract_last_ai_text(messages) -> str:
    """Return the last assistant message text, if any."""
    for message in reversed(messages):
        if message.__class__.__name__.startswith("AI"):
            content = getattr(message, "content", "")
            if isinstance(content, str):
                return content.strip()
            return str(content).strip()
    return ""


def debug_log(message: str) -> None:
    """Print lightweight trace messages when debugging is enabled."""
    if DEBUG:
        stamp = datetime.now().strftime("%H:%M:%S")
        print(f"[LinkedIn DEBUG {stamp}] {message}", flush=True)


def build_agent():
    """Build the main LinkedIn post writing agent."""
    model = build_model()
    tools = build_main_tools()
    subagents = build_subagents()
    task_tool = _create_task_tool(tools, subagents, model, DeepAgentState)
    all_tools = tools + [task_tool]

    instructions = build_instructions()
    agent = create_agent(
        model,
        all_tools,
        system_prompt=instructions,
        state_schema=DeepAgentState,
    )
    return agent, instructions


agent, INSTRUCTIONS = build_agent()


def run_agent(query: str, config: dict[str, Any] | None = None):
    """Run the agent on a single user query and print messages like the notebook."""
    debug_log("main agent: invoke started")
    result = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": query,
                }
            ],
        },
        config=config,
    )
    debug_log(f"main agent: invoke finished with {len(result.get('messages', []))} messages")
    format_messages(result["messages"])

    final_post = result.get("files", {}).get("final_linkedin_post.md", "").strip()
    last_ai_text = _extract_last_ai_text(result.get("messages", []))
    if final_post and final_post != last_ai_text:
        print("\n" + "=" * 80)
        print("Final LinkedIn Post")
        print("=" * 80)
        print(final_post)
        debug_log("rendered final_linkedin_post.md fallback")
    return result


def main() -> None:
    """CLI entry point for manual runs."""
    query = " ".join(sys.argv[1:]).strip()
    if not query:
        query = (
            "Write a LinkedIn post about earning a certificate in deep agents and "
            "make it polished, factual, and concise."
        )
    run_agent(query)


if __name__ == "__main__":
    print(f"Starting LinkedIn Post Writer Agent with model {MODEL_NAME}...")
    print(f"Loaded environment from: {ENV_PATH}")
    debug_log("startup complete; rendering prompt")

    show_prompt(INSTRUCTIONS, title="LinkedIn Main Prompt")
    main()
