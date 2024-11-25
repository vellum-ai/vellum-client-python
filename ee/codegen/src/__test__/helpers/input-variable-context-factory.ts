import { VellumVariable } from "vellum-ai/api/types";

import { WorkflowContext } from "src/context";
import { InputVariableContext } from "src/context/input-variable-context";

export function inputVariableContextFactory({
  inputVariableData,
  workflowContext,
}: {
  inputVariableData: VellumVariable;
  workflowContext: WorkflowContext;
}): InputVariableContext {
  return new InputVariableContext({
    inputVariableData,
    workflowContext,
  });
}
