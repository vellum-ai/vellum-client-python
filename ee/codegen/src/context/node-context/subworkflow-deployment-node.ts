import { BaseNodeContext } from "./base";

import { PortContext } from "src/context/port-context";
import { SubworkflowNode as SubworkflowNodeType } from "src/types/vellum";

export class SubworkflowDeploymentNodeContext extends BaseNodeContext<SubworkflowNodeType> {
  // TODO: Hit an API to get a subworkflow deployment node's outputs at runtime
  // https://app.shortcut.com/vellum/story/5638/fetch-subworkflow-deployment-node-outputs-via-api
  getNodeOutputNamesById(): Record<string, string> {
    return {};
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
