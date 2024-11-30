import { python } from "@fern-api/python-ast";
import { AstNode } from "@fern-api/python-ast/core/AstNode";

import { OUTPUTS_CLASS_NAME } from "src/constants";
import { MapNodeContext } from "src/context/node-context/map-node";
import { BaseNestedWorkflowNode } from "src/generators/nodes/bases/nested-workflow-base";
import { WorkflowProjectGenerator } from "src/project";
import {
  InlineMapNodeData,
  MapNode as MapNodeType,
  WorkflowRawData,
} from "src/types/vellum";

export class MapNode extends BaseNestedWorkflowNode<
  MapNodeType,
  MapNodeContext
> {
  baseNodeClassName = "MapNode";
  baseNodeDisplayClassName = "BaseMapNodeDisplay";

  getInnerWorkflowData(): WorkflowRawData {
    if (this.nodeData.data.variant !== "INLINE") {
      throw new Error(
        `MapNode only supports INLINE variant. Received: ${this.nodeData.data.variant}`
      );
    }

    return this.nodeData.data.workflowRawData;
  }

  getNodeClassBodyStatements(): AstNode[] {
    const nestedWorkflowContext = this.getNestedWorkflowContextByName(
      BaseNestedWorkflowNode.subworkflowNestedProjectName
    );

    const nestedWorkflowReference = python.reference({
      name: nestedWorkflowContext.workflowClassName,
      modulePath: nestedWorkflowContext.modulePath,
    });

    const subworkflowField = python.field({
      name: "subworkflow",
      initializer: nestedWorkflowReference,
    });

    const itemsField = python.field({
      name: "items",
      initializer: this.getNodeInputByName("items"),
    });

    const outputsClass = this.generateOutputsClass();

    return [itemsField, subworkflowField, outputsClass];
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

    return statements;
  }

  private generateOutputsClass(): python.Class {
    const nodeBaseClassRef = this.getNodeBaseClass();
    const outputsClass = python.class_({
      name: OUTPUTS_CLASS_NAME,
      extends_: [
        python.reference({
          name: nodeBaseClassRef.name,
          modulePath: nodeBaseClassRef.modulePath,
          alias: nodeBaseClassRef.alias,
          attribute: [OUTPUTS_CLASS_NAME],
        }),
      ],
    });

    const nestedWorkflowContext = this.getNestedWorkflowContextByName(
      BaseNestedWorkflowNode.subworkflowNestedProjectName
    );

    nestedWorkflowContext.workflowOutputContexts.forEach((outputContext) => {
      const outputName = outputContext.getOutputName();
      const outputField = python.field({
        name: outputName,
        initializer: python.reference({
          name: nestedWorkflowContext.workflowClassName,
          modulePath: nestedWorkflowContext.modulePath,
          attribute: [OUTPUTS_CLASS_NAME, outputName],
        }),
      });

      outputsClass.add(outputField);
    });

    return outputsClass;
  }

  protected getNestedWorkflowProject(): WorkflowProjectGenerator {
    if (this.nodeData.data.variant !== "INLINE") {
      throw new Error(
        `MapNode only supports INLINE variant. Received: ${this.nodeData.data.variant}`
      );
    }

    const mapNodeData = this.nodeData.data;
    const nestedWorkflowContext = this.getNestedWorkflowContextByName(
      BaseNestedWorkflowNode.subworkflowNestedProjectName
    );

    return new WorkflowProjectGenerator({
      workflowVersionExecConfig: {
        workflowRawData: mapNodeData.workflowRawData,
        inputVariables: mapNodeData.inputVariables,
        outputVariables: mapNodeData.outputVariables,
      },
      workflowContext: nestedWorkflowContext,
    });
  }

  protected getOutputDisplay(): python.Field {
    let nodeData: InlineMapNodeData;
    if (this.nodeData.data.variant !== "INLINE") {
      throw new Error(
        `MapNode only supports INLINE variant. Received: ${this.nodeData.data.variant}`
      );
    } else {
      nodeData = this.nodeData.data;
    }

    let outputValue: AstNode;
    const output = nodeData.outputVariables.find(
      (output) => output.key === "final-output"
    );
    if (output?.id) {
      outputValue = python.TypeInstantiation.uuid(output.id);
    } else {
      throw new Error(
        "Output with key 'final-output' is missing from map node"
      );
    }

    return python.field({
      name: "output_display",
      initializer: python.TypeInstantiation.dict([
        {
          key: python.reference({
            name: this.nodeContext.nodeClassName,
            modulePath: this.nodeContext.nodeModulePath,
            attribute: [OUTPUTS_CLASS_NAME, "final_output"],
          }),
          value: python.instantiateClass({
            classReference: python.reference({
              name: "NodeOutputDisplay",
              modulePath:
                this.workflowContext.sdkModulePathNames
                  .NODE_DISPLAY_TYPES_MODULE_PATH,
            }),
            arguments_: [
              python.methodArgument({
                name: "id",
                value: outputValue,
              }),
              python.methodArgument({
                name: "name",
                value: python.TypeInstantiation.str("final_output"),
              }),
            ],
          }),
        },
      ]),
    });
  }

  protected getErrorOutputId(): string | undefined {
    return this.nodeData.data.errorOutputId;
  }
}
