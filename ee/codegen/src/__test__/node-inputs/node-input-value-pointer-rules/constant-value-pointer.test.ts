import { Writer } from "@fern-api/python-ast/core/Writer";

import { workflowContextFactory } from "src/__test__/helpers";
import { WorkflowContext } from "src/context";
import { ConstantValuePointerRule } from "src/generators/node-inputs/node-input-value-pointer-rules/constant-value-pointer";
import { ConstantValuePointer } from "src/types/vellum";

describe("ConstantValuePointer", () => {
  let workflowContext: WorkflowContext;

  beforeEach(() => {
    workflowContext = workflowContextFactory();
  });

  it("should generate correct AST for STRING constant value", async () => {
    const constantValuePointer: ConstantValuePointer = {
      type: "CONSTANT_VALUE",
      data: {
        type: "STRING",
        value: "Hello, World!",
      },
    };

    const rule = new ConstantValuePointerRule({
      workflowContext: workflowContext,
      nodeInputValuePointerRule: constantValuePointer,
    });

    const writer = new Writer();
    rule.write(writer);

    expect(await writer.toStringFormatted()).toMatchSnapshot();
  });
});
