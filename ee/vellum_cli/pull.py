import io
import os
from pathlib import Path
import zipfile
from typing import Optional

from dotenv import load_dotenv

from vellum.workflows.vellum_client import create_vellum_client
from vellum_cli.config import load_vellum_cli_config
from vellum_cli.logger import load_cli_logger


def pull_command(
    module: Optional[str], legacy_module: Optional[bool] = None, include_json: Optional[bool] = None
) -> None:
    load_dotenv()
    logger = load_cli_logger()
    config = load_vellum_cli_config()

    if not config.workflows:
        raise ValueError("No Workflows found in project to pull.")

    if len(config.workflows) > 1 and not module:
        raise ValueError("Multiple workflows found in project to pull. Pulling only a single workflow is supported.")

    workflow_config = (
        next((w for w in config.workflows if w.module == module), None) if module else config.workflows[0]
    )
    if workflow_config is None:
        raise ValueError(f"No workflow config for '{module}' found in project to push.")

    if not workflow_config.workflow_sandbox_id:
        raise ValueError("No workflow sandbox ID found in project to pull from.")

    logger.info(f"Pulling workflow into {workflow_config.module}")
    client = create_vellum_client()
    query_parameters = {}
    if legacy_module:
        query_parameters["legacyModule"] = legacy_module
    if include_json:
        query_parameters["include_json"] = include_json

    response = client.workflows.pull(
        workflow_config.workflow_sandbox_id,
        request_options={"additional_query_parameters": query_parameters},
    )

    zip_bytes = b"".join(response)
    zip_buffer = io.BytesIO(zip_bytes)

    target_dir = os.path.join(os.getcwd(), *workflow_config.module.split("."))
    with zipfile.ZipFile(zip_buffer) as zip_file:
        # Delete files in target_dir that aren't in the zip file
        if os.path.exists(target_dir):
            ignore_patterns = (
                workflow_config.ignore
                if isinstance(workflow_config.ignore, list)
                else [workflow_config.ignore] if isinstance(workflow_config.ignore, str) else []
            )
            existing_files = []
            for root, _, files in os.walk(target_dir):
                for file in files:
                    rel_path = os.path.relpath(os.path.join(root, file), target_dir)
                    existing_files.append(rel_path)

            for file in existing_files:
                if any(Path(file).match(ignore_pattern) for ignore_pattern in ignore_patterns):
                    continue

                if file not in zip_file.namelist():
                    file_path = os.path.join(target_dir, file)
                    logger.info(f"Deleting {file_path}...")
                    os.remove(file_path)

        for file_name in zip_file.namelist():
            target_file = os.path.join(target_dir, file_name)
            os.makedirs(os.path.dirname(target_file), exist_ok=True)
            with zip_file.open(file_name) as source, open(target_file, "w") as target:
                logger.info(f"Writing to {target_file}...")
                target.write(source.read().decode("utf-8"))

    if include_json:
        logger.warning("The pulled JSON representation of the Workflow should be used for debugging purposely only. Its schema should be considered unstable and subject to change at any time.")

    logger.info(f"Successfully pulled Workflow into {workflow_config.module}")
