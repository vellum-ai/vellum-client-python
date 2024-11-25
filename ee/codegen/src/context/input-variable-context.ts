import { VellumVariable } from "vellum-ai/api/types";

import { WorkflowContext } from "src/context/workflow-context";
import { toSnakeCase } from "src/utils/casing";
import { getGeneratedInputsModulePath } from "src/utils/paths";

export declare namespace InputVariableContext {
  export type Args = {
    inputVariableData: VellumVariable;
    workflowContext: WorkflowContext;
  };
}

export class InputVariableContext {
  private readonly workflowContext: WorkflowContext;
  private readonly inputVariableData: VellumVariable;
  public readonly modulePath: string[];

  constructor({
    inputVariableData,
    workflowContext,
  }: InputVariableContext.Args) {
    this.workflowContext = workflowContext;
    this.inputVariableData = inputVariableData;
    this.modulePath = getGeneratedInputsModulePath(workflowContext);
  }

  public getInputVariableId(): string {
    return this.inputVariableData.id;
  }

  public getInputVariableName(): string {
    return toSnakeCase(this.inputVariableData.key);
  }

  public getInputVariableData(): VellumVariable {
    return this.inputVariableData;
  }
}
