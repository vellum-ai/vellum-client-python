import { MetricDefinitionHistoryItem } from "vellum-ai/api";
import { MetricDefinitions as MetricDefinitionsClient } from "vellum-ai/api/resources/metricDefinitions/client/Client";
import { MockInstance } from "vitest";

export class SpyMocks {
  static createMetricDefinitionMock(): MockInstance {
    return vi
      .spyOn(
        MetricDefinitionsClient.prototype,
        "metricDefinitionHistoryItemRetrieve"
      )
      .mockResolvedValue({
        id: "mocked-metric-output-id",
        label: "mocked-metric-output-label",
        name: "mocked-metric-output-name",
        description: "mocked-metric-output-description",
        outputVariables: [
          {
            id: "0e455862-ccc4-47a4-a9a5-061fadc94fd6",
            key: "score",
            type: "NUMBER",
          },
        ],
      } as MetricDefinitionHistoryItem);
  }
}
