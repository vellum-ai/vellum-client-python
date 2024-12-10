import { WorkflowContext } from "src/context/workflow-context";
import { FinalOutputNode as FinalOutputNodeType } from "src/types/vellum";
import { toSnakeCase } from "src/utils/casing";

export declare namespace WorkflowOutputContext {
  export type Args = {
    terminalNodeData: FinalOutputNodeType;
    workflowContext: WorkflowContext;
  };
}

export class WorkflowOutputContext {
  private readonly terminalNodeData: FinalOutputNodeType;
  private readonly workflowContext: WorkflowContext;

  constructor({
    terminalNodeData,
    workflowContext,
  }: WorkflowOutputContext.Args) {
    this.terminalNodeData = terminalNodeData;
    this.workflowContext = workflowContext;
  }

  public getFinalOutputNodeId(): string {
    return this.terminalNodeData.id;
  }

  public getFinalOutputNodeData(): FinalOutputNodeType {
    return this.terminalNodeData;
  }

  public getOutputName(): string {
    const name = this.workflowContext.getOutputName(this.terminalNodeData.id);
    if (!name) {
      throw new Error(
        `No final output name found for output names in workflow context given id ${this.terminalNodeData.id}`
      );
    }
    return toSnakeCase(name);
  }
}
