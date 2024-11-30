import { BaseNode } from "./base";

import { WorkflowContext } from "src/context";
import { BaseNodeContext } from "src/context/node-context/base";
import { WorkflowProjectGenerator } from "src/project";
import { WorkflowDataNode, WorkflowRawData } from "src/types/vellum";

export abstract class BaseNestedWorkflowNode<
  T extends WorkflowDataNode,
  V extends BaseNodeContext<T>
> extends BaseNode<T, V> {
  protected static readonly subworkflowNestedProjectName = "subworkflow";
  protected readonly nestedWorkflowContextsByName: Map<string, WorkflowContext>;
  protected readonly nestedProjectsByName: Map<
    string,
    WorkflowProjectGenerator
  >;

  protected abstract getNestedWorkflowProject(): WorkflowProjectGenerator;

  protected abstract getInnerWorkflowData(): WorkflowRawData;

  constructor(args: BaseNode.Args<T, V>) {
    super(args);

    this.nestedWorkflowContextsByName = this.generateNestedWorkflowContexts();
    this.nestedProjectsByName = this.generateNestedProjectsByName();
  }

  public getNestedProjects(): WorkflowProjectGenerator[] {
    return Array.from(this.nestedProjectsByName.values());
  }

  protected getNestedWorkflowContextByName(name: string): WorkflowContext {
    const nestedWorkflowContext = this.nestedWorkflowContextsByName.get(name);

    if (!nestedWorkflowContext) {
      throw new Error(
        `Nested workflow context not found for attribute name: ${name}`
      );
    }

    return nestedWorkflowContext;
  }

  protected generateNestedProjectsByName(): Map<
    string,
    WorkflowProjectGenerator
  > {
    return new Map([
      [
        BaseNestedWorkflowNode.subworkflowNestedProjectName,
        this.getNestedWorkflowProject(),
      ],
    ]);
  }

  protected generateNestedWorkflowContexts(): Map<string, WorkflowContext> {
    const nestedWorkflowLabel = `${this.nodeContext.getNodeLabel()} Workflow`;

    const innerWorkflowData = this.getInnerWorkflowData();

    const nestedWorkflowContext =
      this.workflowContext.createNestedWorkflowContext({
        workflowLabel: nestedWorkflowLabel,
        parentNode: this,
        workflowRawEdges: innerWorkflowData.edges,
      });

    return new Map([
      [
        BaseNestedWorkflowNode.subworkflowNestedProjectName,
        nestedWorkflowContext,
      ],
    ]);
  }
}
