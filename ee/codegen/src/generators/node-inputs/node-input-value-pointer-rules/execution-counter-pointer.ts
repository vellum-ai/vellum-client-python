import { python } from "@fern-api/python-ast";

import { BaseNodeInputValuePointerRule } from "./base";

import { ExecutionCounterPointer } from "src/types/vellum";

export class ExecutionCounterPointerRule extends BaseNodeInputValuePointerRule<ExecutionCounterPointer> {
  getAstNode(): python.Reference {
    const executionCounterData = this.nodeInputValuePointerRule.data;

    const nodeContext = this.workflowContext.getNodeContext(
      executionCounterData.nodeId
    );

    return python.reference({
      name: nodeContext.nodeClassName,
      modulePath: nodeContext.nodeModulePath,
      attribute: ["Execution", "count"],
    });
  }
}
