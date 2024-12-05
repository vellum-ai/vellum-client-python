import { python } from "@fern-api/python-ast";
import { OperatorType } from "@fern-api/python-ast/OperatorType";
import { Reference } from "@fern-api/python-ast/Reference";
import { Type } from "@fern-api/python-ast/Type";
import { AstNode } from "@fern-api/python-ast/core/AstNode";

import { BasePersistedFile } from "./base-persisted-file";
import { WorkflowOutput } from "./workflow-output";

import {
  GENERATED_DISPLAY_MODULE_NAME,
  GENERATED_WORKFLOW_MODULE_NAME,
  OUTPUTS_CLASS_NAME,
  PORTS_CLASS_NAME,
} from "src/constants";
import { WorkflowContext } from "src/context";
import { BaseNodeContext } from "src/context/node-context/base";
import { PortContext } from "src/context/port-context";
import { BaseState } from "src/generators/base-state";
import { Inputs } from "src/generators/inputs";
import { NodeDisplayData } from "src/generators/node-display-data";
import {
  WorkflowDataNode,
  WorkflowDisplayData,
  WorkflowEdge,
} from "src/types/vellum";
import { getNodeId } from "src/utils/nodes";
import { isDefined } from "src/utils/typing";

export declare namespace Workflow {
  interface Args {
    /* The name of the module that the workflow class belongs to */
    moduleName: string;
    /* The context for the workflow */
    workflowContext: WorkflowContext;
    /* The inputs for the workflow */
    inputs: Inputs;
    /* The nodes in the workflow */
    nodes: WorkflowDataNode[];
    /* The display data for the workflow */
    displayData?: WorkflowDisplayData;
    /*
    Whether to use the new graph generation algorithm

    We are using this as a feature flag to build out the new graph generation algorithm
    over the course of a few PRs, each with a new test to satisfy, instead of all at once.
    */
    breadthFirstGraphGeneration?: boolean;
  }
}

export class Workflow {
  public readonly workflowContext: WorkflowContext;
  private readonly inputs: Inputs;
  private readonly nodes: WorkflowDataNode[];
  private readonly edgesByPortId: Map<string, WorkflowEdge[]>;
  private readonly entrypointPortContexts: PortContext[];
  private readonly entrypointNodeEdges: WorkflowEdge[];
  private readonly displayData: WorkflowDisplayData | undefined;
  private readonly breadthFirstGraphGeneration: boolean;
  private readonly entrypointNodeId: string;
  constructor({
    workflowContext,
    inputs,
    nodes,
    displayData,
    breadthFirstGraphGeneration,
  }: Workflow.Args) {
    this.workflowContext = workflowContext;
    this.inputs = inputs;
    this.nodes = nodes;
    this.displayData = displayData;

    const edges = this.workflowContext.workflowRawEdges;
    const {
      edgesByPortId,
      entrypointPortContexts,
      entrypointNodeEdges,
      entrypointNodeId,
    } = this.getEdgesAndEntrypointNodeContexts({ nodes, edges });
    this.edgesByPortId = edgesByPortId;
    this.entrypointPortContexts = entrypointPortContexts;
    this.entrypointNodeEdges = entrypointNodeEdges;
    this.entrypointNodeId = entrypointNodeId;
    this.breadthFirstGraphGeneration = breadthFirstGraphGeneration ?? false;
  }

