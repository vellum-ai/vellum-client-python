import { Writer } from "@fern-api/python-ast/core/Writer";

import {
  nodeContextFactory,
  workflowContextFactory,
} from "src/__test__/helpers";
import { searchNodeDataFactory } from "src/__test__/helpers/node-data-factories";
import { ExecutionCounterPointerRule } from "src/generators/node-inputs/node-input-value-pointer-rules/execution-counter-pointer";

describe("ExecutionCounterPointer", () => {
  let writer: Writer;

  beforeEach(() => {
    writer = new Writer();
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  it("should generate correct Python code", async () => {
    const workflowContext = workflowContextFactory();

    const node = searchNodeDataFactory();
    workflowContext.addNodeContext(
      await nodeContextFactory({ workflowContext, nodeData: node })
    );

    const executionCounterPointer = new ExecutionCounterPointerRule({
      workflowContext: workflowContext,
      nodeInputValuePointerRule: {
        type: "EXECUTION_COUNTER",
        data: {
          nodeId: node.id,
        },
      },
    });

    executionCounterPointer.write(writer);

    expect(await writer.toStringFormatted()).toMatchSnapshot();
  });
});
