import { workflowContextFactory } from "src/__test__/helpers";
import { templatingNodeFactory } from "src/__test__/helpers/node-data-factories";
import { createNodeContext } from "src/context";
import { TemplatingNodeContext } from "src/context/node-context/templating-node";
import { NodeAttributeGenerationError } from "src/generators/errors";
import { TemplatingNode } from "src/generators/nodes/templating-node";

describe("BaseNode", () => {
  describe("failures", () => {
    it("should throw the expected error when a input references an invalid node", async () => {
      const workflowContext = workflowContextFactory();

      const templatingNodeData = templatingNodeFactory({
        inputRules: [
          {
            type: "NODE_OUTPUT",
            data: {
              nodeId: "12345678-1234-5678-1234-567812345678",
              outputId: "90abcdef-90ab-cdef-90ab-cdef90abcdef",
            },
          },
        ],
      });
      const templatingNodeContext = (await createNodeContext({
        workflowContext,
        nodeData: templatingNodeData,
      })) as TemplatingNodeContext;
      workflowContext.addNodeContext(templatingNodeContext);

      expect(() => {
        new TemplatingNode({
          workflowContext,
          nodeContext: templatingNodeContext,
        });
      }).toThrow(
        new NodeAttributeGenerationError(
          "Failed to generate attribute 'TemplatingNode.inputs.text': Failed to find node with id '12345678-1234-5678-1234-567812345678'"
        )
      );
    });
  });
});