  private getEdgesAndEntrypointNodeContexts({
    nodes,
    edges,
  }: {
    nodes: WorkflowDataNode[];
    edges: WorkflowEdge[];
  }) {
    const entrypointNodeId = this.workflowContext.getEntrypointNode().id;
    const nodeIds = new Set<string>([
      ...nodes.map((node) => getNodeId(node)),
      entrypointNodeId,
    ]);
    const edgesByPortId = new Map<string, WorkflowEdge[]>();
    let entrypointPortContexts: PortContext[] = [];
    const entrypointNodeEdges: WorkflowEdge[] = [];

    edges.forEach((edge) => {
      // Handle edge case where there are zombie edges that point to nodes that don't exist
      if (!nodeIds.has(edge.sourceNodeId) || !nodeIds.has(edge.targetNodeId)) {
        return;
      }

      if (edge.sourceNodeId === entrypointNodeId) {
        const targetNodeContext = this.workflowContext.getNodeContext(
          edge.targetNodeId
        );

        const newEntrypointPortContexts = Array.from(
          targetNodeContext.portContextsById.values()
        );

        entrypointPortContexts = entrypointPortContexts.concat(
          newEntrypointPortContexts
        );
        entrypointNodeEdges.push(edge);
      }

      const portId = edge.sourceHandleId;

      const edges = edgesByPortId.get(portId) ?? [];
      edges.push(edge);
      edgesByPortId.set(portId, edges);
    });

    return {
      edgesByPortId,
      entrypointPortContexts,
      entrypointNodeEdges,
      entrypointNodeId,
    };
  }

  private generateParentWorkflowClass(): python.Reference {
    let parentGenerics: Type[] | undefined;

    if (this.inputs.inputsClass) {
      let inputsClassRef: python.Reference;
      if (this.inputs.inputsClass) {
        inputsClassRef = python.reference({
          name: this.inputs.inputsClass.name,
          modulePath: this.inputs.getModulePath(),
        });
      } else {
        inputsClassRef = this.inputs.baseInputsClassReference;
      }

      const baseStateClassReference = new BaseState({
        workflowContext: this.workflowContext,
      });

      parentGenerics = [
        python.Type.reference(inputsClassRef),
        python.Type.reference(baseStateClassReference),
      ];
    }

    const baseWorkflowClassRef = python.reference({
      name: "BaseWorkflow",
      modulePath: this.workflowContext.sdkModulePathNames.WORKFLOWS_MODULE_PATH,
      genericTypes: parentGenerics,
    });

    return baseWorkflowClassRef;
  }

  private generateOutputsClass(parentWorkflowClass: Reference): python.Class {
    const outputsClass = python.class_({
      name: OUTPUTS_CLASS_NAME,
      extends_: [
        python.reference({
          name: parentWorkflowClass.name,
          modulePath: parentWorkflowClass.modulePath,
          attribute: [OUTPUTS_CLASS_NAME],
        }),
      ],
    });

    this.workflowContext.workflowOutputContexts.forEach(
      (workflowOutputContext) => {
        outputsClass.add(
          new WorkflowOutput({
            workflowContext: this.workflowContext,
            workflowOutputContext,
          })
        );
      }
    );

    return outputsClass;
  }

  public generateWorkflowClass(): python.Class {
    const workflowClassName = this.workflowContext.workflowClassName;

    const baseWorkflowClassRef = this.generateParentWorkflowClass();

    const workflowClass = python.class_({
      name: workflowClassName,
      extends_: [baseWorkflowClassRef],
    });
    workflowClass.inheritReferences(baseWorkflowClassRef);

    this.addGraph(workflowClass);

    const outputsClass = this.generateOutputsClass(baseWorkflowClassRef);
    workflowClass.add(outputsClass);

    return workflowClass;
  }

