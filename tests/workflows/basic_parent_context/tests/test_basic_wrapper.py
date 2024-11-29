from uuid import uuid4

from vellum.core.context import get_execution_context, wrapper_execution_parent_context
from vellum.workflows.events.types import NodeParentContext, ParentContext

from tests.workflows.basic_parent_context.basic_workflow import StartNode


class A:
    def __init__(self):
        self._span_id = uuid4()
        self._context = None

    @wrapper_execution_parent_context(
        lambda self: NodeParentContext(node_definition=StartNode().__class__, span_id=self._span_id))
    def test(self):
        self.inner_test()

    @wrapper_execution_parent_context(
        lambda self: NodeParentContext(node_definition=StartNode().__class__, span_id=self._span_id))
    def inner_test(self):
        self._context = get_execution_context().get('parent_context')


def test_basic_wrapper():
    a_instance = A()
    a_instance.test()

    assert a_instance._context == NodeParentContext(
        node_definition=StartNode().__class__,
        span_id=a_instance._span_id,
        parent=NodeParentContext(
            node_definition=StartNode().__class__,
            span_id=a_instance._span_id,
        ),
    )
