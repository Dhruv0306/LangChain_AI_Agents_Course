"""Sub-agent definitions for the LinkedIn post writing workflow."""

from __future__ import annotations

from typing import Any

from file_tools import ls, read_file, write_file
from prompts import (
    LINKEDIN_POST_WRITER_INSTRUCTIONS,
    LINKEDIN_SCORER_INSTRUCTIONS,
    LINKEDIN_VALIDATOR_INSTRUCTIONS,
)
from todo_tools import read_todos, write_todos
from webSearch_tools import tavily_search, think_tool


WRITER_DESCRIPTION = (
    "Draft the LinkedIn post from verified evidence. Use files and web pages to "
    "gather support, then save raw output before summarizing."
)
VALIDATOR_DESCRIPTION = (
    "Check the draft for factual accuracy, unsupported claims, tone, and "
    "publication readiness."
)
SCORER_DESCRIPTION = (
    "Score the post using the validator feedback and summary, then issue a pass/fail "
    "decision with concrete revision guidance if needed."
)


def build_subagents() -> list[dict[str, Any]]:
    """Return the writer, validator, and scorer sub-agent configurations."""
    writer_tools = [ls, read_file, write_file, tavily_search, think_tool]
    validator_tools = [ls, read_file, write_file, think_tool]
    scorer_tools = [ls, read_file, write_file, think_tool]

    return [
        {
            "name": "writer",
            "description": WRITER_DESCRIPTION,
            "system_prompt": LINKEDIN_POST_WRITER_INSTRUCTIONS,
            "tools": writer_tools,
        },
        {
            "name": "validator",
            "description": VALIDATOR_DESCRIPTION,
            "system_prompt": LINKEDIN_VALIDATOR_INSTRUCTIONS,
            "tools": validator_tools,
        },
        {
            "name": "scorer",
            "description": SCORER_DESCRIPTION,
            "system_prompt": LINKEDIN_SCORER_INSTRUCTIONS,
            "tools": scorer_tools,
        },
    ]


def build_main_tools() -> list[Any]:
    """Return the core tool list used by the main orchestrator."""
    return [
        ls,
        read_file,
        write_file,
        write_todos,
        read_todos,
        tavily_search,
        think_tool,
    ]
