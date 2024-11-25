import { AstNode } from "@fern-api/python-ast/core/AstNode";

import { NoteNodeContext } from "src/context/node-context/note-node";
import { BaseSingleFileNode } from "src/generators/nodes/bases/single-file-base";
import { NoteNode as NoteNodeType } from "src/types/vellum";

export class NoteNode extends BaseSingleFileNode<
  NoteNodeType,
  NoteNodeContext
> {
  baseNodeClassName = "NoteNode";
  baseNodeDisplayClassName = "BaseNoteNodeDisplay";

  getNodeClassBodyStatements(): AstNode[] {
    const statements: AstNode[] = [];
    return statements;
  }

  getNodeDisplayClassBodyStatements(): AstNode[] {
    const statements: AstNode[] = [];
    return statements;
  }

  getErrorOutputId(): string | undefined {
    return undefined;
  }
}
