import { WorkflowContext } from "src/context";
import { PortContext } from "src/context/port-context";
import { WorkflowDataNode } from "src/types/vellum";
import { toPascalCase, toSnakeCase } from "src/utils/casing";
import {
  getGeneratedNodeDisplayModulePath,
  getGeneratedNodeModulePath,
} from "src/utils/paths";

export declare namespace BaseNodeContext {
  interface Args<T extends WorkflowDataNode> {
    workflowContext: WorkflowContext;
    nodeData: T;
  }
}

export abstract class BaseNodeContext<T extends WorkflowDataNode> {
  protected workflowContext: WorkflowContext;
  public readonly nodeModulePath: string[];
  public readonly nodeModuleName: string;
  public readonly nodeFileName: string;
  public readonly nodeClassName: string;
  public readonly nodeDisplayModulePath: string[];
  public readonly nodeDisplayModuleName: string;
  public readonly nodeDisplayFileName: string;
  public readonly nodeDisplayClassName: string;

  public nodeData: T;

  private readonly nodeOutputNamesById: Record<string, string> = {};
  public readonly portContextsById: Map<string, PortContext>;

  constructor(args: BaseNodeContext.Args<T>) {
    this.workflowContext = args.workflowContext;

    const nodeLabel = args.nodeData.data.label;

    this.nodeModuleName =
      args.nodeData.definition?.module?.[
        args.nodeData.definition.module.length - 1
      ] ?? toSnakeCase(nodeLabel);
    this.nodeFileName = `${this.nodeModuleName}.py`;
    this.nodeClassName =
      args.nodeData.definition?.name ?? toPascalCase(nodeLabel);
    this.nodeModulePath = getGeneratedNodeModulePath(
      args.workflowContext,
      this.nodeModuleName
    );

    this.nodeDisplayModuleName = this.nodeModuleName;
    this.nodeDisplayFileName = `${this.nodeDisplayModuleName}.py`;
    this.nodeDisplayClassName = `${this.nodeClassName}Display`;
    this.nodeDisplayModulePath = getGeneratedNodeDisplayModulePath(
      args.workflowContext,
      this.nodeDisplayModuleName
    );

    this.nodeData = args.nodeData;
    this.nodeOutputNamesById = this.getNodeOutputNamesById();

    const portContexts = this.createPortContexts();
    portContexts.forEach((portContext) => {
      this.workflowContext.addPortContext(portContext);
    });

    this.portContextsById = portContexts.reduce<Map<string, PortContext>>(
      (acc, portContext) => {
        acc.set(portContext.portId, portContext);
        return acc;
      },
      new Map()
    );
  }

  protected abstract getNodeOutputNamesById(): Record<string, string>;
  protected abstract createPortContexts(): PortContext[];

  public getNodeId(): string {
    return this.nodeData.id;
  }

  public getNodeOutputNameById(outputId: string): string {
    const nodeOutputName = this.nodeOutputNamesById[outputId];

    if (!nodeOutputName) {
      throw new Error(`Node output name not found for output ID: ${outputId}`);
    }

    return nodeOutputName;
  }
}
