import { mkdir, rm } from "fs/promises";
import * as fs from "node:fs";
import { join } from "path";

import { difference } from "lodash";
import { expect } from "vitest";

import {
  getAllFilesInDir,
  getFixturesForProjectTest,
} from "./helpers/fixtures";
import { makeTempDir } from "./helpers/temp-dir";

import { SpyMocks } from "src/__test__/utils/SpyMocks";
import { WorkflowProjectGenerator } from "src/project";
import { NodeAttributeGenerationError } from "src/generators/errors";

describe("WorkflowProjectGenerator", () => {
  let tempDir: string;

  beforeEach(async () => {
    tempDir = makeTempDir("project-test");
    await mkdir(tempDir, { recursive: true });
  });

  afterEach(async () => {
    await rm(tempDir, { recursive: true, force: true });
  });

  describe("generateCode", () => {
    const excludeFilesAtPaths: RegExp[] = [/\.pyc$/];
    const ignoreContentsOfFilesAtPaths: RegExp[] = [];
    const fixtureMocks = {
      simple_guard_rail_node: SpyMocks.createMetricDefinitionMock(),
      faa_q_and_a_bot: SpyMocks.createWorkflowDeploymentsMock(),
    };

    it.each(
      getFixturesForProjectTest({
        includeFixtures: [
          "simple_search_node",
          "simple_inline_subworkflow_node",
          "simple_guardrail_node",
          "simple_prompt_node",
          "simple_map_node",
          "simple_code_execution_node",
          "simple_conditional_node",
          "simple_templating_node",
          "simple_error_node",
          "simple_merge_node",
          "simple_api_node",
        ],
        fixtureMocks: fixtureMocks,
      })
    )(
      "should correctly generate code for fixture $fixtureName",
      async ({ displayFile, codeDir }) => {
        const displayData: unknown = JSON.parse(
          fs.readFileSync(displayFile, "utf-8")
        );

        const project = new WorkflowProjectGenerator({
          absolutePathToOutputDirectory: tempDir,
          workflowVersionExecConfigData: displayData,
          moduleName: "code",
          vellumApiKey: "<TEST_API_KEY>",
        });

        await project.generateCode();

        const generatedFiles = getAllFilesInDir(
          join(tempDir, project.getModuleName())
        );
        const expectedFiles = getAllFilesInDir(codeDir, excludeFilesAtPaths);

        const extraFilePaths = difference(
          Object.keys(generatedFiles),
          Object.keys(expectedFiles)
        );
        const extraFiles = extraFilePaths.map((path) => generatedFiles[path]);
        expect(extraFiles.length, `Found extra file(s): ${extraFiles}`).toBe(0);

        for (const [
          expectedRelativePath,
          expectedAbsolutePath,
        ] of Object.entries(expectedFiles)) {
          const generatedAbsolutePath = generatedFiles[expectedRelativePath];

          if (!generatedAbsolutePath) {
            throw new Error(
              `Expected to have generated a file at the path: ${expectedRelativePath}`
            );
          }

          if (
            ignoreContentsOfFilesAtPaths.some((regex) =>
              regex.test(expectedRelativePath)
            )
          ) {
            continue;
          }

          const generatedFileContents = fs.readFileSync(
            generatedAbsolutePath,
            "utf-8"
          );

          expect(generatedFileContents).toMatchFileSnapshot(
            expectedAbsolutePath,
            `File contents don't match snapshot: ${expectedRelativePath}`
          );
        }
      }
    );

    it("should generate code even if a node fails to generate", async () => {
      const displayData = {};
      const project = new WorkflowProjectGenerator({
        absolutePathToOutputDirectory: tempDir,
        workflowVersionExecConfigData: displayData,
        moduleName: "code",
        vellumApiKey: "<TEST_API_KEY>",
      });

      await project.generateCode();

      expect(
        fs.existsSync(join(tempDir, project.getModuleName(), "workflow.py"))
      ).toBe(true);
      expect(
        fs.existsSync(join(tempDir, project.getModuleName(), "nodes"))
      ).toBe(true);
      expect(
        fs.existsSync(
          join(tempDir, project.getModuleName(), "nodes", "bad_node.py")
        )
      ).toBe(false);

      const errorLogPath = join(tempDir, project.getModuleName(), "error.log");
      expect(fs.existsSync(errorLogPath)).toBe(true);
      expect(fs.readFileSync(errorLogPath, "utf-8")).toBe(`\
Encountered 1 error(s) while generating code:

Failed to generate node "BadNode": Failed to find output "foo" in node "Bar"
`);
    });
    });

    it("should fail to generate code if a node fails in strict mode", async () => {
      const displayData = {};
      const project = new WorkflowProjectGenerator({
        absolutePathToOutputDirectory: tempDir,
        workflowVersionExecConfigData: displayData,
        moduleName: "code",
        vellumApiKey: "<TEST_API_KEY>",
        strict: true,
      });

      expect(project.generateCode()).rejects.toThrow(
        new NodeAttributeGenerationError("test")
      );
    });
  });
});
