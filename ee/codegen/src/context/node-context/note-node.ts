import { BaseNodeContext } from "./base";

import { PortContext } from "src/context/port-context";
import { NoteNode } from "src/types/vellum";

export class NoteNodeContext extends BaseNodeContext<NoteNode> {
  baseNodeClassName = "NoteNode";
  baseNodeDisplayClassName = "BaseNoteNodeDisplay";

  getNodeOutputNamesById(): Record<string, string> {
    return {};
  }

  createPortContexts(): PortContext[] {
    return [];
  }
}
