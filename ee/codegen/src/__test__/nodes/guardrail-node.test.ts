import { Writer } from "@fern-api/python-ast/core/Writer";
import { MetricDefinitionHistoryItem } from "vellum-ai/api";
import { MetricDefinitions as MetricDefinitionsClient } from "vellum-ai/api/resources/metricDefinitions/client/Client";
import { beforeEach, vi } from "vitest";

import { workflowContextFactory } from "src/__test__/helpers";
import { inputVariableContextFactory } from "src/__test__/helpers/input-variable-context-factory";
import { guardrailNodeDataFactory } from "src/__test__/helpers/node-data-factories";
import { createNodeContext, WorkflowContext } from "src/context";
import { GuardrailNodeContext } from "src/context/node-context/guardrail-node";
import { GuardrailNode } from "src/generators/nodes/guardrail-node";

describe("GuardrailNode", () => {
  let workflowContext: WorkflowContext;
  let writer: Writer;
  let node: GuardrailNode;

  beforeEach(() => {
    workflowContext = workflowContextFactory();
    writer = new Writer();

    workflowContext.addInputVariableContext(
      inputVariableContextFactory({
        inputVariableData: {
          id: "a6ef8809-346e-469c-beed-2e5c4e9844c5",
          key: "expected",
          type: "STRING",
        },
        workflowContext,
      })
    );

    workflowContext.addInputVariableContext(
      inputVariableContextFactory({
        inputVariableData: {
          id: "abed55ada-923e-46ef-8340-1a5b0b563dc1",
          key: "actual",
          type: "STRING",
        },
        workflowContext,
      })
    );

    workflowContext.addInputVariableContext(
      inputVariableContextFactory({
        inputVariableData: {
          id: "1472503c-1662-4da9-beb9-73026be90c68",
          key: "output",
          type: "STRING",
        },
        workflowContext,
      })
    );
  });

  describe("basic", () => {
    beforeEach(async () => {
      vi.spyOn(
        MetricDefinitionsClient.prototype,
        "metricDefinitionHistoryItemRetrieve"
      ).mockResolvedValue({
        id: "mocked-metric-output-id",
        label: "mocked-metric-output-label",
        name: "mocked-metric-output-name",
        description: "mocked-metric-output-description",
        outputVariables: [
          { id: "mocked-input-id", key: "score", type: "NUMBER" },
        ],
      } as unknown as MetricDefinitionHistoryItem);
      const nodeData = guardrailNodeDataFactory();

      const nodeContext = (await createNodeContext({
        workflowContext,
        nodeData,
      })) as GuardrailNodeContext;
      workflowContext.addNodeContext(nodeContext);

      node = new GuardrailNode({
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
    beforeEach(async () => {
      const nodeData = guardrailNodeDataFactory({
        errorOutputId: "38361ff1-c826-49b8-aa8d-28179c3684cc",
      });

      const nodeContext = (await createNodeContext({
        workflowContext,
        nodeData,
      })) as GuardrailNodeContext;
      workflowContext.addNodeContext(nodeContext);

      node = new GuardrailNode({
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
