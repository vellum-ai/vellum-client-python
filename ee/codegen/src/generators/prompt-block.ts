import { python } from "@fern-api/python-ast";
import { ClassInstantiation } from "@fern-api/python-ast/ClassInstantiation";
import { MethodArgument } from "@fern-api/python-ast/MethodArgument";
import {
  PromptBlock as PromptBlockType,
  JinjaPromptBlock as JinjaPromptBlockType,
  ChatMessagePromptBlock as ChatMessagePromptBlockType,
  VariablePromptBlock as VariablePromptBlockType,
  RichTextPromptBlock as RichTextPromptBlockType,
  PlainTextPromptBlock as PlainTextPromptBlockType,
} from "vellum-ai/api";

import { VELLUM_CLIENT_MODULE_PATH } from "src/constants";
import { BasePromptBlock } from "src/generators/base-prompt-block";

// Flesh out unit tests for various prompt configurations
// https://app.shortcut.com/vellum/story/5249
export class PromptBlock extends BasePromptBlock<PromptBlockType> {
  protected generateAstNode(promptBlock: PromptBlockType): ClassInstantiation {
    switch (promptBlock.blockType) {
      case "JINJA":
        return this.generateJinjaPromptBlock(promptBlock);
      case "CHAT_MESSAGE":
        return this.generateChatMessagePromptBlock(promptBlock);
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
            return this.generateAstNode(block);
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
}
