from typing import List, Optional

import click

from vellum_cli.aliased_group import ClickAliasedGroup
from vellum_cli.image_push import image_push_command
from vellum_cli.pull import pull_command
from vellum_cli.push import push_command


@click.group(cls=ClickAliasedGroup)
def main() -> None:
    """Vellum SDK CLI"""
    pass


@main.command()
@click.argument("module", required=False)
@click.option("--deploy", is_flag=True, help="Deploy the workflow after pushing it to Vellum")
@click.option("--deployment-label", type=str, help="Label to use for the deployment")
@click.option("--deployment-name", type=str, help="Unique name for the deployment")
@click.option("--deployment-description", type=str, help="Description for the deployment")
@click.option("--release-tag", type=list, help="Release tag for the deployment", multiple=True)
def push(
    module: Optional[str],
    deploy: Optional[bool],
    deployment_label: Optional[str],
    deployment_name: Optional[str],
    deployment_description: Optional[str],
    release_tag: Optional[List[str]],
) -> None:
    """Push Workflow to Vellum"""
    push_command(
        module=module,
        deploy=deploy,
        deployment_label=deployment_label,
        deployment_name=deployment_name,
        deployment_description=deployment_description,
        release_tags=release_tag,
    )


@main.command()
@click.argument("module", required=False)
@click.option("--legacy-module", is_flag=True, help="Pull the workflow as a legacy module")
@click.option("--include-json", is_flag=True, help="Include the JSON representation of the Workflow in the pull response. Should only be used for debugging purposes.")
def pull(module: Optional[str], legacy_module: Optional[bool], include_json: Optional[bool]) -> None:
    """Pull Workflow from Vellum"""
    pull_command(module, legacy_module, include_json)


@main.group(aliases=["images", "image"])
def images() -> None:
    """Vellum Docker Images"""
    pass


@images.command(name="push")
@click.argument("image", required=True)
@click.option(
    "--tag",
    "-t",
    multiple=True,
    help="Tags the provided image inside of Vellum's repo. "
    "This field does not push multiple local tags of the passed in image.",
)
def image_push(image: str, tag: Optional[List[str]] = None) -> None:
    """Push Docker image to Vellum"""
    image_push_command(image, tag)


if __name__ == "__main__":
    main()
