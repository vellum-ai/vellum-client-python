import {
  GENERATED_DISPLAY_MODULE_NAME,
  GENERATED_INPUTS_MODULE_NAME,
  GENERATED_NODES_MODULE_NAME,
} from "src/constants";
import { WorkflowContext } from "src/context";
import { WorkflowNodeDefinition } from "src/types/vellum";
import { createPythonClassName, toSnakeCase } from "src/utils/casing";

export function getGeneratedInputsModulePath(
  workflowContext: WorkflowContext
): string[] {
  let modulePath: string[];
  if (workflowContext.parentNode) {
    modulePath = [
      ...workflowContext.parentNode.getNodeModulePath(),
      GENERATED_INPUTS_MODULE_NAME,
    ];
  } else {
    modulePath = [workflowContext.moduleName, GENERATED_INPUTS_MODULE_NAME];
  }

  return modulePath;
}

export function getGeneratedNodesModulePath(
  workflowContext: WorkflowContext
): string[] {
  let modulePath: string[];
  if (workflowContext.parentNode) {
    modulePath = [
      ...workflowContext.parentNode.getNodeModulePath(),
      GENERATED_NODES_MODULE_NAME,
    ];
  } else {
    modulePath = [workflowContext.moduleName, GENERATED_NODES_MODULE_NAME];
  }

  return modulePath;
}

export function getGeneratedNodeModuleInfo({
  workflowContext,
  nodeDefinition,
  nodeLabel,
}: {
  workflowContext: WorkflowContext;
  nodeDefinition: WorkflowNodeDefinition | undefined;
  nodeLabel: string;
}): { moduleName: string; nodeClassName: string; modulePath: string[] } {
  const moduleName =
    nodeDefinition?.module?.[nodeDefinition.module.length - 1] ??
    toSnakeCase(nodeLabel);

  const nodeClassName =
    nodeDefinition?.name ?? createPythonClassName(nodeLabel);

  const modulePath = [
    ...getGeneratedNodesModulePath(workflowContext),
    moduleName,
  ];
  return { moduleName, nodeClassName, modulePath };
}

export function getGeneratedNodeDisplayModulePath(
  workflowContext: WorkflowContext,
  moduleName: string
): string[] {
  let modulePath: string[];
  if (workflowContext.parentNode) {
    modulePath = [
      ...workflowContext.parentNode.getNodeDisplayModulePath(),
      GENERATED_NODES_MODULE_NAME,
      moduleName,
    ];
  } else {
    modulePath = [
      workflowContext.moduleName,
      GENERATED_DISPLAY_MODULE_NAME,
      GENERATED_NODES_MODULE_NAME,
      moduleName,
    ];
  }

  return modulePath;
}
