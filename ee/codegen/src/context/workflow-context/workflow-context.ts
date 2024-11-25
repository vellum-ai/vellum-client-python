import { GENERATED_WORKFLOW_MODULE_NAME } from "src/constants";
import { InputVariableContext } from "src/context/input-variable-context";
import { BaseNodeContext } from "src/context/node-context/base";
import { PortContext } from "src/context/port-context";
import { WorkflowOutputContext } from "src/context/workflow-output-context";
import { BaseNode } from "src/generators/nodes/bases";
import { EntrypointNode, WorkflowDataNode } from "src/types/vellum";
import { toPascalCase } from "src/utils/casing";

type InputVariableContextsById = Map<string, InputVariableContext>;

type NodeContextsByNodeId = Map<string, BaseNodeContext<WorkflowDataNode>>;

// A mapping between source handle ids and port contexts
type PortContextById = Map<string, PortContext>;

export declare namespace WorkflowContext {
  export type Args = {
    absolutePathToOutputDirectory: string;
    moduleName: string;
    workflowLabel?: string;
    workflowClassName?: string;
    inputVariableContextsById?: InputVariableContextsById;
    nodeContextsByNodeId?: NodeContextsByNodeId;
    parentNode?: BaseNode<WorkflowDataNode, BaseNodeContext<WorkflowDataNode>>;
    workflowsSdkModulePath?: readonly string[];
    portContextByName?: PortContextById;
  };
}

export class WorkflowContext {
  public readonly absolutePathToOutputDirectory: string;
  public readonly modulePath: string[];
  public readonly moduleName: string;
  public readonly label: string | undefined;
  public readonly workflowClassName: string;

  // Maps workflow input variable IDs to the input variable
  public readonly inputVariableContextsById: InputVariableContextsById;

  // A list of all outputs this workflow produces
  public readonly workflowOutputContexts: WorkflowOutputContext[] = [];

  // Maps node IDs to a mapping of output IDs to output names
  public readonly nodeContextsByNodeId: NodeContextsByNodeId;

  // If this workflow is a nested workflow belonging to a node, track that node's context here.
  public readonly parentNode?: BaseNode<
    WorkflowDataNode,
    BaseNodeContext<WorkflowDataNode>
  >;

  // The entrypoint node for this workflow
  private entrypointNode: EntrypointNode | undefined;

  public readonly sdkModulePathNames: {
    WORKFLOWS_MODULE_PATH: readonly string[];
    WORKFLOWS_DISPLAY_MODULE_PATH: readonly string[];
    NODE_MODULE_PATH: readonly string[];
    INPUTS_MODULE_PATH: readonly string[];
    STATE_MODULE_PATH: readonly string[];
    NODE_DISPLAY_MODULE_PATH: readonly string[];
    NODE_DISPLAY_TYPES_MODULE_PATH: readonly string[];
    VELLUM_TYPES_MODULE_PATH: readonly string[];
    PORTS_MODULE_PATH: readonly string[];
  };

  public readonly portContextById: PortContextById;

  constructor({
    absolutePathToOutputDirectory,
    moduleName,
    workflowLabel,
    workflowClassName,
    inputVariableContextsById,
    nodeContextsByNodeId,
    parentNode,
    workflowsSdkModulePath = ["vellum", "workflows"] as const,
    portContextByName,
  }: WorkflowContext.Args) {
    this.absolutePathToOutputDirectory = absolutePathToOutputDirectory;
    this.moduleName = moduleName;
    this.modulePath = parentNode
      ? [
          ...parentNode.nodeContext.nodeModulePath,
          GENERATED_WORKFLOW_MODULE_NAME,
        ]
      : [this.moduleName, GENERATED_WORKFLOW_MODULE_NAME];
    this.label = workflowLabel || "Workflow";
    this.workflowClassName = workflowClassName || toPascalCase(this.label);

    this.inputVariableContextsById = inputVariableContextsById ?? new Map();
    this.nodeContextsByNodeId = nodeContextsByNodeId ?? new Map();
    this.portContextById = portContextByName ?? new Map();

    this.parentNode = parentNode;

    this.sdkModulePathNames = {
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

  public addEntrypointNode(entrypointNode: EntrypointNode): void {
    if (this.entrypointNode) {
      throw new Error("Entrypoint node already exists");
    }

    this.entrypointNode = entrypointNode;
  }

  public getEntrypointNode(): EntrypointNode {
    if (!this.entrypointNode) {
      throw new Error("Entrypoint node not found");
    }

    return this.entrypointNode;
  }

  public addInputVariableContext(
    inputVariableContext: InputVariableContext
  ): void {
    const inputVariableId = inputVariableContext.getInputVariableId();
    this.inputVariableContextsById.set(inputVariableId, inputVariableContext);
  }

  public getInputVariableContextById(
    inputVariableId: string
  ): InputVariableContext {
    const inputVariableContext =
      this.inputVariableContextsById.get(inputVariableId);

    if (!inputVariableContext) {
      throw new Error(
        `Input variable context not found for ID: ${inputVariableId}`
      );
    }

    return inputVariableContext;
  }

  public addWorkflowOutputContext(
    workflowOutputContext: WorkflowOutputContext
  ): void {
    this.workflowOutputContexts.push(workflowOutputContext);
  }

  public addNodeContext(nodeContext: BaseNodeContext<WorkflowDataNode>): void {
    const nodeId = nodeContext.getNodeId();

    if (this.nodeContextsByNodeId.get(nodeId)) {
      throw new Error(`Node context already exists for node ID: ${nodeId}`);
    }

    this.nodeContextsByNodeId.set(nodeId, nodeContext);
  }

  public getNodeContext<T extends WorkflowDataNode>(
    nodeId: string
  ): BaseNodeContext<T> {
    const nodeContext = this.nodeContextsByNodeId.get(nodeId);

    if (!nodeContext) {
      throw new Error(`Node context not found for node ID: ${nodeId}`);
    }

    return nodeContext as BaseNodeContext<T>;
  }

  public addPortContext(portContext: PortContext): void {
    const portId = portContext.portId;

    if (this.portContextById.get(portId)) {
      throw new Error(`Port context already exists for port id: ${portId}`);
    }
    this.portContextById.set(portId, portContext);
  }

  public getPortContextById(portId: string): PortContext {
    const portContext: PortContext | undefined =
      this.portContextById.get(portId);

    if (!portContext) {
      throw new Error(`Port context not found for port id: ${portId}`);
    }

    return portContext;
  }
}
