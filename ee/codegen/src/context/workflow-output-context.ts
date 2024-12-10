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
    const name = this.generateUniqueFinalOutputName();
    return toSnakeCase(name);
  }

  private generateUniqueFinalOutputName(): string {
    const value = this.workflowContext.getOutputName(this.terminalNodeData.id);
    if (value !== undefined) {
      return value;
    } else {
      let counter = 1;
      const names = new Set(this.workflowContext.outputNamesById.values());

      const originalName = this.terminalNodeData.data.name;
      let uniqueName = originalName;

      while (names.has(uniqueName)) {
        uniqueName = `${originalName}-${counter}`;
        counter++;
      }
      this.workflowContext.addOutputName(this.terminalNodeData.id, uniqueName);
      return uniqueName;
    }
  }
}
