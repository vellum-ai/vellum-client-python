import { python } from "@fern-api/python-ast";

import { BaseNodeInputValuePointerRule } from "./base";

import { WorkspaceSecretPointer as WorkspaceSecretPointerType } from "src/types/vellum";

export class WorkspaceSecretPointerRule extends BaseNodeInputValuePointerRule<WorkspaceSecretPointerType> {
  getAstNode(): python.AstNode {
    const workspaceSecretPointerData = this.nodeInputValuePointerRule.data;

    const workspaceSecretName = workspaceSecretPointerData.workspaceSecretId;

    if (!workspaceSecretName) {
      throw new Error("Workspace secret name is required");
    }

    return python.instantiateClass({
      classReference: python.reference({
        name: "VellumSecretReference",
        modulePath: [
          ...this.workflowContext.sdkModulePathNames.WORKFLOWS_MODULE_PATH,
          "references",
        ],
      }),
      arguments_: [
        python.methodArgument({
          value: python.TypeInstantiation.str(workspaceSecretName),
        }),
      ],
    });
  }
}
