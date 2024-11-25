import { BaseNodeContext } from "./base";

import { PortContext } from "src/context/port-context";
import { SearchNode } from "src/types/vellum";

export class TextSearchNodeContext extends BaseNodeContext<SearchNode> {
  getNodeOutputNamesById(): Record<string, string> {
    return {
      [this.nodeData.data.resultsOutputId]: "results",
      [this.nodeData.data.textOutputId]: "text",
      ...(this.nodeData.data.errorOutputId
        ? { [this.nodeData.data.errorOutputId]: "error" }
        : {}),
    };
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
