import { python } from "@fern-api/python-ast";
import { ClassInstantiation } from "@fern-api/python-ast/ClassInstantiation";
import { AstNode } from "@fern-api/python-ast/core/AstNode";

import { OUTPUTS_CLASS_NAME, VELLUM_CLIENT_MODULE_PATH } from "src/constants";
import { TextSearchNodeContext } from "src/context/node-context/text-search-node";
import { BaseSingleFileNode } from "src/generators/nodes/bases/single-file-base";
import { SearchNode as SearchNodeType } from "src/types/vellum";

export class SearchNode extends BaseSingleFileNode<
  SearchNodeType,
  TextSearchNodeContext
> {
  baseNodeClassName = "SearchNode";
  baseNodeDisplayClassName = "BaseSearchNodeDisplay";

  getNodeClassBodyStatements(): AstNode[] {
    const bodyStatements: AstNode[] = [];

    bodyStatements.push(
      python.field({
        name: "query",
        initializer: this.getNodeInputByName("query"),
      })
    );

    bodyStatements.push(
      python.field({
        name: "document_index",
        initializer: this.getNodeInputByName("document_index_id"),
      })
    );

    const options = python.instantiateClass({
      classReference: python.reference({
        name: "SearchRequestOptionsRequest",
        modulePath: VELLUM_CLIENT_MODULE_PATH,
      }),
      arguments_: [
        python.methodArgument({
          name: "limit",
          value:
            this.findNodeInputByName("limit") ??
            python.TypeInstantiation.none(),
        }),
        python.methodArgument({
          name: "weights",
          value: this.getSearchWeightsRequest(),
        }),
        python.methodArgument({
          name: "result_merging",
          value: this.getResultMerging(),
        }),
        python.methodArgument({
          name: "filters",
          value: this.searchFiltersConfig(),
        }),
      ],
    });

    bodyStatements.push(
      python.field({
        name: "options",
        initializer: options,
      })
    );

    bodyStatements.push(
      python.field({
        name: "chunk_separator",
        initializer: this.getNodeInputByName("separator"),
      })
    );

    return bodyStatements;
  }

  private getSearchWeightsRequest(): ClassInstantiation {
    const weightsRule =
      this.findNodeInputByName("weights")?.nodeInputData?.value.rules[0];
    if (!weightsRule || weightsRule.type !== "CONSTANT_VALUE") {
      throw new Error("weights input is required");
    }

    // TODO: Determine what we want to cast JSON values to
    //  https://app.shortcut.com/vellum/story/5459
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    const { semantic_similarity, keywords } = weightsRule.data.value as Record<
      string,
      unknown
    >;
    if (typeof semantic_similarity !== "number") {
      throw new Error("semantic_similarity weight must be a number");
    }

    if (typeof keywords !== "number") {
      throw new Error("keywords weight must be a number");
    }

    const searchWeightsRequest = python.instantiateClass({
      classReference: python.reference({
        name: "SearchWeightsRequest",
        modulePath: VELLUM_CLIENT_MODULE_PATH,
      }),
      arguments_: [
        python.methodArgument({
          name: "semantic_similarity",
          value: python.TypeInstantiation.float(semantic_similarity),
        }),
        python.methodArgument({
          name: "keywords",
          value: python.TypeInstantiation.float(keywords),
        }),
      ],
    });

    return searchWeightsRequest;
  }

  private getResultMerging(): ClassInstantiation {
    const resultMergingRule = this.findNodeInputByName("result_merging_enabled")
      ?.nodeInputData?.value.rules[0];
    if (!resultMergingRule || resultMergingRule.type !== "CONSTANT_VALUE") {
      throw new Error("result_merging_enabled input is required");
    }

    const resultMergingEnabled = resultMergingRule.data.value;
    if (typeof resultMergingEnabled !== "string") {
      throw new Error("result_merging_enabled must be a boolean");
    }

    return python.instantiateClass({
      classReference: python.reference({
        name: "SearchResultMergingRequest",
        modulePath: VELLUM_CLIENT_MODULE_PATH,
      }),
      arguments_: [
        python.methodArgument({
          name: "enabled",
          value: python.TypeInstantiation.bool(Boolean(resultMergingEnabled)),
        }),
      ],
    });
  }

  private searchFiltersConfig(): ClassInstantiation {
    return python.instantiateClass({
      classReference: python.reference({
        name: "SearchFiltersRequest",
        modulePath: VELLUM_CLIENT_MODULE_PATH,
      }),
      arguments_: [
        python.methodArgument({
          name: "external_ids",
          value:
            this.findNodeInputByName("external_id_filters") ??
            python.TypeInstantiation.none(),
        }),
        // TODO: Add support for our new style metadata filtering where there might be dynamic node inputs on
        //  either side of an operator.
        //  https://app.shortcut.com/vellum/story/5150
        python.methodArgument({
          name: "metadata",
          value:
            this.findNodeInputByName("metadata_filters") ??
            python.TypeInstantiation.none(),
        }),
      ],
    });
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

  protected getOutputDisplay(): python.Field {
    return python.field({
      name: "output_display",
      initializer: python.TypeInstantiation.dict([
        {
          key: python.reference({
            name: this.nodeContext.nodeClassName,
            modulePath: this.nodeContext.nodeModulePath,
            attribute: [OUTPUTS_CLASS_NAME, "results"],
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
                value: python.TypeInstantiation.uuid(
                  this.nodeData.data.resultsOutputId
                ),
              }),
              python.methodArgument({
                name: "name",
                value: python.TypeInstantiation.str("results"),
              }),
            ],
          }),
        },
        {
          key: python.reference({
            name: this.nodeContext.nodeClassName,
            modulePath: this.nodeContext.nodeModulePath,
            attribute: [OUTPUTS_CLASS_NAME, "text"],
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
                value: python.TypeInstantiation.uuid(
                  this.nodeData.data.textOutputId
                ),
              }),
              python.methodArgument({
                name: "name",
                value: python.TypeInstantiation.str("text"),
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
