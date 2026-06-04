"""State management for the LinkedIn post writing agent.

This module defines the extended agent state structure that supports:
- task planning and progress tracking through TODO lists
- context offloading through a virtual file system stored in state
- efficient state merging with reducer functions
"""

from typing import Annotated, Literal, NotRequired
from typing_extensions import TypedDict

from langchain.agents import AgentState


class Todo(TypedDict):
    """A structured task item for tracking progress through complex workflows."""

    content: str
    status: Literal["pending", "in_progress", "completed"]


def file_reducer(left, right):
    """Merge two file dictionaries, with right side taking precedence."""
    if left is None:
        return right
    elif right is None:
        return left
    else:
        return {**left, **right}


class DeepAgentState(AgentState):
    """Extended agent state that includes task tracking and virtual file system."""

    todos: NotRequired[list[Todo]]
    files: Annotated[NotRequired[dict[str, str]], file_reducer]
