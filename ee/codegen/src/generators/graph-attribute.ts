import { python } from "@fern-api/python-ast";
import { OperatorType } from "@fern-api/python-ast/OperatorType";
import { AstNode } from "@fern-api/python-ast/core/AstNode";
import { Writer } from "@fern-api/python-ast/core/Writer";

import { PORTS_CLASS_NAME } from "src/constants";
import { WorkflowContext } from "src/context";
import { BaseNodeContext } from "src/context/node-context/base";
import { PortContext } from "src/context/port-context";
import { WorkflowDataNode, WorkflowEdge } from "src/types/vellum";

// Fern's Python AST types are not mutable, so we need to define our own types
// so that we can mutate the graph as we traverse through the edges.
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

export declare namespace GraphAttribute {
  interface Args {
    entrypointNodeEdges: WorkflowEdge[];
    entrypointNodeId: string;
    edgesByPortId: Map<string, WorkflowEdge[]>;
    workflowContext: WorkflowContext;
  }
}

export class GraphAttribute extends AstNode {
  private readonly workflowContext: WorkflowContext;
  private readonly edgesByPortId: Map<string, WorkflowEdge[]>;
  private readonly entrypointNodeEdges: WorkflowEdge[];
  private readonly entrypointNodeId: string;
  private readonly astNode: python.AstNode;

  public constructor({
    entrypointNodeEdges,
    entrypointNodeId,
    edgesByPortId,
    workflowContext,
  }: GraphAttribute.Args) {
    super();
    this.entrypointNodeEdges = entrypointNodeEdges;
    this.entrypointNodeId = entrypointNodeId;
    this.workflowContext = workflowContext;
    this.edgesByPortId = edgesByPortId;

    this.astNode = this.generateGraphAttribute();
  }

  /**
   * Generates a mutable graph AST.
   *
   * The algorithm we implement is a Breadth-First Search (BFS) that traverses through
   * the edges of the graph, starting from the entrypoint node.
   *
   * The core assumption made is that `graphMutableAst` is always a valid graph, and
   * adding a single edge to it will always produce another valid graph.
   */
  private generateGraphMutableAst(): GraphMutableAst {
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
          const newLhs = popSources(mutableAst.lhs);
          if (newLhs.type === "empty") {
            return mutableAst.rhs;
          }
          return {
            type: "right_shift",
            lhs: newLhs,
            rhs: mutableAst.rhs,
          };
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
          const newRhs = popTerminals(mutableAst.rhs);
          if (newRhs.type === "empty") {
            return mutableAst.lhs;
          }
          return {
            type: "right_shift",
            lhs: mutableAst.lhs,
            rhs: newRhs,
          };
        } else {
          return { type: "empty" };
        }
      };

      const addEdgeToGraph = (
        mutableAst: GraphMutableAst,
        graphSourceNode: BaseNodeContext<WorkflowDataNode> | null
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
          } else if (sourceNode == graphSourceNode) {
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
            const newSubAst = addEdgeToGraph(subAst, graphSourceNode);
            if (!newSubAst) {
              return { edgeAdded: false, value: subAst };
            }
            return { edgeAdded: true, value: newSubAst };
          });
          if (newSet.every(({ edgeAdded }) => !edgeAdded)) {
            if (sourceNode == graphSourceNode) {
              return {
                type: "set",
                values: [
                  mutableAst,
                  { type: "node_reference", reference: targetNode },
                ],
              };
            } else {
              return;
            }
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
          const newLhs = addEdgeToGraph(mutableAst.lhs, graphSourceNode);
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
          }

          if (
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
            return;
          }

          const lhsTerminals = getAstTerminals(mutableAst.lhs);
          const lhsTerminal = lhsTerminals[0];
          if (!lhsTerminal) {
            return;
          }

          const newRhs = addEdgeToGraph(mutableAst.rhs, lhsTerminal.reference);
          if (newRhs) {
            if (lhsTerminals.length > 1 && newRhs.type === "set") {
              throw new Error(
                "Adding an edge between two sets is not supported"
              );
            }
            return {
              type: "right_shift",
              lhs: mutableAst.lhs,
              rhs: newRhs,
            };
          }
        }

        return;
      };

      const newMutableAst = addEdgeToGraph(graphMutableAst, null);
      processedEdges.add(edge);

      if (!newMutableAst) {
        continue;
      }

      graphMutableAst = newMutableAst;
      targetNode.portContextsById.forEach((portContext) => {
        const edges = this.edgesByPortId.get(portContext.portId);
        edges?.forEach((edge) => {
          if (processedEdges.has(edge) || edgesQueue.includes(edge)) {
            return;
          }
          edgesQueue.push(edge);
        });
      });
    }

    return graphMutableAst;
  }

  /**
   * Translates our mutable graph AST into a Fern-native Python AST node.
   */
  private getGraphAttributeAstNode(mutableAst: GraphMutableAst): AstNode {
    if (mutableAst.type === "empty") {
      return python.TypeInstantiation.none();
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
        mutableAst.values.map((ast) => this.getGraphAttributeAstNode(ast))
      );
    }

    if (mutableAst.type === "right_shift") {
      const lhs = this.getGraphAttributeAstNode(mutableAst.lhs);
      const rhs = this.getGraphAttributeAstNode(mutableAst.rhs);
      if (!lhs || !rhs) {
        return python.TypeInstantiation.none();
      }
      return python.operator({
        operator: OperatorType.RightShift,
        lhs,
        rhs,
      });
    }

    return python.TypeInstantiation.none();
  }

  private generateGraphAttribute(): AstNode {
    const graphMutableAst = this.generateGraphMutableAst();
    const astNode = this.getGraphAttributeAstNode(graphMutableAst);
    this.inheritReferences(astNode);
    return astNode;
  }

  public write(writer: Writer): void {
    this.astNode.write(writer);
  }
}