  public generateWorkflowDisplayClass(): python.Class {
    const workflowDisplayClassName = `${this.workflowContext.workflowClassName}Display`;

    const workflowClassRef = python.reference({
      name: this.workflowContext.workflowClassName,
      modulePath: this.workflowContext.modulePath,
    });

    const workflowDisplayClass = python.class_({
      name: workflowDisplayClassName,
      extends_: [
        python.reference({
          name: "VellumWorkflowDisplay",
          modulePath:
            this.workflowContext.sdkModulePathNames
              .WORKFLOWS_DISPLAY_MODULE_PATH,
          genericTypes: [workflowClassRef],
        }),
      ],
    });
    workflowDisplayClass.inheritReferences(workflowClassRef);

    const entrypointNode = this.workflowContext.getEntrypointNode();
    workflowDisplayClass.add(
      python.field({
        name: "workflow_display",
        initializer: python.instantiateClass({
          classReference: python.reference({
            name: "WorkflowMetaVellumDisplayOverrides",
            modulePath:
              this.workflowContext.sdkModulePathNames.VELLUM_TYPES_MODULE_PATH,
          }),
          arguments_: [
            python.methodArgument({
              name: "entrypoint_node_id",
              value: python.TypeInstantiation.uuid(entrypointNode.id),
            }),
            python.methodArgument({
              name: "entrypoint_node_source_handle_id",
              value: python.TypeInstantiation.uuid(
                entrypointNode.data.sourceHandleId
              ),
            }),
            python.methodArgument({
              name: "entrypoint_node_display",
              value: new NodeDisplayData({
                workflowContext: this.workflowContext,
                nodeDisplayData: entrypointNode.displayData,
              }),
            }),
            python.methodArgument({
              name: "display_data",
              value: python.instantiateClass({
                classReference: python.reference({
                  name: "WorkflowDisplayData",
                  modulePath:
                    this.workflowContext.sdkModulePathNames
                      .VELLUM_TYPES_MODULE_PATH,
                }),
                arguments_: [
                  python.methodArgument({
                    name: "viewport",
                    value: python.instantiateClass({
                      classReference: python.reference({
                        name: "WorkflowDisplayDataViewport",
                        modulePath:
                          this.workflowContext.sdkModulePathNames
                            .VELLUM_TYPES_MODULE_PATH,
                      }),
                      arguments_: [
                        python.methodArgument({
                          name: "x",
                          value: python.TypeInstantiation.float(
                            this.displayData?.viewport.x ?? 0
                          ),
                        }),
                        python.methodArgument({
                          name: "y",
                          value: python.TypeInstantiation.float(
                            this.displayData?.viewport.y ?? 0
                          ),
                        }),
                        python.methodArgument({
                          name: "zoom",
                          value: python.TypeInstantiation.float(
                            this.displayData?.viewport.zoom ?? 0
                          ),
                        }),
                      ],
                    }),
                  }),
                ],
              }),
            }),
          ],
        }),
      })
    );

    workflowDisplayClass.add(
      python.field({
        name: "inputs_display",
        initializer: python.TypeInstantiation.dict(
          Array.from(this.workflowContext.inputVariableContextsById)
            .map(([_, inputVariableContext]) => {
              const inputsClass = this.inputs.inputsClass;
              if (!inputsClass) {
                return;
              }

              return {
                key: python.reference({
                  name: inputsClass.name,
                  modulePath: this.inputs.getModulePath(),
                  attribute: [inputVariableContext.getInputVariableName()],
                }),
                value: python.instantiateClass({
                  classReference: python.reference({
                    name: "WorkflowInputsVellumDisplayOverrides",
                    modulePath:
                      this.workflowContext.sdkModulePathNames
                        .VELLUM_TYPES_MODULE_PATH,
                  }),
                  arguments_: [
                    python.methodArgument({
                      name: "id",
                      value: python.TypeInstantiation.uuid(
                        inputVariableContext.getInputVariableId()
                      ),
                    }),
                  ],
                }),
              };
            })
            .filter(isDefined)
        ),
      })
    );

    workflowDisplayClass.add(
      python.field({
        name: "entrypoint_displays",
        initializer: python.TypeInstantiation.dict(
          this.entrypointNodeEdges.map((edge) => {
            const defaultEntrypointNodeContext =
              this.workflowContext.getNodeContext(edge.targetNodeId);

            return {
              key: python.reference({
                name: defaultEntrypointNodeContext.nodeClassName,
                modulePath: defaultEntrypointNodeContext.nodeModulePath,
              }),
              value: python.instantiateClass({
                classReference: python.reference({
                  name: "EntrypointVellumDisplayOverrides",
                  modulePath:
                    this.workflowContext.sdkModulePathNames
                      .VELLUM_TYPES_MODULE_PATH,
                }),
                arguments_: [
                  python.methodArgument({
                    name: "id",
                    value: python.TypeInstantiation.uuid(entrypointNode.id),
                  }),
                  python.methodArgument({
                    name: "edge_display",
                    value: python.instantiateClass({
                      classReference: python.reference({
                        name: "EdgeVellumDisplayOverrides",
                        modulePath:
                          this.workflowContext.sdkModulePathNames
                            .VELLUM_TYPES_MODULE_PATH,
                      }),
                      arguments_: [
                        python.methodArgument({
                          name: "id",
                          value: python.TypeInstantiation.uuid(edge.id),
                        }),
                      ],
                    }),
                  }),
                ],
              }),
            };
          })
        ),
      })
    );

    const edgeDisplayEntries: { key: AstNode; value: AstNode }[] =
      this.getEdges().reduce<{ key: AstNode; value: AstNode }[]>(
        (acc, edge) => {
          // Stable id references of edges connected to entrypoint nodes are handles separately as part of
          // `entrypoint_displays` and don't need to be taken care of here.
          const entrypointNode = this.workflowContext.getEntrypointNode();
          if (edge.sourceNodeId === entrypointNode.id) {
            return acc;
          }

          const sourcePortId = edge.sourceHandleId;
          const sourcePortContext =
            this.workflowContext.getPortContextById(sourcePortId);

          const targetNodeId = edge.targetNodeId;
          const targetNode = this.workflowContext.getNodeContext(targetNodeId);

          const edgeDisplayEntry = {
            key: python.TypeInstantiation.tuple([
              python.reference({
                name: sourcePortContext.nodeContext.nodeClassName,
                modulePath: sourcePortContext.nodeContext.nodeModulePath,
                attribute: [PORTS_CLASS_NAME, sourcePortContext.portName],
              }),
              python.reference({
                name: targetNode.nodeClassName,
                modulePath: targetNode.nodeModulePath,
              }),
            ]),
            value: python.instantiateClass({
              classReference: python.reference({
                name: "EdgeVellumDisplayOverrides",
                modulePath:
                  this.workflowContext.sdkModulePathNames
                    .VELLUM_TYPES_MODULE_PATH,
              }),
              arguments_: [
                python.methodArgument({
                  name: "id",
                  value: python.TypeInstantiation.uuid(edge.id),
                }),
              ],
            }),
          };

          return [...acc, edgeDisplayEntry];
        },
        []
      );
    if (edgeDisplayEntries.length) {
      workflowDisplayClass.add(
        python.field({
          name: "edge_displays",
          initializer: python.TypeInstantiation.dict(edgeDisplayEntries),
        })
      );
    }

    workflowDisplayClass.add(
      python.field({
        name: "output_displays",
        initializer: python.TypeInstantiation.dict(
          this.workflowContext.workflowOutputContexts.map(
            (workflowOutputContext) => {
              const terminalNodeData =
                workflowOutputContext.getFinalOutputNodeData();

              const edge = this.getEdges().find((edge) => {
                return (
                  edge.targetNodeId === terminalNodeData.id &&
                  edge.targetHandleId === terminalNodeData.data.targetHandleId
                );
              });

              if (!edge) {
                throw new Error(
                  `Could not find edge for terminal node ${terminalNodeData.id}`
                );
              }

              return {
                key: python.reference({
                  name: this.workflowContext.workflowClassName,
                  modulePath: this.workflowContext.modulePath,
                  attribute: [
                    OUTPUTS_CLASS_NAME,
                    workflowOutputContext.getOutputName(),
                  ],
                }),
                value: python.instantiateClass({
                  classReference: python.reference({
                    name: "WorkflowOutputVellumDisplayOverrides",
                    modulePath:
                      this.workflowContext.sdkModulePathNames
                        .VELLUM_TYPES_MODULE_PATH,
                  }),
                  arguments_: [
                    python.methodArgument({
                      name: "id",
                      value: python.TypeInstantiation.uuid(
                        terminalNodeData.data.outputId
                      ),
                    }),
                    python.methodArgument({
                      name: "node_id",
                      value: python.TypeInstantiation.uuid(terminalNodeData.id),
                    }),
                    python.methodArgument({
                      name: "node_input_id",
                      value: python.TypeInstantiation.uuid(
                        terminalNodeData.data.nodeInputId
                      ),
                    }),
                    python.methodArgument({
                      name: "name",
                      value: python.TypeInstantiation.str(
                        terminalNodeData.data.name
                      ),
                    }),
                    python.methodArgument({
                      name: "label",
                      value: python.TypeInstantiation.str(
                        terminalNodeData.data.label
                      ),
                    }),
                    python.methodArgument({
                      name: "target_handle_id",
                      value: python.TypeInstantiation.uuid(
                        terminalNodeData.data.targetHandleId
                      ),
                    }),
                    python.methodArgument({
                      name: "display_data",
                      value: new NodeDisplayData({
                        nodeDisplayData: terminalNodeData.displayData,
                        workflowContext: this.workflowContext,
                      }),
                    }),
                    python.methodArgument({
                      name: "edge_id",
                      value: python.TypeInstantiation.uuid(edge.id),
                    }),
                  ],
                }),
              };
            }
          )
        ),
      })
    );

    return workflowDisplayClass;
  }

