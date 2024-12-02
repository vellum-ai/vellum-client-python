import { MetricDefinitions as MetricDefinitionsClient } from "vellum-ai/api/resources/metricDefinitions/client/Client";

import { BaseNodeContext } from "./base";

import { PortContext } from "src/context/port-context";
import { GuardrailNode as GuardrailNodeType } from "src/types/vellum";

export class GuardrailNodeContext extends BaseNodeContext<GuardrailNodeType> {
  getNodeOutputNamesById(): Record<string, string> {
    const metricDefinitionId = this.nodeData.data.metricDefinitionId;
    return (async () => {
      const metricDefinitionHistoryItem = await new MetricDefinitionsClient({
        apiKey: this.workflowContext.vellumApiKey,
      }).metricDefinitionHistoryItemRetrieve(
        this.nodeData.data.releaseTag,
        metricDefinitionId
      );
      const score = metricDefinitionHistoryItem.outputVariables.find(
        (variable) => variable.key === "score"
      );
      return score
        ? {
            [score.id]: "score",
          }
        : {};
    })() as unknown as Record<string, string>;
  }

  createPortContexts(): PortContext[] {
    return [
      new PortContext({
        workflowContext: this.workflowContext,
        nodeContext: this,
        portId: this.nodeData.data.sourceHandleId,
      }),
    ];
  }
}
