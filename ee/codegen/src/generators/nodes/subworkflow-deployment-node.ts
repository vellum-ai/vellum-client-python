import { python } from "@fern-api/python-ast";
import { AstNode } from "@fern-api/python-ast/core/AstNode";

import { SubworkflowDeploymentNodeContext } from "src/context/node-context/subworkflow-deployment-node";
import { BaseSingleFileNode } from "src/generators/nodes/bases/single-file-base";
import { SubworkflowNode as SubworkflowNodeType } from "src/types/vellum";

export class SubworkflowDeploymentNode extends BaseSingleFileNode<
  SubworkflowNodeType,
  SubworkflowDeploymentNodeContext
> {
  baseNodeClassName = "SubworkflowDeploymentNode";
  baseNodeDisplayClassName = "BaseSubworkflowDeploymentNodeDisplay";

  getNodeClassBodyStatements(): AstNode[] {
    const statements: AstNode[] = [];

    if (this.nodeData.data.variant !== "DEPLOYMENT") {
      throw new Error(
        `SubworkflowDeploymentNode only supports DEPLOYMENT variant. Received ${this.nodeData.data.variant}`
      );
    }

    statements.push(
      python.field({
        name: "deployment",
        initializer: python.TypeInstantiation.str(
          this.nodeData.data.workflowDeploymentId
        ),
      })
    );

    statements.push(
      python.field({
        name: "release_tag",
        initializer: python.TypeInstantiation.str(
          this.nodeData.data.releaseTag
        ),
      })
    );

    statements.push(
      python.field({
        name: "subworkflow_inputs",
        initializer: python.TypeInstantiation.dict(
          Array.from(this.nodeInputsByKey.entries()).map(([key, value]) => ({
            key: python.TypeInstantiation.str(key),
            value: value,
          }))
        ),
      })
    );

    return statements;
  }

  getNodeDisplayClassBodyStatements(): AstNode[] {
    const statements: AstNode[] = [];

    statements.push(
      python.field({
        name: "label",
        initializer: python.TypeInstantiation.str(this.nodeData.data.label),
      })
    );

    statements.push(
      python.field({
        name: "node_id",
        initializer: python.TypeInstantiation.uuid(this.nodeData.id),
      })
    );

    statements.push(
      python.field({
        name: "target_handle_id",
        initializer: python.TypeInstantiation.uuid(
          this.nodeData.data.targetHandleId
        ),
      })
    );

    // TODO: Add stable id references for inputs and outputs
    // https://app.shortcut.com/vellum/story/5639

    return statements;
  }

  protected getErrorOutputId(): string | undefined {
    return this.nodeData.data.errorOutputId;
  }
}
