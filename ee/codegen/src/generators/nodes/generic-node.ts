import { AstNode } from "@fern-api/python-ast/core/AstNode";

import { GenericNodeContext } from "src/context/node-context/generic-node";
import { BaseSingleFileNode } from "src/generators/nodes/bases/single-file-base";
import { GenericNode as GenericNodeType } from "src/types/vellum";

export class GenericNode extends BaseSingleFileNode<
  GenericNodeType,
  GenericNodeContext
> {
  baseNodeClassName = "BaseNode";
  baseNodeDisplayClassName = "BaseNodeDisplay";

  getNodeClassBodyStatements(): AstNode[] {
    const statements: AstNode[] = [];
    return statements;
  }

  getNodeDisplayClassBodyStatements(): AstNode[] {
    const statements: AstNode[] = [];
    return statements;
  }

  getGenericOutputId(): string | undefined {
    return undefined;
  }
}
