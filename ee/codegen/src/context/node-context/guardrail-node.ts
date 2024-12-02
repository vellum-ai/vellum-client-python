import { MetricDefinitions as MetricDefinitionsClient } from "vellum-ai/api/resources/metricDefinitions/client/Client";

import { BaseNodeContext } from "./base";

import { PortContext } from "src/context/port-context";
import { GuardrailNode as GuardrailNodeType } from "src/types/vellum";

export class GuardrailNodeContext extends BaseNodeContext<GuardrailNodeType> {
  async getNodeOutputNamesById(): Promise<Record<string, string>> {
    const metricDefinitionId = this.nodeData.data.metricDefinitionId;
    const metricDefinitionsClient = new MetricDefinitionsClient({
      apiKey: this.workflowContext.vellumApiKey,
    });

    const metricDefinitionHistoryItem =
      await metricDefinitionsClient.metricDefinitionHistoryItemRetrieve(
        this.nodeData.data.releaseTag,
        metricDefinitionId
      );

    return metricDefinitionHistoryItem.outputVariables.reduce(
      (acc, variable) => {
        acc[variable.id] = variable.key;
        return acc;
      },
      {} as Record<string, string>
    );
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
