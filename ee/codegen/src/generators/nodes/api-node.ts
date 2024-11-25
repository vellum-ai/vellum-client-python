import { python } from "@fern-api/python-ast";
import { AstNode } from "@fern-api/python-ast/core/AstNode";
import { isNil } from "lodash";

import { ApiNodeContext } from "src/context/node-context/api-node";
import { BaseSingleFileNode } from "src/generators/nodes/bases/single-file-base";
import { ApiNode as ApiNodeType } from "src/types/vellum";

export class ApiNode extends BaseSingleFileNode<ApiNodeType, ApiNodeContext> {
  baseNodeClassName = "ApiNode";
  baseNodeDisplayClassName = "BaseAPINodeDisplay";

  getNodeClassBodyStatements(): AstNode[] {
    const statements: AstNode[] = [];

    const urlInput = this.nodeInputsByKey.get("url");
    if (!urlInput) {
      throw new Error('Node input "url" is required but not found.');
    }

    const methodInput = this.nodeInputsByKey.get("method");
    if (!methodInput) {
      throw new Error('Node input "method" is required but not found.');
    }

    return statements;
  }

  getNodeDisplayClassBodyStatements(): AstNode[] {
    const statements: AstNode[] = [];

    if (!isNil(this.nodeData.data.urlInputId)) {
      statements.push(
        python.field({
          name: "url_input_id",
          initializer: python.TypeInstantiation.uuid(
            this.nodeData.data.urlInputId
          ),
        })
      );
    }

    if (!isNil(this.nodeData.data.methodInputId)) {
      statements.push(
        python.field({
          name: "method_input_id",
          initializer: python.TypeInstantiation.uuid(
            this.nodeData.data.methodInputId
          ),
        })
      );
    }

    if (!isNil(this.nodeData.data.bodyInputId)) {
      statements.push(
        python.field({
          name: "body_input_id",
          initializer: python.TypeInstantiation.uuid(
            this.nodeData.data.bodyInputId
          ),
        })
      );
    }

    if (!isNil(this.nodeData.data.authorizationTypeInputId)) {
      statements.push(
        python.field({
          name: "authorization_type_input_id",
          initializer: python.TypeInstantiation.uuid(
            this.nodeData.data.authorizationTypeInputId
          ),
        })
      );
    }

    if (!isNil(this.nodeData.data.bearerTokenValueInputId)) {
      statements.push(
        python.field({
          name: "bearer_token_value_input_id",
          initializer: python.TypeInstantiation.uuid(
            this.nodeData.data.bearerTokenValueInputId
          ),
        })
      );
    }

    if (!isNil(this.nodeData.data.apiKeyHeaderKeyInputId)) {
      statements.push(
        python.field({
          name: "api_key_header_key_input_id",
          initializer: python.TypeInstantiation.uuid(
            this.nodeData.data.apiKeyHeaderKeyInputId
          ),
        })
      );
    }

    if (!isNil(this.nodeData.data.apiKeyHeaderValueInputId)) {
      statements.push(
        python.field({
          name: "api_key_header_value_input_id",
          initializer: python.TypeInstantiation.uuid(
            this.nodeData.data.apiKeyHeaderValueInputId
          ),
        })
      );
    }

    if (!isNil(this.nodeData.data.textOutputId)) {
      statements.push(
        python.field({
          name: "text_output_id",
          initializer: python.TypeInstantiation.uuid(
            this.nodeData.data.textOutputId
          ),
        })
      );
    }

    if (!isNil(this.nodeData.data.jsonOutputId)) {
      statements.push(
        python.field({
          name: "json_output_id",
          initializer: python.TypeInstantiation.uuid(
            this.nodeData.data.jsonOutputId
          ),
        })
      );
    }

    if (!isNil(this.nodeData.data.statusCodeOutputId)) {
      statements.push(
        python.field({
          name: "status_code_output_id",
          initializer: python.TypeInstantiation.uuid(
            this.nodeData.data.statusCodeOutputId
          ),
        })
      );
    }

    if (!isNil(this.nodeData.data.additionalHeaders)) {
      statements.push(
        python.field({
          name: "additional_header_key_input_ids",
          initializer: python.TypeInstantiation.dict(
            this.nodeData.data.additionalHeaders.map((header) => {
              const nodeInput = this.nodeData.inputs.find(
                (nodeInput) => nodeInput.id === header.headerValueInputId
              );

              if (!nodeInput) {
                throw new Error(
                  `Node input with ID ${header.headerValueInputId} not found`
                );
              }

              return {
                key: python.TypeInstantiation.str(nodeInput.key),
                value: python.TypeInstantiation.uuid(nodeInput.id),
              };
            })
          ),
        })
      );
    }

    if (!isNil(this.nodeData.data.additionalHeaders)) {
      statements.push(
        python.field({
          name: "additional_header_value_input_ids",
          initializer: python.TypeInstantiation.dict(
            this.nodeData.data.additionalHeaders.map((header) => {
              const nodeInput = this.nodeData.inputs.find(
                (nodeInput) => nodeInput.id === header.headerValueInputId
              );

              if (!nodeInput) {
                throw new Error(
                  `Node input with ID ${header.headerValueInputId} not found`
                );
              }

              return {
                key: python.TypeInstantiation.str(nodeInput.key),
                value: python.TypeInstantiation.uuid(nodeInput.id),
              };
            })
          ),
        })
      );
    }

    return statements;
  }

  getErrorOutputId(): string | undefined {
    return this.nodeData.data.errorOutputId;
  }
}
