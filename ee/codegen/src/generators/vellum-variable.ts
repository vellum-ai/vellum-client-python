import { python } from "@fern-api/python-ast";
import { AstNode } from "@fern-api/python-ast/core/AstNode";
import { Writer } from "@fern-api/python-ast/core/Writer";
import { VellumValue } from "vellum-ai/api/types";

import { WorkflowContext } from "src/context";
import { getVellumVariablePrimitiveType } from "src/utils/vellum-variables";

type VellumVariableWithName = (VellumValue | { type: "NULL"; value?: null }) &
  ({ name: string; key?: undefined } | { name?: undefined; key: string }) & {
    id: string;
  };

export declare namespace VellumVariable {
  interface Args {
    workflowContext: WorkflowContext;
    variable: VellumVariableWithName;
    initializer?: AstNode;
  }
}

export class VellumVariable extends AstNode {
  private readonly field: python.Field;

  constructor({ workflowContext, variable, initializer }: VellumVariable.Args) {
    super();
    this.field = python.field({
      name: variable.name ?? variable.key,
      type: getVellumVariablePrimitiveType({
        type: variable.type,
        workflowContext,
      }),
      initializer,
    });
    this.inheritReferences(this.field);
  }

  public write(writer: Writer): void {
    this.field.write(writer);
  }
}
