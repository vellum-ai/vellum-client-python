import { python } from "@fern-api/python-ast";
import * as Vellum from "vellum-ai/api";

import { VELLUM_CLIENT_MODULE_PATH } from "src/constants";
import { WorkflowContext } from "src/context";
import { assertUnreachable } from "src/utils/typing";

export function getVellumVariablePrimitiveType({
  type,
  workflowContext,
}: {
  type: Vellum.VellumVariableType;
  workflowContext: WorkflowContext;
}): python.Type {
  switch (type) {
    case "STRING":
      return python.Type.str();
    case "NUMBER":
      return python.Type.float();
    case "JSON":
      return python.Type.reference(
        python.reference({
          name: "Json",
          modulePath: [
            ...workflowContext.sdkModulePathNames.WORKFLOWS_MODULE_PATH,
            "types",
          ],
        })
      );
    case "CHAT_HISTORY":
      return python.Type.list(
        python.Type.reference(
          python.reference({
            name: "ChatMessage",
            modulePath: VELLUM_CLIENT_MODULE_PATH,
          })
        )
      );
    case "SEARCH_RESULTS":
      return python.Type.list(
        python.Type.reference(
          python.reference({
            name: "SearchResult",
            modulePath: VELLUM_CLIENT_MODULE_PATH,
          })
        )
      );
    case "ERROR":
      return python.Type.reference(
        python.reference({
          name: "VellumError",
          modulePath: VELLUM_CLIENT_MODULE_PATH,
        })
      );
    case "ARRAY":
      return python.Type.list(
        python.Type.reference(
          python.reference({
            name: "VellumValue",
            modulePath: VELLUM_CLIENT_MODULE_PATH,
          })
        )
      );
    case "FUNCTION_CALL":
      return python.Type.reference(
        python.reference({
          name: "FunctionCall",
          modulePath: VELLUM_CLIENT_MODULE_PATH,
        })
      );
    case "IMAGE":
      return python.Type.reference(
        python.reference({
          name: "VellumImage",
          modulePath: VELLUM_CLIENT_MODULE_PATH,
        })
      );
    case "AUDIO":
      return python.Type.reference(
        python.reference({
          name: "VellumAudio",
          modulePath: VELLUM_CLIENT_MODULE_PATH,
        })
      );
    case "NULL":
      return python.Type.none();
    default: {
      assertUnreachable(vellumVariableType);
    }
  }
}
