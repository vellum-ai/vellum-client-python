import { Writer } from "@fern-api/python-ast/core/Writer";

import { workflowContextFactory } from "src/__test__/helpers";
import { InputVariableContext } from "src/context/input-variable-context";
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
    const mockInputVariable = {
      getInputVariableName: vi.fn().mockReturnValue("test-variable"),
      modulePath: [],
    };
    vi.spyOn(workflowContext, "getInputVariableContextById").mockReturnValue(
      mockInputVariable as unknown as InputVariableContext
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
