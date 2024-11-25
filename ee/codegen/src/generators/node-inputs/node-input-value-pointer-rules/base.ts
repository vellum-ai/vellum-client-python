import { AstNode } from "@fern-api/python-ast/core/AstNode";
import { Writer } from "@fern-api/python-ast/core/Writer";

import { WorkflowContext } from "src/context";
import { NodeInputValuePointerRule as NodeInputValuePointerRuleType } from "src/types/vellum";

export declare namespace BaseNodeInputValuePointerRule {
  export interface Args<T extends NodeInputValuePointerRuleType> {
    workflowContext: WorkflowContext;
    nodeInputValuePointerRule: T;
  }
}

export abstract class BaseNodeInputValuePointerRule<
  T extends NodeInputValuePointerRuleType
> extends AstNode {
  public readonly workflowContext: WorkflowContext;
  public readonly nodeInputValuePointerRule: T;
  private astNode: AstNode;

  constructor({
    workflowContext,
    nodeInputValuePointerRule,
  }: BaseNodeInputValuePointerRule.Args<T>) {
    super();
    this.workflowContext = workflowContext;
    this.nodeInputValuePointerRule = nodeInputValuePointerRule;

    this.astNode = this.getAstNode();
    this.inheritReferences(this.astNode);
  }

  abstract getAstNode(): AstNode;

  public write(writer: Writer): void {
    this.astNode.write(writer);
  }
}
