from typing import Optional, Type

from vellum_ee.workflows.display.types import WorkflowDisplayContext, WorkflowDisplayType
from vellum.workflows.types.generics import WorkflowType


def get_workflow_display(
    *,
    base_display_class: Type[WorkflowDisplayType],
    workflow_class: Type[WorkflowType],
    root_workflow_class: Optional[Type[WorkflowType]] = None,
    parent_display_context: Optional[WorkflowDisplayContext] = None,
) -> WorkflowDisplayType:
    try:
        workflow_display_class = base_display_class.get_from_workflow_display_registry(workflow_class)
    except KeyError:
        try:
            return get_workflow_display(
                base_display_class=base_display_class,
                workflow_class=workflow_class.__bases__[0],
                root_workflow_class=workflow_class if root_workflow_class is None else root_workflow_class,
                parent_display_context=parent_display_context,
            )
        except IndexError:
            return base_display_class(workflow_class)

    if not issubclass(workflow_display_class, base_display_class):
        raise TypeError(
            f"Expected to find a subclass of '{base_display_class.__name__}' for workflow class '{workflow_class.__name__}'"  # noqa: E501
        )

    return workflow_display_class(workflow_class, parent_display_context=parent_display_context)
