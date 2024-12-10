import { terminalNodeDataFactory } from "src/__test__/helpers/node-data-factories";
import { WorkflowContext } from "src/context";
import { WorkflowOutputContext } from "src/context/workflow-output-context";
import { FinalOutputNode as FinalOutputNodeType } from "src/types/vellum";

export function workflowOutputContextFactory({
  terminalNodeData,
  workflowContext,
}: {
  terminalNodeData?: FinalOutputNodeType;
  workflowContext: WorkflowContext;
}): WorkflowOutputContext {
  return new WorkflowOutputContext({
    terminalNodeData: terminalNodeData ?? terminalNodeDataFactory(),
    workflowContext,
  });
}
