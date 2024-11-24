from dataclasses import field
import json
import os
from uuid import UUID
from typing import Dict, List, Literal, Optional, Union

import tomli

from vellum.core.pydantic_utilities import UniversalBaseModel

from vellum.workflows.state.encoder import DefaultStateEncoder

LOCKFILE_PATH = "vellum.lock.json"
PYPROJECT_TOML_PATH = "pyproject.toml"


class WorkflowDeploymentConfig(UniversalBaseModel):
    id: Optional[UUID] = None
    label: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    release_tags: Optional[List[str]] = None


class WorkflowConfig(UniversalBaseModel):
    module: str
    workflow_sandbox_id: Optional[str] = None
    ignore: Optional[Union[str, List[str]]] = None
    deployments: List[WorkflowDeploymentConfig] = field(default_factory=list)

    def merge(self, other: "WorkflowConfig") -> "WorkflowConfig":
        return WorkflowConfig(
            module=self.module,
            workflow_sandbox_id=self.workflow_sandbox_id or other.workflow_sandbox_id,
            ignore=self.ignore or other.ignore,
        )


class VellumCliConfig(UniversalBaseModel):
    version: Literal["1.0"] = "1.0"
    workflows: List[WorkflowConfig] = field(default_factory=list)

    def save(self) -> None:
        lockfile_path = os.path.join(os.getcwd(), LOCKFILE_PATH)
        with open(lockfile_path, "w") as f:
            json.dump(self.model_dump(), f, indent=2, cls=DefaultStateEncoder)

    def merge(self, other: "VellumCliConfig") -> "VellumCliConfig":
        if other.version != self.version:
            raise ValueError("Lockfile version mismatch")

        self_workflow_by_module = {workflow.module: workflow for workflow in self.workflows}
        other_workflow_by_module = {workflow.module: workflow for workflow in other.workflows}
        all_modules = sorted(set(self_workflow_by_module.keys()).union(set(other_workflow_by_module.keys())))
        merged_workflows = []
        for module in all_modules:
            self_workflow = self_workflow_by_module.get(module)
            other_workflow = other_workflow_by_module.get(module)
            if self_workflow and other_workflow:
                merged_workflows.append(self_workflow.merge(other_workflow))
            elif self_workflow:
                merged_workflows.append(self_workflow)
            elif other_workflow:
                merged_workflows.append(other_workflow)

        return VellumCliConfig(workflows=merged_workflows, version=self.version)


def load_vellum_cli_config(root_dir: Optional[str] = None) -> VellumCliConfig:
    if root_dir is None:
        root_dir = os.getcwd()
    lockfile_path = os.path.join(root_dir, LOCKFILE_PATH)
    if not os.path.exists(lockfile_path):
        lockfile_data = {}
    else:
        with open(lockfile_path, "rb") as f:
            lockfile_data = json.load(f)
    lockfile_config = VellumCliConfig.model_validate(lockfile_data)

    pyproject_toml_path = os.path.join(root_dir, PYPROJECT_TOML_PATH)
    if not os.path.exists(pyproject_toml_path):
        toml_vellum: Dict = {}
    else:
        with open(pyproject_toml_path, "rb") as f:
            toml_loaded = tomli.load(f)
        toml_tool = toml_loaded.get("tool", {})
        if not isinstance(toml_tool, dict):
            toml_vellum = {}

        toml_vellum = toml_tool.get("vellum")
        if not isinstance(toml_vellum, dict):
            # Mypy is wrong. this is totally reachable.
            toml_vellum = {}  # type: ignore[unreachable]
    toml_config = VellumCliConfig.model_validate(toml_vellum)

    return toml_config.merge(lockfile_config)
