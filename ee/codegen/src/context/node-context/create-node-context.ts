import { BaseNodeContext } from "./base";
import { GuardrailNodeContext } from "./guardrail-node";
import { InlineSubworkflowNodeContext } from "./inline-subworkflow-node";
import { TextSearchNodeContext } from "./text-search-node";

import { ApiNodeContext } from "src/context/node-context/api-node";
import { CodeExecutionContext } from "src/context/node-context/code-execution-node";
import { ConditionalNodeContext } from "src/context/node-context/conditional-node";
import { ErrorNodeContext } from "src/context/node-context/error-node";
import { FinalOutputNodeContext } from "src/context/node-context/final-output-node";
import { GenericNodeContext } from "src/context/node-context/generic-node";
import { InlinePromptNodeContext } from "src/context/node-context/inline-prompt-node";
import { MapNodeContext } from "src/context/node-context/map-node";
import { MergeNodeContext } from "src/context/node-context/merge-node";
import { NoteNodeContext } from "src/context/node-context/note-node";
import { TemplatingNodeContext } from "src/context/node-context/templating-node";
import {
  InlinePromptNodeData,
  LegacyPromptNodeData,
  WorkflowDataNode,
  WorkflowNodeType,
} from "src/types/vellum";
import { assertUnreachable } from "src/utils/typing";

export function createNodeContext(
  args: BaseNodeContext.Args<WorkflowDataNode>
): BaseNodeContext<WorkflowDataNode> {
  const nodeData = args.nodeData;
  switch (nodeData.type) {
    case WorkflowNodeType.SEARCH: {
      const searchNodeData = nodeData;
      return new TextSearchNodeContext({
        ...args,
        nodeData: searchNodeData,
      });
    }
    case WorkflowNodeType.SUBWORKFLOW: {
      const subworkflowNodeData = nodeData;

      const subworkflowVariant = subworkflowNodeData.data.variant;
      switch (subworkflowVariant) {
        case "INLINE": {
          return new InlineSubworkflowNodeContext({
            ...args,
            nodeData: subworkflowNodeData,
          });
        }
        case "DEPLOYMENT": {
          // TODO: https://app.shortcut.com/vellum/story/5269
          throw new Error(`DEPLOYMENT variant not yet supported`);
        }
        default: {
          assertUnreachable(subworkflowVariant);
        }
      }
      break;
    }
    case WorkflowNodeType.MAP: {
      const mapNodeData = nodeData;
      const variant = mapNodeData.data.variant;
      if (variant === "INLINE") {
        return new MapNodeContext({
          ...args,
          nodeData: mapNodeData,
        });
      } else {
        throw new Error(
          `MapNode only supports INLINE variant. Received: ${variant}`
        );
      }
    }
    case WorkflowNodeType.METRIC: {
      const guardrailNodeData = nodeData;
      return new GuardrailNodeContext({
        ...args,
        nodeData: guardrailNodeData,
      });
    }
    case WorkflowNodeType.CODE_EXECUTION: {
      const codeExecutionNodeData = nodeData;
      return new CodeExecutionContext({
        ...args,
        nodeData: codeExecutionNodeData,
      });
    }
    case WorkflowNodeType.PROMPT: {
      const promptNodeData = nodeData;

      const promptVariant = promptNodeData.data.variant;
      switch (promptVariant) {
        case "INLINE": {
          return new InlinePromptNodeContext({
            ...args,
            nodeData: promptNodeData,
          });
        }
        case "LEGACY": {
          // In the legacy case, we simply convert from LEGACY to INLINE on the fly.
          const legacyNodeData: LegacyPromptNodeData = promptNodeData.data;

          const promptVersionData =
            legacyNodeData.sandboxRoutingConfig.promptVersionData;
          if (!promptVersionData) {
            throw new Error(`Prompt version data not found`);
          }

          const inlinePromptNodeData: InlinePromptNodeData = {
            ...legacyNodeData,
            variant: "INLINE",
            // TODO: Make sure we can operate on mlModelName vs mlModelToWorkspaceId interchangeably
            // https://app.shortcut.com/vellum/story/5591
            mlModelName: promptVersionData.mlModelToWorkspaceId,
            execConfig: promptVersionData.execConfig,
          };

          return new InlinePromptNodeContext({
            ...args,
            nodeData: { ...promptNodeData, data: inlinePromptNodeData },
          });
        }
        case "DEPLOYMENT": {
          // TODO: https://app.shortcut.com/vellum/story/5261
          throw new Error(`DEPLOYMENT variant not yet supported`);
        }
        default: {
          assertUnreachable(promptVariant);
        }
      }
      break;
    }
    case WorkflowNodeType.TEMPLATING: {
      const templatingNodeData = nodeData;
      return new TemplatingNodeContext({
        ...args,
        nodeData: templatingNodeData,
      });
    }
    case WorkflowNodeType.CONDITIONAL: {
      const conditionalNodeData = nodeData;
      return new ConditionalNodeContext({
        ...args,
        nodeData: conditionalNodeData,
      });
    }
    case WorkflowNodeType.API: {
      const apiNodeData = nodeData;
      return new ApiNodeContext({
        ...args,
        nodeData: apiNodeData,
      });
    }
    case WorkflowNodeType.TERMINAL: {
      const terminalNodeData = nodeData;
      return new FinalOutputNodeContext({
        ...args,
        nodeData: terminalNodeData,
      });
    }
    case WorkflowNodeType.MERGE: {
      const mergeNodeData = nodeData;
      return new MergeNodeContext({
        ...args,
        nodeData: mergeNodeData,
      });
    }
    case WorkflowNodeType.ERROR: {
      const errorNodeData = nodeData;
      return new ErrorNodeContext({
        ...args,
        nodeData: errorNodeData,
      });
    }
    case WorkflowNodeType.NOTE: {
      const noteNodeData = nodeData;
      return new NoteNodeContext({
        ...args,
        nodeData: noteNodeData,
      });
    }
    case WorkflowNodeType.GENERIC: {
      const genericNodeData = nodeData;
      return new GenericNodeContext({
        ...args,
        nodeData: genericNodeData,
      });
    }
    default:
      throw new Error(`Unsupported node type: ${args.nodeData.type}`);
  }
}
