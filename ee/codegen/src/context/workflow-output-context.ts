import {
  NodeInput as NodeInputType,
  FinalOutputNode as FinalOutputNodeType,
} from "src/types/vellum";
import { toSnakeCase } from "src/utils/casing";

export declare namespace WorkflowOutputContext {
  export type Args = {
    terminalNodeData: FinalOutputNodeType;
  };
}

export class WorkflowOutputContext {
  private readonly terminalNodeData: FinalOutputNodeType;

  constructor({ terminalNodeData }: WorkflowOutputContext.Args) {
    this.terminalNodeData = terminalNodeData;
  }

  public getFinalOutputNodeId(): string {
    return this.terminalNodeData.id;
  }

  public getFinalOutputNodeData(): FinalOutputNodeType {
    return this.terminalNodeData;
  }

  public getOutputName(): string {
    return toSnakeCase(this.terminalNodeData.data.name);
  }

  public getFinalOutputNodeInputData(): NodeInputType {
    const nodeInputData = this.terminalNodeData.inputs.find(
      (input) => input.id === this.terminalNodeData.data.nodeInputId
    );

    if (!nodeInputData) {
      throw new Error(
        `Node input data not found for node input ID: ${this.terminalNodeData.data.nodeInputId}`
      );
    }

    return nodeInputData;
  }
}
