from optparse import Option
from typing import Optional

from vellum.workflows.events.types import (
    NodeParentContext,
    ParentContext,
    PromptDeploymentParentContext,
    WorkflowDeploymentParentContext,
    WorkflowParentContext,
)
from vellum.workflows.events.workflow import WorkflowEvent
from vellum_ee.workflows.display.vellum import CodeResourceDefinition


def is_terminal_event(event: WorkflowEvent) -> bool:
    return event.name in {
        "workflow.execution.fulfilled",
        "workflow.execution.rejected",
        "workflow.execution.paused",
    }


def set_current_context(current_context_json: dict) -> Optional[ParentContext]:
    type_dict = {
        "WORKFLOW": WorkflowParentContext,
        "WORKFLOW_NODE": NodeParentContext,
        "WORKFLOW_RELEASE_TAG": WorkflowDeploymentParentContext,
        "PROMPT_RELEASE_TAG": PromptDeploymentParentContext,
    }
    current_type_value = current_context_json.get("type", "DEFAULT")
    current_type = type_dict.get(current_type_value, None)
    if current_type:
        temp = current_type(**current_context_json)
        return temp
    else:
        return None


def convert_json_to_parent_context(
    context_json: Optional[dict] = None,
) -> Optional[ParentContext]:
    if not context_json:
        return None

    parent = context_json.pop("parent", None)
    new_context: Optional[ParentContext] = set_current_context(context_json)
    parent_context = []
    while parent:
        # go through and build a list with initialized parent context
        current_context_json = parent
        parent = (
            current_context_json.pop("parent", None) if current_context_json else None
        )
        parent_context.append(set_current_context(current_context_json))
    # chain parent context together
    pointer = new_context
    for parent in parent_context:
        if pointer:
            pointer.parent = parent
        pointer = parent

    return new_context
