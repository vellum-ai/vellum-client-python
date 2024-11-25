import { Writer } from "@fern-api/python-ast/core/Writer";
import { beforeEach } from "vitest";

import { workflowContextFactory } from "src/__test__/helpers";
import { inputVariableContextFactory } from "src/__test__/helpers/input-variable-context-factory";
import { searchNodeDataFactory } from "src/__test__/helpers/node-data-factories";
import { createNodeContext, WorkflowContext } from "src/context";
import { TextSearchNodeContext } from "src/context/node-context/text-search-node";
import { SearchNode } from "src/generators/nodes/search-node";

describe("TextSearchNode", () => {
  let workflowContext: WorkflowContext;
  let writer: Writer;
  let node: SearchNode;

  beforeEach(() => {
    workflowContext = workflowContextFactory();
    writer = new Writer();

    workflowContext.addInputVariableContext(
      inputVariableContextFactory({
        inputVariableData: {
          id: "a6ef8809-346e-469c-beed-2e5c4e9844c5",
          key: "query",
          type: "STRING",
        },
        workflowContext,
      })
    );
  });

  describe("basic", () => {
    beforeEach(() => {
      const nodeData = searchNodeDataFactory();

      const nodeContext = createNodeContext({
        workflowContext,
        nodeData,
      }) as TextSearchNodeContext;
      workflowContext.addNodeContext(nodeContext);

      node = new SearchNode({
        workflowContext: workflowContext,
        nodeContext,
      });
    });

    it("getNodeFile", async () => {
      node.getNodeFile().write(writer);
      expect(await writer.toStringFormatted()).toMatchSnapshot();
    });

    it("getNodeDisplayFile", async () => {
      node.getNodeDisplayFile().write(writer);
      expect(await writer.toStringFormatted()).toMatchSnapshot();
    });
  });

  describe("reject on error enabled", () => {
    beforeEach(() => {
      const nodeData = searchNodeDataFactory({
        errorOutputId: "af589f73-effe-4a80-b48f-fb912ac6ce67",
      });

      const nodeContext = createNodeContext({
        workflowContext,
        nodeData,
      }) as TextSearchNodeContext;
      workflowContext.addNodeContext(nodeContext);

      node = new SearchNode({
        workflowContext: workflowContext,
        nodeContext,
      });
    });

    it("getNodeFile", async () => {
      node.getNodeFile().write(writer);
      expect(await writer.toStringFormatted()).toMatchSnapshot();
    });

    it("getNodeDisplayFile", async () => {
      node.getNodeDisplayFile().write(writer);
      expect(await writer.toStringFormatted()).toMatchSnapshot();
    });
  });
});
