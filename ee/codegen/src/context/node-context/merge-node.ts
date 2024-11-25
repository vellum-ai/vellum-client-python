import { BaseNodeContext } from "./base";

import { PortContext } from "src/context/port-context";
import { MergeNode } from "src/types/vellum";

export class MergeNodeContext extends BaseNodeContext<MergeNode> {
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