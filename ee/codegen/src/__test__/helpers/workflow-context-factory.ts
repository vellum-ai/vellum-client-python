import { WorkflowContext } from "src/context";

export function workflowContextFactory({
  absolutePathToOutputDirectory,
  moduleName,
  workflowLabel,
  workflowClassName,
}: Partial<WorkflowContext.Args> = {}): WorkflowContext {
  return new WorkflowContext({
    absolutePathToOutputDirectory:
      absolutePathToOutputDirectory || "./src/__tests__/",
    moduleName: moduleName || "code",
    workflowClassName: workflowLabel || "Workflow",
    workflowLabel: workflowClassName || "Workflow",
    vellumApiKey: "<TEST_API_KEY>",
  });
}
