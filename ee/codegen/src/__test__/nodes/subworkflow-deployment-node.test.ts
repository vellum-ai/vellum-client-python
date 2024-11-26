import { Writer } from "@fern-api/python-ast/core/Writer";
import { beforeEach } from "vitest";

import { workflowContextFactory } from "src/__test__/helpers";
import { subworkflowDeploymentNodeDataFactory } from "src/__test__/helpers/node-data-factories";
import { createNodeContext, WorkflowContext } from "src/context";
import { SubworkflowDeploymentNodeContext } from "src/context/node-context/subworkflow-deployment-node";
import { SubworkflowDeploymentNode } from "src/generators/nodes/subworkflow-deployment-node";

describe("SubworkflowDeploymentNode", () => {
  let workflowContext: WorkflowContext;
  let node: SubworkflowDeploymentNode;
  let writer: Writer;

  beforeEach(() => {
    workflowContext = workflowContextFactory();
    writer = new Writer();
  });

  describe("basic", () => {
    beforeEach(() => {
      const nodeData = subworkflowDeploymentNodeDataFactory();

      const nodeContext = createNodeContext({
        workflowContext,
        nodeData,
      }) as SubworkflowDeploymentNodeContext;
      workflowContext.addNodeContext(nodeContext);

      node = new SubworkflowDeploymentNode({
        workflowContext,
        nodeContext,
      });
    });

    it(`getNodeFile`, async () => {
      node.getNodeFile().write(writer);
      expect(await writer.toStringFormatted()).toMatchSnapshot();
    });

    it(`getNodeDisplayFile`, async () => {
      node.getNodeDisplayFile().write(writer);
      expect(await writer.toStringFormatted()).toMatchSnapshot();
    });
  });
});
