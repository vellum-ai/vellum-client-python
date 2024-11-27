import { python } from "@fern-api/python-ast";
import { AstNode } from "@fern-api/python-ast/core/AstNode";
import { Writer } from "@fern-api/python-ast/core/Writer";
import {
  ChatMessageRequest,
  VellumValue as VellumVariableValueType,
} from "vellum-ai/api";

import { ChatMessageContent } from "./chat-message-content";

import { VELLUM_CLIENT_MODULE_PATH } from "src/constants";
import { Json } from "src/generators/json";

class StringVellumValue extends AstNode {
  private value: string;

  public constructor(value: string) {
    super();
    this.value = value;
  }

  public write(writer: Writer): void {
    python.TypeInstantiation.str(this.value).write(writer);
  }
}

class NumberVellumValue extends AstNode {
  private value: number;

  public constructor(value: number) {
    super();
    this.value = value;
  }

  public write(writer: Writer): void {
    python.TypeInstantiation.float(this.value).write(writer);
  }
}

class JsonVellumValue extends AstNode {
  private astNode: Json;

  public constructor(value: unknown) {
    super();
    this.astNode = new Json(value);
    this.inheritReferences(this.astNode);
  }

  public write(writer: Writer): void {
    this.astNode.write(writer);
  }
}

class ChatHistoryVellumValue extends AstNode {
  private value: ChatMessageRequest[];
  private isRequestType: boolean;
  private contentsByIndex: Map<number, ChatMessageContent>;

  public constructor({
    value,
    isRequestType = true,
  }: {
    value: ChatMessageRequest[];
    isRequestType?: boolean;
  }) {
    super();
    this.value = value;
    this.isRequestType = isRequestType;
    this.contentsByIndex = new Map();

    this.setContentsByIndex();
  }

  private setContentsByIndex(): void {
    this.value.forEach((chatMessage, index) => {
      if (chatMessage.content !== undefined) {
        const content = new ChatMessageContent({
          chatMessageContent: chatMessage.content,
          isRequestType: this.isRequestType,
        });

        this.inheritReferences(content);

        this.contentsByIndex.set(index, content);
      }
    });
  }

  public write(writer: Writer): void {
    const chatHistoryValue = this.value;

    const chatMessages = chatHistoryValue.map((chatMessage, index) => {
      const arguments_ = [
        python.methodArgument({
          name: "role",
          value: python.TypeInstantiation.str(chatMessage.role),
        }),
      ];

      if (chatMessage.text !== undefined) {
        arguments_.push(
          python.methodArgument({
            name: "text",
            value: python.TypeInstantiation.str(chatMessage.text),
          })
        );
      }

      if (chatMessage.source !== undefined) {
        arguments_.push(
          python.methodArgument({
            name: "source",
            value: python.TypeInstantiation.str(chatMessage.source),
          })
        );
      }

      if (chatMessage.content !== undefined) {
        const content = this.contentsByIndex.get(index);
        if (content === undefined) {
          throw new Error("Content not found");
        }

        arguments_.push(
          python.methodArgument({
            name: "content",
            value: content,
          })
        );
      }

      return python.instantiateClass({
        classReference: python.reference({
          name: "ChatMessage" + (this.isRequestType ? "Request" : ""),
          modulePath: VELLUM_CLIENT_MODULE_PATH,
        }),
        arguments_: arguments_,
      });
    });

    python.TypeInstantiation.list(chatMessages).write(writer);
  }
}
export namespace VellumValue {
  export type Args = {
    vellumValue: VellumVariableValueType;
    isRequestType?: boolean;
  };
}

export class VellumValue extends AstNode {
  private astNode: AstNode | null;

  public constructor({ vellumValue, isRequestType }: VellumValue.Args) {
    super();
    this.astNode = null;

    if (vellumValue.value === undefined) {
      return;
    }

    switch (vellumValue.type) {
      case "STRING":
        this.astNode = new StringVellumValue(vellumValue.value);
        break;
      case "NUMBER":
        this.astNode = new NumberVellumValue(vellumValue.value);
        break;
      case "JSON":
        this.astNode = new JsonVellumValue(vellumValue.value);
        break;
      case "CHAT_HISTORY":
        this.astNode = new ChatHistoryVellumValue({
          value: vellumValue.value,
          isRequestType,
        });
        break;
      default:
        throw new Error(`Unknown vellum value type: ${vellumValue.type}`);
    }

    this.inheritReferences(this.astNode);
  }

  public write(writer: Writer): void {
    if (this.astNode === null) {
      writer.write("None");
      return;
    }

    this.astNode.write(writer);
  }
}
