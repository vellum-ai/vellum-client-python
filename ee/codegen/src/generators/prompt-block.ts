import { python } from "@fern-api/python-ast";
import { ClassInstantiation } from "@fern-api/python-ast/ClassInstantiation";
import { MethodArgument } from "@fern-api/python-ast/MethodArgument";
import { AstNode } from "@fern-api/python-ast/core/AstNode";
import { Writer } from "@fern-api/python-ast/core/Writer";
import {
  PromptBlock as PromptBlockType,
  JinjaPromptBlock as JinjaPromptBlockType,
  ChatMessagePromptBlock as ChatMessagePromptBlockType,
  FunctionDefinitionPromptBlock as FunctionDefinitionPromptBlockType,
  VariablePromptBlock as VariablePromptBlockType,
  RichTextPromptBlock as RichTextPromptBlockType,
  PlainTextPromptBlock as PlainTextPromptBlockType,
} from "vellum-ai/api";

import { VELLUM_CLIENT_MODULE_PATH } from "src/constants";

export declare namespace PromptBlock {
  interface Args {
    promptBlock: PromptBlockType;
  }
}

// Flesh out unit tests for various prompt configurations
// https://app.shortcut.com/vellum/story/5249
export class PromptBlock extends AstNode {
  private promptBlock: python.ClassInstantiation;

  public constructor({ promptBlock }: PromptBlock.Args) {
    super();
    this.promptBlock = this.generatePromptBlock(promptBlock);
  }

  private generatePromptBlock(
    promptBlock: PromptBlockType
  ): ClassInstantiation {
    switch (promptBlock.blockType) {
      case "JINJA":
        return this.generateJinjaPromptBlock(promptBlock);
      case "CHAT_MESSAGE":
        return this.generateChatMessagePromptBlock(promptBlock);
      case "FUNCTION_DEFINITION":
        return this.generateFunctionDefinitionPromptBlock(promptBlock);
      case "VARIABLE":
        return this.generateVariablePromptBlock(promptBlock);
      case "RICH_TEXT":
        return this.generateRichTextPromptBlock(promptBlock);
    }
  }

  private getPromptBlockRef(promptBlock: PromptBlockType): python.Reference {
    let pathName;
    switch (promptBlock.blockType) {
      case "JINJA":
        pathName = "JinjaPromptBlock";
        break;
      case "CHAT_MESSAGE":
        pathName = "ChatMessagePromptBlock";
        break;
      case "FUNCTION_DEFINITION":
        pathName = "FunctionDefinitionPromptBlock";
        break;
      case "VARIABLE":
        pathName = "VariablePromptBlock";
        break;
      case "RICH_TEXT":
        pathName = "RichTextPromptBlock";
        break;
    }
    return python.reference({
      name: pathName,
      modulePath: VELLUM_CLIENT_MODULE_PATH,
    });
  }

  private generateJinjaPromptBlock(
    promptBlock: JinjaPromptBlockType
  ): python.ClassInstantiation {
    const classArgs: MethodArgument[] = [
      ...this.constructCommonClassArguments(promptBlock),
    ];

    if (promptBlock.template) {
      classArgs.push(
        new MethodArgument({
          name: "template",
          value: python.TypeInstantiation.str(promptBlock.template),
        })
      );
    }

    const jinjaBlock = python.instantiateClass({
      classReference: this.getPromptBlockRef(promptBlock),
      arguments_: classArgs,
    });

    this.inheritReferences(jinjaBlock);
    return jinjaBlock;
  }

  private generateChatMessagePromptBlock(
    promptBlock: ChatMessagePromptBlockType
  ): python.ClassInstantiation {
    const classArgs: MethodArgument[] = [
      ...this.constructCommonClassArguments(promptBlock),
    ];

    if (promptBlock.chatRole) {
      classArgs.push(
        new MethodArgument({
          name: "chat_role",
          value: python.TypeInstantiation.str(promptBlock.chatRole),
        })
      );
    }

    classArgs.push(
      new MethodArgument({
        name: "chat_source",
        value: promptBlock.chatSource
          ? python.TypeInstantiation.str(promptBlock.chatSource)
          : python.TypeInstantiation.none(),
      })
    );

    const chatMessageUnterminatedValue =
      promptBlock.chatMessageUnterminated !== undefined &&
      promptBlock.chatMessageUnterminated !== null
        ? python.TypeInstantiation.bool(promptBlock.chatMessageUnterminated)
        : python.TypeInstantiation.none();
    classArgs.push(
      new MethodArgument({
        name: "chat_message_unterminated",
        value: chatMessageUnterminatedValue,
      })
    );

    classArgs.push(
      new MethodArgument({
        name: "blocks",
        value: python.TypeInstantiation.list(
          promptBlock.blocks.map((block) => {
            return this.generatePromptBlock(block);
          })
        ),
      })
    );

    const chatBlock = python.instantiateClass({
      classReference: this.getPromptBlockRef(promptBlock),
      arguments_: classArgs,
    });

    this.inheritReferences(chatBlock);
    return chatBlock;
  }

