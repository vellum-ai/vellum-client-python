import { Writer } from "@fern-api/python-ast/core/Writer";

import { workflowContextFactory } from "src/__test__/helpers";
import { inputVariableContextFactory } from "src/__test__/helpers/input-variable-context-factory";
import { InputVariablePointerRule } from "src/generators/node-inputs";

describe("InputVariablePointer", () => {
  let writer: Writer;

  beforeEach(() => {
    writer = new Writer();
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  it("should generate correct Python code", async () => {
    const workflowContext = workflowContextFactory();
    workflowContext.addInputVariableContext(
      inputVariableContextFactory({
        inputVariableData: {
          id: "test-input-id",
          key: "testVariable",
          type: "STRING",
        },
        workflowContext,
      })
    );

    const inputVariablePointer = new InputVariablePointerRule({
      workflowContext: workflowContext,
      nodeInputValuePointerRule: {
        type: "INPUT_VARIABLE",
        data: {
          inputVariableId: "test-input-id",
        },
      },
    });

    inputVariablePointer.write(writer);

    expect(await writer.toStringFormatted()).toMatchSnapshot();
  });
});
