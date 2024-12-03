import { Writer } from "@fern-api/python-ast/core/Writer";

import { workflowContextFactory } from "./helpers";
import { inputVariableContextFactory } from "./helpers/input-variable-context-factory";
import {
  entrypointNodeDataFactory,
  searchNodeDataFactory,
  terminalNodeDataFactory,
} from "./helpers/node-data-factories";

import { workflowOutputContextFactory } from "src/__test__/helpers/workflow-output-context-factory";
import * as codegen from "src/codegen";
import { createNodeContext, WorkflowContext } from "src/context";
import { WorkflowEdge } from "src/types/vellum";

describe("Workflow", () => {
  let workflowContext: WorkflowContext;
  let writer: Writer;
  const moduleName = "test";
  const entrypointNode = entrypointNodeDataFactory();

  beforeEach(async () => {
    workflowContext = workflowContextFactory({
      workflowClassName: "TestWorkflow",
    });
    workflowContext.addEntrypointNode(entrypointNode);

    const nodeData = terminalNodeDataFactory();
    workflowContext.addNodeContext(
      await createNodeContext({
        workflowContext: workflowContext,
        nodeData,
      })
    );

    writer = new Writer();
  });

  describe("write", () => {
    it("should generate correct code when there are input variables", async () => {
      const inputs = codegen.inputs({ workflowContext });
      const workflow = codegen.workflow({
        moduleName,
        workflowContext,
        inputs,
        nodes: [],
      });

      workflow.getWorkflowFile().write(writer);
      expect(await writer.toStringFormatted()).toMatchSnapshot();
    });

    it("should generate correct code when there are no input variables", async () => {
      const inputs = codegen.inputs({ workflowContext });
      const workflow = codegen.workflow({
        moduleName,
        workflowContext,
        inputs,
        nodes: [],
      });

      workflow.getWorkflowFile().write(writer);
      expect(await writer.toStringFormatted()).toMatchSnapshot();
    });

    it("should generate correct code with Search Results as an output variable", async () => {
      workflowContext.addInputVariableContext(
        inputVariableContextFactory({
          inputVariableData: {
            id: "input-variable-id",
            key: "query",
            type: "STRING",
          },
          workflowContext,
        })
      );

      const inputs = codegen.inputs({ workflowContext });

      workflowContext.addWorkflowOutputContext(workflowOutputContextFactory());

      const workflow = codegen.workflow({
        moduleName,
        workflowContext,
        inputs,
        nodes: [],
      });

      workflow.getWorkflowFile().write(writer);
      expect(await writer.toStringFormatted()).toMatchSnapshot();
    });

    it("should handle edges pointing to non-existent nodes", async () => {
      workflowContext.addInputVariableContext(
        inputVariableContextFactory({
          inputVariableData: {
            id: "input-variable-id",
            key: "query",
            type: "STRING",
          },
          workflowContext,
        })
      );

      const inputs = codegen.inputs({ workflowContext });

      const searchNodeData = searchNodeDataFactory();
      const searchNodeContext = await createNodeContext({
        workflowContext: workflowContext,
        nodeData: searchNodeData,
      });
      workflowContext.addNodeContext(searchNodeContext);

      const edges: WorkflowEdge[] = [
        {
          id: "edge-1",
          type: "DEFAULT",
          sourceNodeId: entrypointNode.id,
          sourceHandleId: entrypointNode.data.sourceHandleId,
          targetNodeId: searchNodeData.id,
          targetHandleId: searchNodeData.data.sourceHandleId,
        },
        {
          id: "edge-2",
          type: "DEFAULT",
          sourceNodeId: searchNodeData.id,
          sourceHandleId: "some-handle",
          targetNodeId: "non-existent-node-id",
          targetHandleId: "some-target-handle",
        },
      ];

      workflowContext.addWorkflowEdges(edges);

      const workflow = codegen.workflow({
        moduleName,
        workflowContext,
        inputs,
        nodes: [searchNodeData],
      });

      workflow.getWorkflowFile().write(writer);
      expect(await writer.toStringFormatted()).toMatchSnapshot();
    });

    describe("graph", () => {
      it("should be correct for a basic single node case", async () => {
        workflowContext.addInputVariableContext(
          inputVariableContextFactory({
            inputVariableData: {
              id: "input-variable-id",
              key: "query",
              type: "STRING",
            },
            workflowContext,
          })
        );

        const inputs = codegen.inputs({ workflowContext });

        workflowContext.addWorkflowOutputContext(
          workflowOutputContextFactory()
        );

        const searchNodeData = searchNodeDataFactory();
        const searchNodeContext = await createNodeContext({
          workflowContext: workflowContext,
          nodeData: searchNodeData,
        });
        workflowContext.addNodeContext(searchNodeContext);

        const edges: WorkflowEdge[] = [
          {
            id: "edge-1",
            type: "DEFAULT",
            sourceNodeId: entrypointNode.id,
            sourceHandleId: entrypointNode.data.sourceHandleId,
            targetNodeId: searchNodeData.id,
            targetHandleId: searchNodeData.data.sourceHandleId,
          },
        ];
        workflowContext.addWorkflowEdges(edges);

        const workflow = codegen.workflow({
          moduleName,
          workflowContext,
          inputs,
          nodes: [searchNodeData],
        });

        workflow.getWorkflowFile().write(writer);
        expect(await writer.toStringFormatted()).toMatchSnapshot();
      });
    });
  });
});