  private generateFunctionDefinitionPromptBlock(
    promptBlock: FunctionDefinitionPromptBlockType
  ): python.ClassInstantiation {
    const classArgs: MethodArgument[] = [
      ...this.constructCommonClassArguments(promptBlock),
    ];

    if (promptBlock.functionName) {
      classArgs.push(
        new MethodArgument({
          name: "function_name",
          value: python.TypeInstantiation.str(promptBlock.functionName),
        })
      );
    }

    if (promptBlock.functionDescription) {
      classArgs.push(
        new MethodArgument({
          name: "function_description",
          value: python.TypeInstantiation.str(promptBlock.functionDescription),
        })
      );
    }

    if (promptBlock.functionParameters) {
      classArgs.push(
        new MethodArgument({
          name: "function_parameters",
          value: python.codeBlock(
            JSON.stringify(promptBlock.functionParameters)
          ),
        })
      );
    }

    if (promptBlock.functionForced) {
      classArgs.push(
        new MethodArgument({
          name: "function_forced",
          value: python.TypeInstantiation.bool(promptBlock.functionForced),
        })
      );
    }

    if (promptBlock.functionStrict) {
      classArgs.push(
        new MethodArgument({
          name: "function_strict",
          value: python.TypeInstantiation.bool(promptBlock.functionStrict),
        })
      );
    }

    const functionBlock = python.instantiateClass({
      classReference: this.getPromptBlockRef(promptBlock),
      arguments_: classArgs,
    });

    this.inheritReferences(functionBlock);
    return functionBlock;
  }

  private generateVariablePromptBlock(
    promptBlock: VariablePromptBlockType
  ): python.ClassInstantiation {
    const classArgs: MethodArgument[] = [
      ...this.constructCommonClassArguments(promptBlock),
    ];
    classArgs.push(
      new MethodArgument({
        name: "input_variable",
        value: python.TypeInstantiation.str(promptBlock.inputVariable),
      })
    );

    const variableBlock = python.instantiateClass({
      classReference: this.getPromptBlockRef(promptBlock),
      arguments_: classArgs,
    });

    this.inheritReferences(variableBlock);
    return variableBlock;
  }

  private generatePlainTextPromptBlock(
    promptBlock: PlainTextPromptBlockType
  ): python.ClassInstantiation {
    const classArgs: MethodArgument[] = [];

    if (promptBlock.state) {
      classArgs.push(
        new MethodArgument({
          name: "state",
          value: python.TypeInstantiation.str(promptBlock.state),
        })
      );
    }

    let cacheConfigValue = python.TypeInstantiation.none();
    if (
      promptBlock.cacheConfig !== undefined &&
      promptBlock.cacheConfig !== null
    ) {
      if (promptBlock.cacheConfig.type) {
        cacheConfigValue = python.TypeInstantiation.str(
          promptBlock.cacheConfig.type
        );
      }
    }
    classArgs.push(
      new MethodArgument({
        name: "cache_config",
        value: cacheConfigValue,
      })
    );

    classArgs.push(
      new MethodArgument({
        name: "text",
        value: python.TypeInstantiation.str(promptBlock.text),
      })
    );

    const plainBlock = python.instantiateClass({
      classReference: python.reference({
        name: "PlainTextPromptBlock",
        modulePath: VELLUM_CLIENT_MODULE_PATH,
      }),
      arguments_: classArgs,
    });

    this.inheritReferences(plainBlock);
    return plainBlock;
  }

  private generateRichTextPromptBlock(
    promptBlock: RichTextPromptBlockType
  ): python.ClassInstantiation {
    const classArgs: MethodArgument[] = [
      ...this.constructCommonClassArguments(promptBlock),
    ];

    classArgs.push(
      new MethodArgument({
        name: "blocks",
        value: python.TypeInstantiation.list(
          promptBlock.blocks.map((block) => {
            if (block.blockType === "VARIABLE") {
              return this.generateVariablePromptBlock(block);
            } else {
              return this.generatePlainTextPromptBlock(block);
            }
          })
        ),
      })
    );

    const richBlock = python.instantiateClass({
      classReference: this.getPromptBlockRef(promptBlock),
      arguments_: classArgs,
    });

    this.inheritReferences(richBlock);
    return richBlock;
  }

  private constructCommonClassArguments(
    promptBlock: PromptBlockType
  ): MethodArgument[] {
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

  private extractCacheConfig(
    promptBlock: PromptBlockType
  ): python.TypeInstantiation {
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
    this.promptBlock.write(writer);
  }
}
