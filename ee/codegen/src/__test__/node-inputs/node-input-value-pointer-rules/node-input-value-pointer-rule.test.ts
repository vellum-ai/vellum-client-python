import { Writer } from "@fern-api/python-ast/core/Writer";

import { workflowContextFactory } from "src/__test__/helpers";
import { WorkflowContext } from "src/context";
import { InputVariableContext } from "src/context/input-variable-context";
import { BaseNodeContext } from "src/context/node-context/base";
import { NodeInputValuePointerRule } from "src/generators/node-inputs/node-input-value-pointer-rules/node-input-value-pointer-rule";
import {
  NodeInputValuePointerRule as NodeInputValuePointerRuleType,
  WorkflowDataNode,
} from "src/types/vellum";

describe("NodeInputValuePointerRule", () => {
  let writer: Writer;
  let workflowContext: WorkflowContext;

  beforeEach(() => {
    writer = new Writer();
    workflowContext = workflowContextFactory();
  });

  it("should generate correct AST for CONSTANT_VALUE pointer", async () => {
    const constantValuePointer: NodeInputValuePointerRuleType = {
      type: "CONSTANT_VALUE",
      data: {
        type: "STRING",
        value: "Hello, World!",
      },
    };

    const rule = new NodeInputValuePointerRule({
      workflowContext: workflowContext,
      nodeInputValuePointerRuleData: constantValuePointer,
    });

    rule.write(writer);
    expect(await writer.toStringFormatted()).toMatchSnapshot();
  });

  it("should generate correct AST for NODE_OUTPUT pointer", async () => {
    vi.spyOn(workflowContext, "getNodeContext").mockReturnValue({
      nodeClassName: "TestNode",
      path: ["nodes", "test-node-path"],
      getNodeOutputNameById: vi.fn().mockReturnValue("my-output"),
    } as unknown as BaseNodeContext<WorkflowDataNode>);

    const nodeOutputPointer: NodeInputValuePointerRuleType = {
      type: "NODE_OUTPUT",
      data: {
        nodeId: "test-node-id",
        outputId: "test-output-id",
      },
    };

    const rule = new NodeInputValuePointerRule({
      workflowContext: workflowContext,
      nodeInputValuePointerRuleData: nodeOutputPointer,
    });

    rule.write(writer);
    expect(await writer.toStringFormatted()).toMatchSnapshot();
  });

  it("should generate correct AST for INPUT_VARIABLE pointer", async () => {
    const mockInputVariable = {
      getInputVariableName: vi.fn().mockReturnValue("test_variable"),
      modulePath: [],
    };
    vi.spyOn(workflowContext, "getInputVariableContextById").mockReturnValue(
      mockInputVariable as unknown as InputVariableContext
    );

    const inputVariablePointer: NodeInputValuePointerRuleType = {
      type: "INPUT_VARIABLE",
      data: {
        inputVariableId: "testInputVariableId",
      },
    };

    const rule = new NodeInputValuePointerRule({
      workflowContext: workflowContext,
      nodeInputValuePointerRuleData: inputVariablePointer,
    });

    rule.write(writer);
    expect(await writer.toStringFormatted()).toMatchSnapshot();
  });
});
