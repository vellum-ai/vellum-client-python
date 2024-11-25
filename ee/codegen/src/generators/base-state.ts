import { python } from "@fern-api/python-ast";

import { WorkflowContext } from "src/context";

export declare namespace BaseState {
  export interface Args {
    workflowContext: WorkflowContext;
  }
}

export class BaseState extends python.Reference {
  public constructor(args: BaseState.Args) {
    super({
      name: "BaseState",
      modulePath: args.workflowContext.sdkModulePathNames.STATE_MODULE_PATH,
    });
  }
}