  private getEdges(): WorkflowEdge[] {
    return Array.from(this.edgesByPortId.values()).flat();
  }

  private buildGraphLegacy({
    portContexts,
  }: {
    portContexts: PortContext | PortContext[];
  }): AstNode | undefined {
    if (Array.isArray(portContexts)) {
      if (portContexts.length > 1) {
        const graphItems = portContexts
          .filter((portContext) => {
            return this.edgesByPortId.has(portContext.portId);
          })
          .map((portContext) => this.buildGraphBranchLegacy({ portContext }))
          .filter(isDefined);

        if (graphItems.length > 1) {
          return python.TypeInstantiation.set(graphItems);
        } else {
          return graphItems[0];
        }
      } else {
        const portContext = portContexts[0];
        if (!portContext) {
          return;
        }
        return this.buildGraphBranchLegacy({ portContext });
      }
    } else {
      return this.buildGraphBranchLegacy({ portContext: portContexts });
    }
  }

  private buildGraphBranchLegacy({
    portContext,
  }: {
    portContext: PortContext;
  }): AstNode | undefined {
    const edges = this.edgesByPortId.get(portContext.portId);
    if (!edges) {
      const terminalNodeRef = python.reference({
        name: portContext.nodeContext.nodeClassName,
        modulePath: portContext.nodeContext.nodeModulePath,
        attribute: portContext.isDefault
          ? undefined
          : [PORTS_CLASS_NAME, portContext.portName],
      });
      return terminalNodeRef;
    }

    const targetNodeContexts = edges.map((edge) =>
      this.workflowContext.getNodeContext(edge.targetNodeId)
    );

    if (targetNodeContexts.length === 0) {
      const terminalNodeRef = python.reference({
        name: portContext.nodeContext.nodeClassName,
        modulePath: portContext.nodeContext.nodeModulePath,
      });
      return terminalNodeRef;
    }

    const subGraphs = targetNodeContexts
      .map((targetNodeContext) => {
        const portContexts = Array.from(
          targetNodeContext.portContextsById.values()
        );

        if (portContexts.length === 0) {
          return python.reference({
            name: targetNodeContext.nodeClassName,
            modulePath: targetNodeContext.nodeModulePath,
          });
        }

        return this.buildGraphLegacy({ portContexts });
      })
      .filter(isDefined);

    const lhs = python.reference({
      name: portContext.nodeContext.nodeClassName,
      modulePath: portContext.nodeContext.nodeModulePath,
      attribute: portContext.isDefault
        ? undefined
        : [PORTS_CLASS_NAME, portContext.portName],
    });

    const subgraphFirstItem = subGraphs[0];
    if (!subgraphFirstItem) {
      return;
    }
    const rhs =
      subGraphs.length > 1
        ? python.TypeInstantiation.set(subGraphs)
        : subgraphFirstItem;

    return python.operator({
      operator: OperatorType.RightShift,
      lhs,
      rhs,
    });
  }

