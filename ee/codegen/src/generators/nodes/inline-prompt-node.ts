import { python } from "@fern-api/python-ast";
import { AstNode } from "@fern-api/python-ast/core/AstNode";

import { OUTPUTS_CLASS_NAME } from "src/constants";
import { InlinePromptNodeContext } from "src/context/node-context/inline-prompt-node";
import { BaseSingleFileNode } from "src/generators/nodes/bases/single-file-base";
import { PromptBlock } from "src/generators/prompt-block";
import { PromptParameters } from "src/generators/prompt-parameters-request";
import { InlinePromptNodeData, PromptNode } from "src/types/vellum";

export class InlinePromptNode extends BaseSingleFileNode<
  PromptNode,
  InlinePromptNodeContext
> {
  baseNodeClassName = "InlinePromptNode";
  baseNodeDisplayClassName = "BaseInlinePromptNodeDisplay";

  protected getNodeClassBodyStatements(): AstNode[] {
    const statements: AstNode[] = [];

    if (this.nodeData.data.variant !== "INLINE") {
      throw new Error(
        `InlinePromptNode only supports INLINE variant. Received ${this.nodeData.data.variant}`
      );
    }

    const nodeData: InlinePromptNodeData = this.nodeData.data;

    statements.push(
      python.field({
        name: "ml_model",
        initializer: python.TypeInstantiation.str(nodeData.mlModelName),
      })
    );
    statements.push(
      python.field({
        name: "blocks",
        initializer: python.TypeInstantiation.list(
          this.nodeData.data.execConfig.promptTemplateBlockData.blocks.map(
            (block) => {
              return new PromptBlock({
                promptBlock: block,
              });
            }
          )
        ),
      })
    );

    statements.push(
      python.field({
        name: "parameters",
        initializer: new PromptParameters({
          promptParametersRequest: this.nodeData.data.execConfig.parameters,
        }),
      })
    );

    statements.push(
      python.field({
        name: "prompt_inputs",
        initializer: python.TypeInstantiation.dict(
          Array.from(this.nodeInputsByKey.entries()).map(([key, value]) => ({
            key: python.TypeInstantiation.str(key),
            value: value,
          }))
        ),
      })
    );

    return statements;
  }

  protected getNodeDisplayClassBodyStatements(): AstNode[] {
    const statements: AstNode[] = [];

    statements.push(
      python.field({
        name: "label",
        initializer: python.TypeInstantiation.str(this.nodeData.data.label),
      }),
      python.field({
        name: "node_id",
        initializer: python.TypeInstantiation.uuid(this.nodeData.id),
      }),
      python.field({
        name: "output_id",
        initializer: python.TypeInstantiation.uuid(this.nodeData.data.outputId),
      }),
      python.field({
        name: "array_output_id",
        initializer: python.TypeInstantiation.uuid(
          this.nodeData.data.arrayOutputId
        ),
      }),
      python.field({
        name: "target_handle_id",
        initializer: python.TypeInstantiation.uuid(
          this.nodeData.data.targetHandleId
        ),
      }),
      python.field({
        name: "prompt_input_ids_by_name",
        initializer: python.TypeInstantiation.dict(
          this.nodeData.inputs.map((input) => ({
            key: python.TypeInstantiation.str(input.key),
            value: python.TypeInstantiation.uuid(input.id),
          }))
        ),
      })
    );

    return statements;
  }

  protected getOutputDisplay(): python.Field {
    // TODO: Handle error_output_id with try node
    // https://app.shortcut.com/vellum/story/5386/

    return python.field({
      name: "output_display",
      initializer: python.TypeInstantiation.dict([
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
                  this.nodeData.data.outputId
                ),
              }),
              python.methodArgument({
                name: "name",
                value: python.TypeInstantiation.str("text"),
              }),
            ],
          }),
        },
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
                  this.nodeData.data.arrayOutputId
                ),
              }),
              python.methodArgument({
                name: "name",
                value: python.TypeInstantiation.str("results"),
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
