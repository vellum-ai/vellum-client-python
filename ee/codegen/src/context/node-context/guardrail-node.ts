import { BaseNodeContext } from "./base";

import { PortContext } from "src/context/port-context";
import { GuardrailNode as GuardrailNodeType } from "src/types/vellum";

export class GuardrailNodeContext extends BaseNodeContext<GuardrailNodeType> {
  // TODO: Figure out a way to correctly get the node outputs from metric definitions
  // https://app.shortcut.com/vellum/story/5348/figure-out-correct-way-to-handle-guardrailnode-output
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
