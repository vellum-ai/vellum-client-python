export function generateSdkModulePaths(
  workflowsSdkModulePath: Readonly<string[]>
) {
  return {
    WORKFLOWS_MODULE_PATH: workflowsSdkModulePath,
    WORKFLOWS_DISPLAY_MODULE_PATH: [
      "vellum_ee",
      "workflows",
      "display",
      "workflows",
      "vellum_workflow_display",
    ] as const,
    NODE_MODULE_PATH: [
      ...workflowsSdkModulePath,
      "nodes",
      "displayable",
    ] as const,
    INPUTS_MODULE_PATH: [...workflowsSdkModulePath, "inputs"] as const,
    STATE_MODULE_PATH: [...workflowsSdkModulePath, "state"] as const,
    NODE_DISPLAY_MODULE_PATH: [
      "vellum_ee",
      "workflows",
      "display",
      "nodes",
    ] as const,
    NODE_DISPLAY_TYPES_MODULE_PATH: [
      "vellum_ee",
      "workflows",
      "display",
      "nodes",
      "types",
    ] as const,
    VELLUM_TYPES_MODULE_PATH: [
      "vellum_ee",
      "workflows",
      "display",
      "vellum",
    ] as const,
    PORTS_MODULE_PATH: [...workflowsSdkModulePath, "ports"] as const,
  };
}
