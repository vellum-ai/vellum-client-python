import { python } from "@fern-api/python-ast";
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
    // Note Nodes intentionally have no body statements.
    return [];
  }

  getNodeDisplayClassBodyStatements(): AstNode[] {
    const statements: AstNode[] = [];

    statements.push(
      python.field({
        name: "text",
        initializer: python.TypeInstantiation.str(
          this.nodeData.data.text ?? ""
        ),
      })
    );

    statements.push(
      python.field({
        name: "style",
        initializer: this.nodeData.data.style
          ? // TODO: https://app.shortcut.com/vellum/story/5147/correctly-convert-json-to-python-dicts
            python.codeBlock(JSON.stringify(this.nodeData.data.style))
          : python.TypeInstantiation.none(),
      })
    );

    return statements;
  }

  getErrorOutputId(): string | undefined {
    return undefined;
  }
}
