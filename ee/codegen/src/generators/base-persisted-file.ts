import { mkdir, writeFile } from "fs/promises";
import path, { join } from "path";

import { python } from "@fern-api/python-ast";
import { AstNode } from "@fern-api/python-ast/core/AstNode";
import { Writer } from "@fern-api/python-ast/core/Writer";

import { INIT_FILE_NAME } from "src/constants";
import { WorkflowContext } from "src/context";

export declare namespace BasePersistedFile {
  interface Args {
    workflowContext: WorkflowContext;
    isInitFile?: boolean;
  }
}

export abstract class BasePersistedFile extends AstNode {
  protected readonly workflowContext: WorkflowContext;
  protected readonly isInitFile: boolean;

  public constructor({ workflowContext, isInitFile }: BasePersistedFile.Args) {
    super();
    this.workflowContext = workflowContext;
    this.isInitFile = isInitFile ?? false;
  }

  protected abstract getModulePath(): string[];

  protected abstract getFileStatements(): AstNode[] | undefined;

  public write(writer: Writer): void {
    const fileStatements = this.getFileStatements();
    if (!fileStatements) {
      return;
    }

    const file = python.file({
      path: this.getModulePath(),
      isInitFile: this.isInitFile,
    });

    file.inheritReferences(this);
    fileStatements.forEach((statement) => file.addStatement(statement));

    file.write(writer);
  }

  public async persist(): Promise<void> {
    const absolutePathToModuleDirectory =
      this.workflowContext.absolutePathToOutputDirectory;

    const modulePath = this.getModulePath();

    let fileName: string;
    let filePath: string[];
    if (this.isInitFile) {
      fileName = INIT_FILE_NAME;
      filePath = modulePath;
    } else {
      fileName = modulePath[modulePath.length - 1] + ".py";
      filePath = modulePath.slice(0, -1);
    }

    const filepath = join(absolutePathToModuleDirectory, ...filePath, fileName);
    await mkdir(path.dirname(filepath), { recursive: true });

    const writer = new Writer();
    this.write(writer);

    let contents: string;
    try {
      contents = await writer.toStringFormatted({ line_width: 120 });
    } catch (error) {
      console.error("Error formatting file", error);
      contents = writer.toString();
    }

    await writeFile(filepath, contents);
  }
}
