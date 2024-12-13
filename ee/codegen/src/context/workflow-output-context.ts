import { isEmpty, isNil } from "lodash";

import { WorkflowContext } from "src/context/workflow-context";
import { FinalOutputNode as FinalOutputNodeType } from "src/types/vellum";
import { toPythonSafeSnakeCase } from "src/utils/casing";

export declare namespace WorkflowOutputContext {
  export type Args = {
    workflowContext: WorkflowContext;
    terminalNodeData: FinalOutputNodeType;
  };
}

export class WorkflowOutputContext {
  private readonly workflowContext: WorkflowContext;
  private readonly terminalNodeData: FinalOutputNodeType;
  public readonly name: string;

  constructor({
    terminalNodeData,
    workflowContext,
  }: WorkflowOutputContext.Args) {
    this.workflowContext = workflowContext;
    this.terminalNodeData = terminalNodeData;
    this.name = this.generateSanitizedOutputVariableName();
  }

  public getFinalOutputNodeId(): string {
    return this.terminalNodeData.id;
  }

  public getFinalOutputNodeData(): FinalOutputNodeType {
    return this.terminalNodeData;
  }

  private generateSanitizedOutputVariableName(): string {
    const defaultName = "output_";
    const rawOutputVariableName = this.terminalNodeData.data.name;

    const initialOutputVariableName =
      !isNil(rawOutputVariableName) && !isEmpty(rawOutputVariableName)
        ? toPythonSafeSnakeCase(rawOutputVariableName, "output")
        : defaultName;

    // Deduplicate the output variable name if it's already in use
    let sanitizedName = initialOutputVariableName;
    let numRenameAttempts = 0;
    while (this.workflowContext.isOutputVariableNameUsed(sanitizedName)) {
      sanitizedName = `${initialOutputVariableName}${
        initialOutputVariableName.endsWith("_") ? "" : "_"
      }${numRenameAttempts + 1}`;
      numRenameAttempts += 1;
    }

    return sanitizedName;
  }
}
