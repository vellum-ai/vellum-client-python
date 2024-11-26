import { BaseNodeContext } from "src/context/node-context/base";
import { PortContext } from "src/context/port-context";
import { GenericNode as GenericNodeType } from "src/types/vellum";

export class GenericNodeContext extends BaseNodeContext<GenericNodeType> {
  getNodeOutputNamesById(): Record<string, string> {
    return {};
  }

  protected createPortContexts(): PortContext[] {
    return [];
  }
}
