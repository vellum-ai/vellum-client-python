import { Writer } from "@fern-api/python-ast/core/Writer";
import { VellumVariable } from "vellum-ai/api";

import { workflowContextFactory } from "./helpers";
import { inputVariableContextFactory } from "./helpers/input-variable-context-factory";

import * as codegen from "src/codegen";
import { WorkflowContext } from "src/context";

describe("Inputs", () => {
  let workflowContext: WorkflowContext;
  let writer: Writer;

  beforeEach(() => {
    workflowContext = workflowContextFactory();
    writer = new Writer();
  });

  describe("write", () => {
    it("should generate correct code when Inputs has no variables", async () => {
      const inputs = codegen.inputs({ workflowContext });

      inputs.write(writer);
      expect(await writer.toStringFormatted()).toMatchSnapshot();
    });

    it("should generate correct code when Inputs has variables", async () => {
      const inputVariables: VellumVariable[] = [
        { id: "input1", key: "input1", type: "STRING" },
        { id: "input2", key: "input2", type: "NUMBER" },
      ];
      inputVariables.forEach((inputVariableData) => {
        workflowContext.addInputVariableContext(
          inputVariableContextFactory({
            inputVariableData: inputVariableData,
            workflowContext,
          })
        );
      });
      const inputs = codegen.inputs({ workflowContext });

      inputs.write(writer);
      expect(await writer.toStringFormatted()).toMatchSnapshot();
    });

    it("should generate correct code when Inputs has a custom name", async () => {
      const inputVariables: VellumVariable[] = [
        { id: "input1", key: "input1", type: "STRING" },
      ];
      inputVariables.forEach((inputVariableData) => {
        workflowContext.addInputVariableContext(
          inputVariableContextFactory({
            inputVariableData: inputVariableData,
            workflowContext,
          })
        );
      });
      const inputs = codegen.inputs({
        workflowContext,
        name: "CustomInputs",
      });

      inputs.write(writer);
      expect(await writer.toStringFormatted()).toMatchSnapshot();
    });

    it("should not generate any code when Inputs is empty", async () => {
      const inputs = codegen.inputs({ workflowContext });

      inputs.write(writer);
      expect(await writer.toStringFormatted()).toBe("");
    });

    it("should generate correct code for complex input variables", async () => {
      const inputVariables: VellumVariable[] = [
        { id: "1", key: "query", type: "STRING" },
        { id: "2", key: "max_runtime", type: "NUMBER" },
        { id: "3", key: "previous_chat_history", type: "CHAT_HISTORY" },
        { id: "4", key: "prior_results", type: "SEARCH_RESULTS" },
      ];
      inputVariables.forEach((inputVariableData) => {
        workflowContext.addInputVariableContext(
          inputVariableContextFactory({
            inputVariableData: inputVariableData,
            workflowContext,
          })
        );
      });
      const inputs = codegen.inputs({
        workflowContext,
      });

      inputs.write(writer);
      expect(await writer.toStringFormatted()).toMatchSnapshot();
    });

    it("should convert input variable names into valid python attributes", async () => {
      const inputVariables: VellumVariable[] = [
        { id: "1", key: "My Input", type: "STRING" },
        { id: "2", key: "$My*Input", type: "NUMBER" },
      ];
      inputVariables.forEach((inputVariableData) => {
        workflowContext.addInputVariableContext(
          inputVariableContextFactory({
            inputVariableData: inputVariableData,
            workflowContext,
          })
        );
      });
      const inputs = codegen.inputs({
        workflowContext,
      });

      inputs.write(writer);
      expect(await writer.toStringFormatted()).toMatchSnapshot();
    });
  });
});
