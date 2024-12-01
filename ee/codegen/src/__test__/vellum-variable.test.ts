import { Writer } from "@fern-api/python-ast/core/Writer";

import { workflowContextFactory } from "src/__test__/helpers";
import * as codegen from "src/codegen";
import { WorkflowContext } from "src/context";

describe("VellumVariableField", () => {
  let writer: Writer;
  let workflowContext: WorkflowContext;

  beforeEach(() => {
    writer = new Writer();
    workflowContext = workflowContextFactory();
  });

  test("StringVellumVariable snapshot", async () => {
    const stringVar = codegen.vellumVariable({
      variable: { id: "1", name: "test", type: "STRING" },
      workflowContext,
    });
    stringVar.write(writer);
    expect(await writer.toStringFormatted()).toMatchSnapshot();
  });

  test("NumberVellumVariable snapshot", async () => {
    const numberVar = codegen.vellumVariable({
      variable: { id: "1", name: "test", type: "NUMBER" },
      workflowContext,
    });
    numberVar.write(writer);
    expect(await writer.toStringFormatted()).toMatchSnapshot();
  });

  test("JsonVellumVariable snapshot", async () => {
    const jsonVar = codegen.vellumVariable({
      variable: { id: "1", name: "test", type: "JSON" },
      workflowContext,
    });
    jsonVar.write(writer);
    expect(await writer.toStringFormatted()).toMatchSnapshot();
  });

  test("ImageVellumVariable snapshot", async () => {
    const imageVar = codegen.vellumVariable({
      variable: { id: "1", name: "test", type: "IMAGE" },
      workflowContext,
    });
    imageVar.write(writer);
    expect(await writer.toStringFormatted()).toMatchSnapshot();
  });

  test("FunctionCallVellumVariable snapshot", async () => {
    const functionCallVar = codegen.vellumVariable({
      variable: { id: "1", name: "test", type: "FUNCTION_CALL" },
      workflowContext,
    });
    functionCallVar.write(writer);
    expect(await writer.toStringFormatted()).toMatchSnapshot();
  });

  test("ErrorVellumVariable snapshot", async () => {
    const errorVar = codegen.vellumVariable({
      variable: { id: "1", name: "test", type: "ERROR" },
      workflowContext,
    });
    errorVar.write(writer);
    expect(await writer.toStringFormatted()).toMatchSnapshot();
  });

  test("ArrayVellumVariable snapshot", async () => {
    const arrayVar = codegen.vellumVariable({
      variable: { id: "1", name: "test", type: "ARRAY" },
      workflowContext,
    });
    arrayVar.write(writer);
    expect(await writer.toStringFormatted()).toMatchSnapshot();
  });

  test("ChatHistoryVellumVariable snapshot", async () => {
    const chatHistoryVar = codegen.vellumVariable({
      variable: { id: "1", name: "test", type: "CHAT_HISTORY" },
      workflowContext,
    });
    chatHistoryVar.write(writer);
    expect(await writer.toStringFormatted()).toMatchSnapshot();
  });

  test("SearchResultsVellumVariable snapshot", async () => {
    const searchResultsVar = codegen.vellumVariable({
      variable: { id: "1", name: "test", type: "SEARCH_RESULTS" },
      workflowContext,
    });
    searchResultsVar.write(writer);
    expect(await writer.toStringFormatted()).toMatchSnapshot();
  });

  test("NullVellumVariable snapshot", async () => {
    const nullVar = codegen.vellumVariable({
      variable: { id: "1", name: "test", type: "NULL" },
      workflowContext,
    });
    nullVar.write(writer);
    expect(await writer.toStringFormatted()).toMatchSnapshot();
  });
});
