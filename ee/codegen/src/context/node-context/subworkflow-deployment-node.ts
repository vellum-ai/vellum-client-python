import { WorkflowDeploymentHistoryItem } from "vellum-ai/api";

import { BaseNodeContext } from "./base";

import { PortContext } from "src/context/port-context";
import { SubworkflowNode as SubworkflowNodeType } from "src/types/vellum";
import { toSnakeCase } from "src/utils/casing";

export declare namespace SubworkflowDeploymentNodeContext {
  interface Args extends BaseNodeContext.Args<SubworkflowNodeType> {
    workflowDeploymentHistoryItem: WorkflowDeploymentHistoryItem;
  }
}

export class SubworkflowDeploymentNodeContext extends BaseNodeContext<SubworkflowNodeType> {
  public workflowDeploymentHistoryItem: WorkflowDeploymentHistoryItem;

  constructor(args: SubworkflowDeploymentNodeContext.Args) {
    super(args);

    this.workflowDeploymentHistoryItem = args.workflowDeploymentHistoryItem;
  }

  getNodeOutputNamesById(): Record<string, string> {
    return this.workflowDeploymentHistoryItem.outputVariables.reduce<
      Record<string, string>
    >((acc, output) => {
      acc[output.id] = toSnakeCase(output.key);
      return acc;
    }, {});
  }

  createPortContexts(): PortContext[] {
    return [
      new PortContext({
        workflowContext: this.workflowContext,
        nodeContext: this,
        portId: this.nodeData.data.sourceHandleId,
      }),
    ];
  }
}
