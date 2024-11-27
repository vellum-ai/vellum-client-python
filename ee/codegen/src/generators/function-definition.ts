import { python } from "@fern-api/python-ast";
import { MethodArgument } from "@fern-api/python-ast/MethodArgument";
import { isNil } from "lodash";
import { FunctionDefinition as FunctionDefinitionType } from "vellum-ai/api";

import { VELLUM_CLIENT_MODULE_PATH } from "src/constants";
import { BasePromptBlock } from "src/generators/base-prompt-block";
import { Json } from "src/generators/json";

export class FunctionDefinition extends BasePromptBlock<FunctionDefinitionType> {
  protected generateAstNode(
    functionDefinition: FunctionDefinitionType
  ): python.ClassInstantiation {
    const classArgs: MethodArgument[] = [
      ...this.constructCommonClassArguments(functionDefinition),
    ];

    if (!isNil(functionDefinition.name)) {
      classArgs.push(
        new MethodArgument({
          name: "name",
          value: python.TypeInstantiation.str(functionDefinition.name),
        })
      );
    }

    if (!isNil(functionDefinition.description)) {
      classArgs.push(
        new MethodArgument({
          name: "description",
          value: python.TypeInstantiation.str(functionDefinition.description),
        })
      );
    }

    if (!isNil(functionDefinition.parameters)) {
      classArgs.push(
        new MethodArgument({
          name: "parameters",
          value: new Json(functionDefinition.parameters),
        })
      );
    }

    if (!isNil(functionDefinition.forced)) {
      classArgs.push(
        new MethodArgument({
          name: "function_forced",
          value: python.TypeInstantiation.bool(functionDefinition.forced),
        })
      );
    }

    if (!isNil(functionDefinition.strict)) {
      classArgs.push(
        new MethodArgument({
          name: "function_strict",
          value: python.TypeInstantiation.bool(functionDefinition.strict),
        })
      );
    }

    const functionDefinitionClass = python.instantiateClass({
      classReference: python.reference({
        name: "FunctionDefinition",
        modulePath: VELLUM_CLIENT_MODULE_PATH,
      }),
      arguments_: classArgs,
    });

    this.inheritReferences(functionDefinitionClass);
    return functionDefinitionClass;
  }
}
