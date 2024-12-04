import { Writer } from "@fern-api/python-ast/core/Writer";

import * as codegen from "src/codegen";

describe("VellumValue", () => {
  let writer: Writer;

  beforeEach(() => {
    writer = new Writer();
  });

  describe("STRING", () => {
    it("should write a STRING value correctly", async () => {
      const stringValue = codegen.vellumValue({
        vellumValue: {
          type: "STRING",
          value: "Hello, World!",
        },
      });
      stringValue.write(writer);
      expect(await writer.toStringFormatted()).toMatchSnapshot();
    });
  });

  describe("NUMBER", () => {
    it("should write a NUMBER value correctly", async () => {
      const numberValue = codegen.vellumValue({
        vellumValue: {
          type: "NUMBER",
          value: 42,
        },
      });
      numberValue.write(writer);
      expect(await writer.toStringFormatted()).toMatchSnapshot();
    });
  });

  describe("CHAT_HISTORY", () => {
    it("should write a CHAT_HISTORY value with just text", async () => {
      const chatHistoryValue = codegen.vellumValue({
        vellumValue: {
          type: "CHAT_HISTORY",
          value: [
            {
              role: "USER",
              text: "Hello, AI!",
            },
          ],
        },
      });
      chatHistoryValue.write(writer);
      expect(await writer.toString()).toMatchSnapshot();
    });

    it("should write a CHAT_HISTORY value with a string content", async () => {
      const chatHistoryValue = codegen.vellumValue({
        vellumValue: {
          type: "CHAT_HISTORY",
          value: [
            {
              role: "USER",
              content: { type: "STRING", value: "Hello, AI!" },
            },
          ],
        },
      });
      chatHistoryValue.write(writer);
      expect(await writer.toString()).toMatchSnapshot();
    });
  });

  describe.skip("SEARCH_RESULTS", () => {
    it("should write a SEARCH_RESULTS value correctly", async () => {
      const searchResultsValue = codegen.vellumValue({
        vellumValue: {
          type: "SEARCH_RESULTS",
          value: [],
        },
      });
      searchResultsValue.write(writer);
      expect(await writer.toStringFormatted()).toMatchSnapshot();
    });
  });

  describe("JSON", () => {
    it("should write a JSON value correctly", async () => {
      const jsonValue = codegen.vellumValue({
        vellumValue: {
          type: "JSON",
          value: {
            key: "value",
            nested: { array: [1, 2, 3] },
          },
        },
      });
      jsonValue.write(writer);
      expect(await writer.toStringFormatted()).toMatchSnapshot();
    });
  });

  describe("ERROR", () => {
    it("should write a ERROR value correctly", async () => {
      const errorValue = codegen.vellumValue({
        vellumValue: {
          type: "ERROR",
          value: {
            message: "This is an error!",
            code: "INTERNAL_SERVER_ERROR",
          },
        },
      });
      errorValue.write(writer);
      expect(await writer.toStringFormatted()).toMatchSnapshot();
    });
  });

  describe("IMAGE", () => {
    it("should write a IMAGE value correctly", async () => {
      const imageValue = codegen.vellumValue({
        vellumValue: {
          type: "IMAGE",
          value: {
            src: "https://example.com/image.png",
          },
        },
      });
      imageValue.write(writer);
      expect(await writer.toStringFormatted()).toMatchSnapshot();
    });
  });

  describe("AUDIO", () => {
    it("should write a AUDIO value correctly", async () => {
      const audioValue = codegen.vellumValue({
        vellumValue: {
          type: "AUDIO",
          value: {
            src: "https://example.com/audio.mp3",
          },
        },
      });
      audioValue.write(writer);
      expect(await writer.toStringFormatted()).toMatchSnapshot();
    });
  });

  describe("SEARCH_RESULTS", () => {
    it("should write a SEARCH_RESULTS value correctly", async () => {
      const searchResultsValue = codegen.vellumValue({
        vellumValue: {
          type: "SEARCH_RESULTS",
          value: [
            {
              text: "Hello, World!",
              score: 0.5,
              keywords: ["hello", "world"],
              document: {
                id: "123",
                label: "Example Document",
              },
            },
            {
              text: "Hello, AI!",
              score: 0.7,
              keywords: ["hello", "ai"],
              document: {
                id: "456",
                label: "Another Document",
              },
            },
          ],
        },
      });
      searchResultsValue.write(writer);
      expect(await writer.toStringFormatted()).toMatchSnapshot();
    });
  });
});
