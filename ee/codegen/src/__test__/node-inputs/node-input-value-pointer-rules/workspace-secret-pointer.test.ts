import { Writer } from "@fern-api/python-ast/core/Writer";

import { workflowContextFactory } from "src/__test__/helpers";
import { WorkspaceSecretPointerRule } from "src/generators/node-inputs/node-input-value-pointer-rules/workspace-secret-pointer";

describe("WorkspaceSecretPointer", () => {
  let writer: Writer;

  beforeEach(() => {
    writer = new Writer();
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  it("should generate correct Python code", async () => {
    const workflowContext = workflowContextFactory();

    const workspaceSecretPointer = new WorkspaceSecretPointerRule({
      workflowContext: workflowContext,
      nodeInputValuePointerRule: {
        type: "WORKSPACE_SECRET",
        data: {
          type: "STRING",
          workspaceSecretId: "MY_SECRET",
        },
      },
    });

    workspaceSecretPointer.write(writer);
    expect(await writer.toStringFormatted()).toMatchSnapshot();
  });

  it("should handle the the case where the workspace secret isn't yet specified", async () => {
    const workflowContext = workflowContextFactory();

    const workspaceSecretPointer = new WorkspaceSecretPointerRule({
      workflowContext: workflowContext,
      nodeInputValuePointerRule: {
        type: "WORKSPACE_SECRET",
        data: {
          type: "STRING",
          workspaceSecretId: undefined,
        },
      },
    });

    workspaceSecretPointer.write(writer);
    expect(await writer.toStringFormatted()).toMatchSnapshot();
  });
});