  private buildGraphAttribute(): AstNode | undefined {
    if (!this.breadthFirstGraphGeneration) {
      return this.buildGraphLegacy({
        portContexts: this.entrypointPortContexts,
      });
    }

    // This graph attribute generation is a breadth-first traversal of the WorkflowEdges
    // starting at the entrypoint port edges. We process each one sequentially and incrementally
    // build up the graph as we go.
    type GraphEmpty = { type: "empty" };
    type GraphSet = { type: "set"; values: GraphMutableAst[] };
    type GraphNodeReference = {
      type: "node_reference";
      reference: BaseNodeContext<WorkflowDataNode>;
    };
    type GraphPortReference = {
      type: "port_reference";
      reference: PortContext;
    };
    type GraphRightShift = {
      type: "right_shift";
      lhs: GraphMutableAst;
      rhs: GraphMutableAst;
    };
    type GraphMutableAst =
      | GraphEmpty
      | GraphSet
      | GraphNodeReference
      | GraphPortReference
      | GraphRightShift;

    let graphMutableAst: GraphMutableAst = { type: "empty" };
    const edgesQueue = [...this.entrypointNodeEdges];
    const processedEdges = new Set<WorkflowEdge>();

    while (edgesQueue.length > 0) {
      const edge = edgesQueue.shift();
      if (!edge) {
        continue;
      }

      const sourceNode =
        edge.sourceNodeId === this.entrypointNodeId
          ? null
          : this.workflowContext.getNodeContext(edge.sourceNodeId);

      const targetNode = this.workflowContext.getNodeContext(edge.targetNodeId);
      if (!targetNode) {
        processedEdges.add(edge);
        continue;
      }

      const isPlural = (mutableAst: GraphMutableAst): boolean => {
        return (
          mutableAst.type === "right_shift" ||
          (mutableAst.type === "set" && mutableAst.values.every(isPlural))
        );
      };

      const getAstSources = (
        mutableAst: GraphMutableAst
      ): GraphPortReference[] => {
        if (mutableAst.type === "empty") {
          return [];
        } else if (mutableAst.type === "node_reference") {
          const defaultPort = mutableAst.reference.defaultPortContext;
          if (defaultPort) {
            return [
              {
                type: "port_reference",
                reference: defaultPort,
              },
            ];
          }
          return [];
        } else if (mutableAst.type === "set") {
          return mutableAst.values.flatMap(getAstSources);
        } else if (mutableAst.type === "right_shift") {
          return getAstSources(mutableAst.lhs);
        } else if (mutableAst.type == "port_reference") {
          return [mutableAst];
        } else {
          return [];
        }
      };

      const getAstTerminals = (
        mutableAst: GraphMutableAst
      ): GraphNodeReference[] => {
        if (mutableAst.type === "empty") {
          return [];
        } else if (mutableAst.type === "node_reference") {
          return [mutableAst];
        } else if (mutableAst.type === "set") {
          return mutableAst.values.flatMap(getAstTerminals);
        } else if (mutableAst.type === "right_shift") {
          return getAstTerminals(mutableAst.rhs);
        } else if (mutableAst.type == "port_reference") {
          return [
            {
              type: "node_reference",
              reference: mutableAst.reference.nodeContext,
            },
          ];
        } else {
          return [];
        }
      };

      const popSources = (mutableAst: GraphMutableAst): GraphMutableAst => {
        if (mutableAst.type === "set") {
          return {
            type: "set",
            values: mutableAst.values.map(popSources),
          };
        } else if (mutableAst.type === "right_shift") {
          return mutableAst.rhs;
        } else {
          return { type: "empty" };
        }
      };

      const popTerminals = (mutableAst: GraphMutableAst): GraphMutableAst => {
        if (mutableAst.type === "set") {
          return {
            type: "set",
            values: mutableAst.values.map(popTerminals),
          };
        } else if (mutableAst.type === "right_shift") {
          return mutableAst.lhs;
        } else {
          return { type: "empty" };
        }
      };

      const addEdgeToGraph = (
        mutableAst: GraphMutableAst
      ): GraphMutableAst | undefined => {
        if (mutableAst.type === "empty") {
          return {
            type: "node_reference",
            reference: targetNode,
          };
        } else if (mutableAst.type === "node_reference") {
          if (sourceNode && mutableAst.reference === sourceNode) {
            const sourceNodePortContext = sourceNode.portContextsById.get(
              edge.sourceHandleId
            );
            if (sourceNodePortContext) {
              if (sourceNodePortContext.isDefault) {
                return {
                  type: "right_shift",
                  lhs: mutableAst,
                  rhs: { type: "node_reference", reference: targetNode },
                };
              } else {
                return {
                  type: "right_shift",
                  lhs: {
                    type: "port_reference",
                    reference: sourceNodePortContext,
                  },
                  rhs: { type: "node_reference", reference: targetNode },
                };
              }
            }
          } else if (!sourceNode) {
            return {
              type: "set",
              values: [
                mutableAst,
                { type: "node_reference", reference: targetNode },
              ],
            };
          }
        } else if (mutableAst.type === "set") {
          const newSet = mutableAst.values.map((subAst) => {
            const newSubAst = addEdgeToGraph(subAst);
            if (!newSubAst) {
              return { edgeAdded: false, value: subAst };
            }
            return { edgeAdded: true, value: newSubAst };
          });
          if (newSet.every(({ edgeAdded }) => !edgeAdded)) {
            return {
              type: "set",
              values: [
                mutableAst,
                { type: "node_reference", reference: targetNode },
              ],
            };
          }
          const newSetAst: GraphSet = {
            type: "set",
            values: newSet.map(({ value }) => value),
          };

          if (isPlural(newSetAst)) {
            const newAstTerminals = newSetAst.values.flatMap((value) =>
              getAstTerminals(value)
            );

            const uniqueAstTerminalIds = new Set(
              newAstTerminals.map((terminal) => terminal.reference.getNodeId())
            );
            if (uniqueAstTerminalIds.size === 1 && newAstTerminals[0]) {
              // If all the terminals are the same, we can simplify the graph into a
              // right shift between the set and the target node.
              return {
                type: "right_shift",
                lhs: popTerminals(newSetAst),
                rhs: newAstTerminals[0],
              };
            }
          }

          return newSetAst;
        } else if (mutableAst.type === "right_shift") {
          const newLhs = addEdgeToGraph(mutableAst.lhs);
          if (newLhs) {
            const newSetAst: GraphSet = {
              type: "set",
              values: [mutableAst, newLhs],
            };
            if (isPlural(newSetAst)) {
              const newAstSources = newSetAst.values.flatMap((value) =>
                getAstSources(value)
              );

              const uniqueAstSourceIds = new Set(
                newAstSources.map((source) => source.reference.portId)
              );
              if (uniqueAstSourceIds.size === 1 && newAstSources[0]) {
                // If all the sources are the same, we can simplify the graph into a
                // right shift between the source node and the set.
                const portReference = newAstSources[0];
                return {
                  type: "right_shift",
                  lhs: portReference,
                  rhs: popSources(newSetAst),
                };
              }
            }
            return newSetAst;
          } else if (
            mutableAst.lhs.type == "port_reference" &&
            sourceNode &&
            mutableAst.lhs.reference.nodeContext == sourceNode
          ) {
            const sourcePortContext = sourceNode.portContextsById.get(
              edge.sourceHandleId
            );
            if (sourcePortContext) {
              return {
                type: "set",
                values: [
                  mutableAst,
                  {
                    type: "right_shift",
                    lhs: {
                      type: "port_reference",
                      reference: sourcePortContext,
                    },
                    rhs: { type: "node_reference", reference: targetNode },
                  },
                ],
              };
            }
          } else if (mutableAst.rhs.type === "node_reference") {
            if (sourceNode && mutableAst.rhs.reference === sourceNode) {
              return {
                type: "right_shift",
                lhs: mutableAst,
                rhs: { type: "node_reference", reference: targetNode },
              };
            }
          }
        }

        return;
      };

      const newMutableAst = addEdgeToGraph(graphMutableAst);
      processedEdges.add(edge);

      if (!newMutableAst) {
        continue;
      }

      graphMutableAst = newMutableAst;
      targetNode.portContextsById.forEach((portContext) => {
        const edges = this.edgesByPortId.get(portContext.portId);
        edges?.forEach((edge) => {
          if (processedEdges.has(edge)) {
            return;
          }
          edgesQueue.push(edge);
        });
      });
    }

    const buildAstNode = (mutableAst: GraphMutableAst): AstNode | undefined => {
      if (mutableAst.type === "empty") {
        return;
      }

      if (mutableAst.type === "node_reference") {
        return python.reference({
          name: mutableAst.reference.nodeClassName,
          modulePath: mutableAst.reference.nodeModulePath,
        });
      }

      if (mutableAst.type === "port_reference") {
        return python.reference({
          name: mutableAst.reference.nodeContext.nodeClassName,
          modulePath: mutableAst.reference.nodeContext.nodeModulePath,
          attribute: mutableAst.reference.isDefault
            ? undefined
            : [PORTS_CLASS_NAME, mutableAst.reference.portName],
        });
      }

      if (mutableAst.type === "set") {
        return python.TypeInstantiation.set(
          mutableAst.values.map(buildAstNode).filter(isDefined)
        );
      }

      if (mutableAst.type === "right_shift") {
        const lhs = buildAstNode(mutableAst.lhs);
        const rhs = buildAstNode(mutableAst.rhs);
        if (!lhs || !rhs) {
          return;
        }
        return python.operator({
          operator: OperatorType.RightShift,
          lhs,
          rhs,
        });
      }

      return;
    };

    return buildAstNode(graphMutableAst);
  }

