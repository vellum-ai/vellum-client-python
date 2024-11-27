import { Writer } from "@fern-api/python-ast/core/Writer";
import { beforeEach } from "vitest";

import { workflowContextFactory } from "src/__test__/helpers";
import { inputVariableContextFactory } from "src/__test__/helpers/input-variable-context-factory";
import { conditionalNodeFactory } from "src/__test__/helpers/node-data-factories";
import { createNodeContext, WorkflowContext } from "src/context";
import { ConditionalNodeContext } from "src/context/node-context/conditional-node";
import { ConditionalNode } from "src/generators/nodes/conditional-node";

describe("ConditionalNode", () => {
  let workflowContext: WorkflowContext;
  let writer: Writer;
  let node: ConditionalNode;

  beforeEach(async () => {
    workflowContext = workflowContextFactory();
    writer = new Writer();

    const nodeData = conditionalNodeFactory();

    workflowContext.addInputVariableContext(
      inputVariableContextFactory({
        inputVariableData: {
          id: "d2287fee-98fb-421c-9464-e54d8f70f046",
          key: "field",
          type: "STRING",
        },
        workflowContext,
      })
    );

    const nodeContext = (await createNodeContext({
      workflowContext,
      nodeData,
    })) as ConditionalNodeContext;
    workflowContext.addNodeContext(nodeContext);

    node = new ConditionalNode({
      workflowContext,
      nodeContext,
    });
  });

  it("getNodeFile", async () => {
    node.getNodeFile().write(writer);
    expect(await writer.toStringFormatted()).toMatchSnapshot();
  });

  it("getNodeDisplayFile", async () => {
    node.getNodeDisplayFile().write(writer);
    expect(await writer.toStringFormatted()).toMatchSnapshot();
  });
});
