import { python } from "@fern-api/python-ast";
import { AstNode } from "@fern-api/python-ast/core/AstNode";
import { Writer } from "@fern-api/python-ast/core/Writer";

import { VELLUM_CLIENT_MODULE_PATH } from "src/constants";
import {
  VellumLogicalCondition as VellumLogicalConditionType,
  VellumLogicalConditionGroup as VellumLogicalConditionGroupType,
  VellumLogicalExpression as VellumLogicalExpressionType,
} from "src/types/vellum";

export declare namespace MetadataFilters {
  export interface Args {
    metadata: VellumLogicalExpressionType;
  }
}

export class MetadataFilters extends AstNode {
  private metadata: VellumLogicalExpressionType;
  private astNode: AstNode;

  public constructor(args: MetadataFilters.Args) {
    super();

    this.metadata = args.metadata;
    this.astNode = this.generateAstNode();
    this.inheritReferences(this.astNode);
  }

  private generateAstNode(): AstNode {
    switch (this.metadata.type) {
      case "LOGICAL_CONDITION":
        return this.generateLogicalConditionArguments(this.metadata);
      case "LOGICAL_CONDITION_GROUP":
        return this.generateLogicalConditionGroupArguments(this.metadata);
    }
  }

  private generateLogicalConditionGroupArguments(
    data: VellumLogicalConditionGroupType
  ): python.ClassInstantiation {
    const processCondition = (
      condition: VellumLogicalExpressionType
    ): AstNode => {
      if (condition.type === "LOGICAL_CONDITION") {
        return this.generateLogicalConditionArguments(condition);
      } else {
        return this.generateLogicalConditionGroupArguments(condition);
      }
    };

    const processedConditions: AstNode[] = data.conditions.map((condition) =>
      processCondition(condition)
    );

    return python.instantiateClass({
      classReference: python.reference({
        name: "VellumValueLogicalConditionGroupRequest",
        modulePath: [...VELLUM_CLIENT_MODULE_PATH, "types"],
      }),
      arguments_: [
        python.methodArgument({
          name: "type",
          value: python.TypeInstantiation.str("LOGICAL_CONDITION_GROUP"),
        }),
        python.methodArgument({
          name: "combinator",
          value: python.TypeInstantiation.str(data.combinator),
        }),
        python.methodArgument({
          name: "negated",
          value: python.TypeInstantiation.bool(data.negated),
        }),
        python.methodArgument({
          name: "conditions",
          value: python.TypeInstantiation.list(processedConditions),
        }),
      ],
    });
  }

  private generateLogicalConditionArguments(
    data: VellumLogicalConditionType
  ): python.ClassInstantiation {
    const lhsId = data.lhsVariableId;

    const rhsId = data.rhsVariableId;

    return python.instantiateClass({
      classReference: python.reference({
        name: "VellumValueLogicalConditionRequest",
        modulePath: [...VELLUM_CLIENT_MODULE_PATH, "types"],
      }),
      arguments_: [
        python.methodArgument({
          name: "type",
          value: python.TypeInstantiation.str("LOGICAL_CONDITION"),
        }),
        python.methodArgument({
          name: "lhs_variable",
          value: python.instantiateClass({
            classReference: python.reference({
              name: "StringVellumValueRequest",
              modulePath: [...VELLUM_CLIENT_MODULE_PATH, "types"],
            }),
            arguments_: [
              python.methodArgument({
                name: "type",
                value: python.TypeInstantiation.str("STRING"),
              }),
              python.methodArgument({
                name: "value",
                value: python.TypeInstantiation.str(lhsId),
              }),
            ],
          }),
        }),
        python.methodArgument({
          name: "operator",
          value: python.TypeInstantiation.str(data.operator),
        }),
        python.methodArgument({
          name: "rhs_variable",
          value: python.instantiateClass({
            classReference: python.reference({
              name: "StringVellumValueRequest",
              modulePath: [...VELLUM_CLIENT_MODULE_PATH, "types"],
            }),
            arguments_: [
              python.methodArgument({
                name: "type",
                value: python.TypeInstantiation.str("STRING"),
              }),
              python.methodArgument({
                name: "value",
                value: python.TypeInstantiation.str(rhsId),
              }),
            ],
          }),
        }),
      ],
    });
  }

  public write(writer: Writer): void {
    this.astNode.write(writer);
  }
}
