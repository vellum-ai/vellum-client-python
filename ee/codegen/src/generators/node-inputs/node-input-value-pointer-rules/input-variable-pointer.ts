import { python } from "@fern-api/python-ast";

import { BaseNodeInputValuePointerRule } from "./base";

import { InputVariablePointer } from "src/types/vellum";
import { toSnakeCase } from "src/utils/casing";

export class InputVariablePointerRule extends BaseNodeInputValuePointerRule<InputVariablePointer> {
  getAstNode(): python.Reference {
    const inputVariablePointerRuleData = this.nodeInputValuePointerRule.data;

    const inputVariableContext =
      this.workflowContext.getInputVariableContextById(
        inputVariablePointerRuleData.inputVariableId
      );

    return python.reference({
      name: "Inputs",
      modulePath: inputVariableContext.modulePath,
      attribute: [toSnakeCase(inputVariableContext.getInputVariableName())],
    });
  }
}
