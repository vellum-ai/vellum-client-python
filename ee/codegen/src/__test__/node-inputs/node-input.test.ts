import { Writer } from "@fern-api/python-ast/core/Writer";

import { workflowContextFactory } from "src/__test__/helpers";
import * as codegen from "src/codegen";
import { WorkflowContext } from "src/context";
import { NodeInput as NodeInputType } from "src/types/vellum";

describe("NodeInput", () => {
  let writer: Writer;
  let workflowContext: WorkflowContext;

  beforeEach(() => {
    writer = new Writer();
    workflowContext = workflowContextFactory();
  });

  it("should generate correct Python code", async () => {
    const nodeInputData: NodeInputType = {
      id: "test-input-id",
      key: "test-input-key",
      value: {
        rules: [
          {
            type: "CONSTANT_VALUE",
            data: {
              type: "STRING",
              value: "test-value",
            },
          },
        ],
        combinator: "OR",
      },
    };

    const nodeInput = codegen.nodeInput({
      workflowContext: workflowContext,
      nodeInputData,
    });

    nodeInput.write(writer);

    expect(await writer.toStringFormatted()).toMatchSnapshot();
  });
});
