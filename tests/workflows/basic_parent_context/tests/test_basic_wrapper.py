from threading import Thread
from uuid import uuid4

from vellum.workflows.context import get_execution_context, get_parent_context, wrapper_execution_context
from vellum.workflows.events.types import NodeParentContext

from tests.workflows.basic_parent_context.basic_workflow import StartNode

constant_span = uuid4()


class A:
    def __init__(self, span_id):
        self._span_id = span_id
        self._context = None

    @wrapper_execution_context(
        parent_context=NodeParentContext(node_definition=StartNode.__class__, span_id=constant_span)
    )
    def test(self):
        self.inner_test(
            parent_context=NodeParentContext(
                node_definition=StartNode.__class__, span_id=self._span_id, parent=get_parent_context()
            )
        )

    @wrapper_execution_context()
    def inner_test(self):
        self._context = get_execution_context().get("parent_context")

    @wrapper_execution_context(
        parent_context=NodeParentContext(node_definition=StartNode.__class__, span_id=constant_span)
    )
    def threaded_work(self, node, span_id):
        self._context = get_execution_context().get("parent_context")


def test_basic_wrapper():
    a_instance = A(uuid4())
    a_instance.inner_test()

    assert a_instance._context is None

    a_instance.test()

    assert a_instance._context == NodeParentContext(
        node_definition=StartNode.__class__,
        span_id=a_instance._span_id,
        parent=NodeParentContext(
            node_definition=StartNode.__class__,
            span_id=constant_span,
        ),
    )


def test_threaded_wrapper():
    a_instance = A(uuid4())
    node = StartNode()
    node_span_id = uuid4()

    worker_thread = Thread(
        target=a_instance.threaded_work,
        kwargs={"node": node, "span_id": node_span_id},
    )
    worker_thread.start()
    worker_thread.join()

    assert a_instance._context == NodeParentContext(
        node_definition=StartNode.__class__,
        span_id=constant_span,
    )
