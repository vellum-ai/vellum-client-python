import { python } from "@fern-api/python-ast";
import { ClassInstantiation } from "@fern-api/python-ast/ClassInstantiation";
import { MethodArgument } from "@fern-api/python-ast/MethodArgument";
import { AstNode } from "@fern-api/python-ast/core/AstNode";
import { Writer } from "@fern-api/python-ast/core/Writer";
import {
  PromptBlock as PromptBlockType,
  FunctionDefinition as FunctionDefinitionType,
} from "vellum-ai/api";

export declare namespace BasePromptBlock {
  interface Args<T extends PromptBlockType | FunctionDefinitionType> {
    promptBlock: T;
  }
}

export abstract class BasePromptBlock<
  T extends PromptBlockType | FunctionDefinitionType
> extends AstNode {
  private astNode: python.ClassInstantiation;

  public constructor({ promptBlock }: BasePromptBlock.Args<T>) {
    super();
    this.astNode = this.generateAstNode(promptBlock);
  }

  protected abstract generateAstNode(promptBlock: T): ClassInstantiation;

  protected constructCommonClassArguments(promptBlock: T): MethodArgument[] {
    const args: MethodArgument[] = [];

    if (promptBlock.state) {
      args.push(
        new MethodArgument({
          name: "state",
          value: python.TypeInstantiation.str(promptBlock.state),
        })
      );
    }

    const cacheConfigValue = this.extractCacheConfig(promptBlock);
    args.push(
      new MethodArgument({
        name: "cache_config",
        value: cacheConfigValue,
      })
    );

    return args;
  }

  private extractCacheConfig(promptBlock: T): python.TypeInstantiation {
    if (
      promptBlock.cacheConfig !== undefined &&
      promptBlock.cacheConfig !== null
    ) {
      if (promptBlock.cacheConfig.type) {
        return python.TypeInstantiation.str(promptBlock.cacheConfig.type);
      }
    }
    return python.TypeInstantiation.none();
  }

  public write(writer: Writer): void {
    this.astNode.write(writer);
  }
}
