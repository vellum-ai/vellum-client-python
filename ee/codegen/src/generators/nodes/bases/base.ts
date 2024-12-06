import { python } from "@fern-api/python-ast";
import { AstNode } from "@fern-api/python-ast/core/AstNode";

import * as codegen from "src/codegen";
import { PORTS_CLASS_NAME } from "src/constants";
import { WorkflowContext } from "src/context";
import { BaseNodeContext } from "src/context/node-context/base";
import {
  BaseCodegenError,
  NodeAttributeGenerationError,
} from "src/generators/errors";
import { NodeDisplayData } from "src/generators/node-display-data";
import { NodeInput } from "src/generators/node-inputs/node-input";
import { WorkflowProjectGenerator } from "src/project";
import { WorkflowDataNode } from "src/types/vellum";

export declare namespace BaseNode {
  interface Args<T extends WorkflowDataNode, V extends BaseNodeContext<T>> {
    workflowContext: WorkflowContext;
    nodeContext: V;
  }
}

export abstract class BaseNode<
  T extends WorkflowDataNode,
  V extends BaseNodeContext<T>
> {
  public readonly workflowContext: WorkflowContext;
  public readonly nodeData: T;
  public readonly nodeContext: V;

  protected readonly nodeInputsByKey: Map<string, NodeInput>;

  protected abstract readonly baseNodeClassName: string;
  protected abstract readonly baseNodeDisplayClassName: string;
  private readonly errorOutputId: string | undefined;

  constructor({ workflowContext, nodeContext }: BaseNode.Args<T, V>) {
    this.workflowContext = workflowContext;
    this.nodeContext = nodeContext;
    this.nodeData = nodeContext.nodeData;

    this.nodeInputsByKey = this.generateNodeInputs();
    this.errorOutputId = this.getErrorOutputId();
  }

  public abstract persist(): Promise<void>;

  protected abstract getNodeClassBodyStatements(): AstNode[];

  protected abstract getNodeDisplayClassBodyStatements(): AstNode[];

  // Override to specify a custom output display
  protected abstract getOutputDisplay(): python.Field | undefined;

  // If the node supports the Reject on Error toggle, then implement this to return
  // the error_output_id from this.nodeData. If returned, a @TryNode decorator will be
  // added to the node class.
  protected abstract getErrorOutputId(): string | undefined;

  // Override if the node implementation's base class needs to include generic types
  protected getNodeBaseGenericTypes(): AstNode[] | undefined {
    return undefined;
  }

  protected getNodeBaseClass(): python.Reference {
    const baseNodeClassNameAlias =
      this.baseNodeClassName === this.nodeContext.nodeClassName
        ? `Base${this.baseNodeClassName}`
        : undefined;

    const baseNodeGenericTypes = this.getNodeBaseGenericTypes();

    return python.reference({
      name: this.baseNodeClassName,
      modulePath:
        this.workflowContext.sdkModulePathNames.DISPLAYABLE_NODES_MODULE_PATH,
      genericTypes: baseNodeGenericTypes,
      alias: baseNodeClassNameAlias,
    });
  }

  protected getNodeDisplayBaseClass(): python.Reference {
    return python.reference({
      name: this.baseNodeDisplayClassName,
      modulePath:
        this.workflowContext.sdkModulePathNames.NODE_DISPLAY_MODULE_PATH,
      genericTypes: [
        python.reference({
          name: this.nodeContext.nodeClassName,
          modulePath: this.nodeContext.nodeModulePath,
        }),
      ],
    });
  }

  /* Override if the node implementation needs to generate nested workflows */
  protected generateNestedWorkflowContexts(): Map<string, WorkflowContext> {
    return new Map();
  }

  /* Override if the node implementation needs to generate nested workflows */
  protected generateNestedProjectsByName(): Map<
    string,
    WorkflowProjectGenerator
  > {
    return new Map();
  }

  protected findNodeInputByName(name: string): NodeInput | undefined {
    return this.nodeInputsByKey.get(name);
  }

  protected getNodeInputByName(name: string): NodeInput {
    const nodeInput = this.findNodeInputByName(name);
    if (!nodeInput) {
      throw new Error(`No input found named "${name}"`);
    }

    return nodeInput;
  }

  public getNodeClassName() {
    return this.nodeContext.nodeClassName;
  }

  public getNodeModulePath() {
    return this.nodeContext.nodeModulePath;
  }

  public getNodeDisplayClassName() {
    return this.nodeContext.nodeDisplayClassName;
  }

  public getNodeDisplayModulePath() {
    return this.nodeContext.nodeDisplayModulePath;
  }

  private generateNodeInputs(): Map<string, NodeInput> {
    const generatedNodeInputs = new Map<string, NodeInput>();

    if (!("inputs" in this.nodeData)) {
      return generatedNodeInputs;
    }

    this.nodeData.inputs.forEach((nodeInputData) => {
      try {
        const nodeInput = codegen.nodeInput({
          workflowContext: this.workflowContext,
          nodeInputData,
        });

        generatedNodeInputs.set(nodeInputData.key, nodeInput);
      } catch (error) {
        if (error instanceof BaseCodegenError) {
          throw new NodeAttributeGenerationError(
            `Failed to generate attribute '${this.nodeContext.nodeClassName}.inputs.${nodeInputData.key}': ${error.message}`
          );
        }
        throw error;
      }
    });

    return generatedNodeInputs;
  }

  protected getPortDisplay(): python.Field | undefined {
    if (
      !("data" in this.nodeData) ||
      !("sourceHandleId" in this.nodeData.data)
    ) {
      return;
    }

    return python.field({
      name: "port_displays",
      initializer: python.TypeInstantiation.dict([
        {
          key: python.reference({
            name: this.nodeContext.nodeClassName,
            modulePath: this.nodeContext.nodeModulePath,
            attribute: [PORTS_CLASS_NAME, "default"],
          }),
          value: python.instantiateClass({
            classReference: python.reference({
              name: "PortDisplayOverrides",
              modulePath:
                this.workflowContext.sdkModulePathNames
                  .NODE_DISPLAY_TYPES_MODULE_PATH,
            }),
            arguments_: [
              python.methodArgument({
                name: "id",
                value: python.TypeInstantiation.uuid(
                  this.nodeData.data.sourceHandleId
                ),
              }),
            ],
          }),
        },
      ]),
    });
  }

  private getDisplayData(): python.Field {
    return python.field({
      name: "display_data",
      initializer: new NodeDisplayData({
        workflowContext: this.workflowContext,
        nodeDisplayData: this.nodeData.displayData,
      }),
    });
  }

  public generateNodeClass(): python.Class {
    const nodeContext = this.nodeContext;

    let nodeBaseClass: python.Reference = this.getNodeBaseClass();
    if (nodeBaseClass.name === nodeContext.nodeClassName) {
      nodeBaseClass = python.reference({
        name: nodeBaseClass.name,
        modulePath: nodeBaseClass.modulePath,
        genericTypes: nodeBaseClass.genericTypes,
        alias: `Base${nodeBaseClass.name}`,
        attribute: nodeBaseClass.attribute,
      });
    }

    const nodeClass = python.class_({
      name: nodeContext.nodeClassName,
      extends_: [nodeBaseClass],
      decorators: this.errorOutputId
        ? [
            python.decorator({
              callable: python.invokeMethod({
                methodReference: python.reference({
                  name: "TryNode",
                  attribute: ["wrap"],
                  modulePath:
                    this.workflowContext.sdkModulePathNames
                      .CORE_NODES_MODULE_PATH,
                }),
                arguments_: [],
              }),
            }),
          ]
        : undefined,
    });

    this.getNodeClassBodyStatements().forEach((statement) =>
      nodeClass.add(statement)
    );

    return nodeClass;
  }

  public generateNodeDisplayClasses(): python.Class[] {
    const nodeContext = this.nodeContext;

    const nodeClass = python.class_({
      name: nodeContext.nodeDisplayClassName,
      extends_: [this.getNodeDisplayBaseClass()],
    });

    this.getNodeDisplayClassBodyStatements().forEach((statement) =>
      nodeClass.add(statement)
    );

    const nodeInputIdsByNameField = python.field({
      name: "node_input_ids_by_name",
      initializer: python.TypeInstantiation.dict(
        Array.from(this.nodeInputsByKey).map<{
          key: AstNode;
          value: AstNode;
        }>(([key, nodeInput]) => {
          return {
            key: python.TypeInstantiation.str(key),
            value: python.TypeInstantiation.uuid(nodeInput.nodeInputData.id),
          };
        })
      ),
    });
    nodeClass.add(nodeInputIdsByNameField);

    const outputDisplay = this.getOutputDisplay();
    if (outputDisplay) {
      nodeClass.add(outputDisplay);
    }

    const portDisplay = this.getPortDisplay();
    if (portDisplay) {
      nodeClass.add(portDisplay);
    }

    nodeClass.add(this.getDisplayData());

    const errorOutputId = this.getErrorOutputId();
    if (!errorOutputId) {
      return [nodeClass];
    }

    const tryNodeDisplayClass = python.class_({
      name: "TryNodeDisplay",
      extends_: [
        python.reference({
          name: "BaseTryNodeDisplay",
          modulePath:
            this.workflowContext.sdkModulePathNames.NODE_DISPLAY_MODULE_PATH,
        }),
      ],
    });
    tryNodeDisplayClass.add(
      python.field({
        name: "error_output_id",
        initializer: python.TypeInstantiation.uuid(errorOutputId),
      })
    );

    return [tryNodeDisplayClass, nodeClass];
  }
}
