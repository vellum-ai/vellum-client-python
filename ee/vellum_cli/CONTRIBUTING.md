<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

- [Vellum CLI](#vellum-cli)
- [Updating this README](#updating-this-readme)
- [Development](#development)
  - [vellum pull](#vellum-pull)
    - [Step 1. Run the Codegen Service Locally](#step-1-run-the-codegen-service-locally)
    - [Step 2. Run the Vellum Webserver Locally](#step-2-run-the-vellum-webserver-locally)
    - [Step 3. Run the Vellum CLI Locally](#step-3-run-the-vellum-cli-locally)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

# Vellum CLI

This contribution guide is for the Vellum CLI, which is the command-line interface connecting Vellum SDKs to the Vellum application.

**Note:** This directory is _not_ accepting contributions from anyone besides Vellum employees. Please open an issue for feedback or feature requests.

# Updating this README

This README is generated using [doctoc](https://github.com/thlorenz/doctoc)

To install doctoc, run `npm install -g doctoc`

To update the table of contents, run `doctoc README.md`

# Development

## vellum pull

If you want to run `vellum pull` locally end to end, here are the steps you'll need to follow.

### Step 1. Run the Codegen Service Locally

- Pull down the private `vellum-ai/codegen-service` repo [here](https://github.com/vellum-ai/codegen-service)
- Follow its README to run the service locally. This will spin up a local webserver running on `localhost:5111`.
- By default, when you run that service, it'll use the latest published `@vellum-ai/vellum-codegen` npm package.
  However, you'll often want to instead point it to the local version defined here in this repo under the `codegen/`
  directory (which is the source of where @vellum-ai/vellum-codegen is published from). The README in the
  codegen-service repo should show you how to do that.

### Step 2. Run the Vellum Webserver Locally

- Pull down the private `vellum-ai/vellum` repo [here](https://github.com/vellum-ai/vellum)
- Follow its README to set up the Vellum backend
- Run `make run-backend-dev`. This will start up the Vellum backend on `localhost:8000` and have it point to the
  local codegen-service running on `localhost:5111`.

### Step 3. Run the Vellum CLI Locally

- From within the root of this repo, run `pip install -e .` to install the Vellum CLI locally.
- Ensure you have a valid workflow config in your `pyproject.toml` file. For example:
  ```toml
  [[tool.vellum.workflows]]
  module = "examples.basic_rag_workflow"
  workflow_sandbox_id = "<your-workflow-sandbox-id>"
  ```
- Ensure you have an API key stored in your `.env` file:
  ```
  VELLUM_API_KEY="<your-api-key>"
  ```
- Run the cli command and point it to the local Vellum backend running on `localhost:8000`. For example:
  ```
  VELLUM_API_URL="http://localhost:8000" vellum pull examples.basic_rag_workflow
  ```
