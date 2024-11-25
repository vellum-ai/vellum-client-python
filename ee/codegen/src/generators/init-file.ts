import { AstNode } from "@fern-api/python-ast/core/AstNode";

import { BasePersistedFile } from "./base-persisted-file";

export declare namespace InitFile {
  interface Args extends BasePersistedFile.Args {
    modulePath: string[] | Readonly<string[]>;
    statements?: AstNode[];
  }
}

export class InitFile extends BasePersistedFile {
  private readonly modulePath: string[];
  private readonly statements: AstNode[];

  public constructor({
    workflowContext,
    modulePath,
    statements,
  }: InitFile.Args) {
    super({ workflowContext, isInitFile: true });
    this.modulePath = [...modulePath];
    this.statements = statements ?? [];
    this.statements.forEach((statement) => this.inheritReferences(statement));
  }

  getModulePath(): string[] {
    return this.modulePath;
  }

  public getFileStatements() {
    return this.statements;
  }
}
