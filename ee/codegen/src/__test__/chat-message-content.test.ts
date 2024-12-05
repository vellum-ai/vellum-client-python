import { Writer } from "@fern-api/python-ast/core/Writer";

import { ChatMessageContent } from "src/generators/chat-message-content";

describe("ChatMessageContent", () => {
  let writer: Writer;

  beforeEach(() => {
    writer = new Writer();
  });

  describe("STRING", () => {
    it("should write a string content correctly", async () => {
      const chatMessageContent = new ChatMessageContent({
        chatMessageContent: { type: "STRING", value: "Hello, AI!" },
      });
      chatMessageContent.write(writer);
      expect(await writer.toString()).toMatchSnapshot();
    });
  });

  describe("FUNCTION_CALL", () => {
    it("should write a function call content with id correctly", async () => {
      const chatMessageContent = new ChatMessageContent({
        chatMessageContent: {
          type: "FUNCTION_CALL",
          value: {
            id: "123",
            name: "get_weather",
            arguments: {
              location: "New York",
              unit: "celsius",
            },
          },
        },
      });
      chatMessageContent.write(writer);
      expect(await writer.toStringFormatted()).toMatchSnapshot();
    });

    it("should write a function call content without id correctly", async () => {
      const chatMessageContent = new ChatMessageContent({
        chatMessageContent: {
          type: "FUNCTION_CALL",
          value: {
            name: "get_weather",
            arguments: {
              location: "New York",
              unit: "celsius",
            },
          },
        },
      });
      chatMessageContent.write(writer);
      expect(await writer.toStringFormatted()).toMatchSnapshot();
    });
  });
  describe("ARRAY", () => {
    it("should write an array of content correctly", async () => {
      const chatMessageContent = new ChatMessageContent({
        chatMessageContent: {
          type: "ARRAY",
          value: [
            {
              type: "STRING",
              value: "First message",
            },
            {
              type: "FUNCTION_CALL",
              value: {
                name: "get_weather",
                arguments: {
                  location: "Seattle",
                },
              },
            },
          ],
        },
      });
      chatMessageContent.write(writer);
      expect(await writer.toStringFormatted()).toMatchSnapshot();
      expect(chatMessageContent.getReferences()).toHaveLength(1);
    });
  });
});
