import { python } from "@fern-api/python-ast";
import { AstNode } from "@fern-api/python-ast/core/AstNode";

import { OUTPUTS_CLASS_NAME } from "src/constants";
import { InlineSubworkflowNodeContext } from "src/context/node-context/inline-subworkflow-node";
import { BaseNestedWorkflowNode } from "src/generators/nodes/bases/nested-workflow-base";
import { WorkflowProjectGenerator } from "src/project";
import {
  SubworkflowNode as SubworkflowNodeType,
  WorkflowRawData,
} from "src/types/vellum";

export class InlineSubworkflowNode extends BaseNestedWorkflowNode<
  SubworkflowNodeType,
  InlineSubworkflowNodeContext
> {
  baseNodeClassName = "InlineSubworkflowNode";
  baseNodeDisplayClassName = "BaseInlineSubworkflowNodeDisplay";

  getInnerWorkflowData(): WorkflowRawData {
    if (this.nodeData.data.variant !== "INLINE") {
      throw new Error(
        `InlineSubworkflowNode only supports INLINE variant. Received: ${this.nodeData.data.variant}`
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

    const outputsClass = this.generateOutputsClass();

    return [subworkflowField, outputsClass];
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

    statements.push(
      python.field({
        name: "workflow_input_ids_by_name",
        initializer: python.TypeInstantiation.dict([]),
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
        `SubworkflowNode only supports INLINE variant. Received: ${this.nodeData.data.variant}`
      );
    }

    const inlineSubworkflowNodeData = this.nodeData.data;
    const nestedWorkflowContext = this.getNestedWorkflowContextByName(
      BaseNestedWorkflowNode.subworkflowNestedProjectName
    );

    return new WorkflowProjectGenerator({
      workflowVersionExecConfig: {
        workflowRawData: inlineSubworkflowNodeData.workflowRawData,
        inputVariables: inlineSubworkflowNodeData.inputVariables,
        outputVariables: inlineSubworkflowNodeData.outputVariables,
      },
      workflowContext: nestedWorkflowContext,
    });
  }

  protected getErrorOutputId(): string | undefined {
    return this.nodeData.data.errorOutputId;
  }
}