  private addGraph(workflowClass: python.Class): void {
    if (this.nodes.length === 0) {
      return;
    }

    const graph = this.buildGraphAttribute();

    if (!graph) {
      return;
    }

    const graphField = python.field({
      name: "graph",
      initializer: graph,
    });

    workflowClass.add(graphField);
  }

  public getWorkflowFile(): WorkflowFile {
    return new WorkflowFile({ workflow: this });
  }

  public getWorkflowDisplayFile(): WorkflowDisplayFile {
    return new WorkflowDisplayFile({ workflow: this });
  }
}

declare namespace WorkflowFile {
  interface Args {
    workflow: Workflow;
  }
}

class WorkflowFile extends BasePersistedFile {
  private readonly workflow: Workflow;

  constructor({ workflow }: WorkflowFile.Args) {
    super({ workflowContext: workflow.workflowContext });
    this.workflow = workflow;
  }

  protected getModulePath(): string[] {
    let modulePath: string[];
    if (this.workflowContext.parentNode) {
      modulePath = [
        ...this.workflowContext.parentNode.getNodeModulePath(),
        GENERATED_WORKFLOW_MODULE_NAME,
      ];
    } else {
      modulePath = [
        this.workflowContext.moduleName,
        GENERATED_WORKFLOW_MODULE_NAME,
      ];
    }

    return modulePath;
  }

  protected getFileStatements(): AstNode[] {
    return [this.workflow.generateWorkflowClass()];
  }
}

declare namespace WorkflowDisplayFile {
  interface Args {
    workflow: Workflow;
  }
}

class WorkflowDisplayFile extends BasePersistedFile {
  private readonly workflow: Workflow;

  constructor({ workflow }: WorkflowDisplayFile.Args) {
    super({ workflowContext: workflow.workflowContext });

    this.workflow = workflow;
  }

  protected getModulePath(): string[] {
    let modulePath: string[];
    if (this.workflowContext.parentNode) {
      modulePath = [
        ...this.workflowContext.parentNode.getNodeDisplayModulePath(),
        GENERATED_WORKFLOW_MODULE_NAME,
      ];
    } else {
      modulePath = [
        this.workflowContext.moduleName,
        GENERATED_DISPLAY_MODULE_NAME,
        GENERATED_WORKFLOW_MODULE_NAME,
      ];
    }

    return modulePath;
  }

  protected getFileStatements(): AstNode[] {
    return [this.workflow.generateWorkflowDisplayClass()];
  }
}
