import { python } from "@fern-api/python-ast";
import { AstNode } from "@fern-api/python-ast/core/AstNode";
import { Writer } from "@fern-api/python-ast/core/Writer";

import { WorkflowContext } from "src/context";
import { NodeDisplayData as NodeDisplayDataType } from "src/types/vellum";

export namespace NodeDisplayData {
  export interface Args {
    workflowContext: WorkflowContext;
    nodeDisplayData: NodeDisplayDataType | undefined;
  }
}

export class NodeDisplayData extends AstNode {
  private readonly sourceNodeDisplayData: NodeDisplayDataType | undefined;
  private readonly nodeDisplayData: AstNode;
  private readonly workflowContext: WorkflowContext;

  public constructor({
    nodeDisplayData,
    workflowContext,
  }: NodeDisplayData.Args) {
    super();
    this.sourceNodeDisplayData = nodeDisplayData;
    this.workflowContext = workflowContext;
    this.nodeDisplayData = this.generateNodeDisplayData();
  }

  private generateNodeDisplayData(): python.ClassInstantiation {
    const clazz = python.instantiateClass({
      classReference: python.reference({
        name: "NodeDisplayData",
        modulePath:
          this.workflowContext.sdkModulePathNames.VELLUM_TYPES_MODULE_PATH,
      }),
      arguments_: [
        python.methodArgument({
          name: "position",
          value: python.instantiateClass({
            classReference: python.reference({
              name: "NodeDisplayPosition",
              modulePath:
                this.workflowContext.sdkModulePathNames
                  .VELLUM_TYPES_MODULE_PATH,
            }),
            arguments_: [
              python.methodArgument({
                name: "x",
                value: python.TypeInstantiation.float(
                  this.sourceNodeDisplayData?.position?.x ?? 0
                ),
              }),
              python.methodArgument({
                name: "y",
                value: python.TypeInstantiation.float(
                  this.sourceNodeDisplayData?.position?.y ?? 0
                ),
              }),
            ],
          }),
        }),
        python.methodArgument({
          name: "width",
          value: this.sourceNodeDisplayData?.width
            ? python.TypeInstantiation.int(this.sourceNodeDisplayData.width)
            : python.TypeInstantiation.none(),
        }),
        python.methodArgument({
          name: "height",
          value: this.sourceNodeDisplayData?.height
            ? python.TypeInstantiation.int(this.sourceNodeDisplayData?.height)
            : python.TypeInstantiation.none(),
        }),
      ],
    });
    this.inheritReferences(clazz);
    return clazz;
  }

  public write(writer: Writer) {
    this.nodeDisplayData.write(writer);
  }
}