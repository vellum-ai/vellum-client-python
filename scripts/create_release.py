import yaml
import os
from typing import List, Optional, TypedDict
from github import Github

class ChangelogEntry(TypedDict):
    summary: str
    latest: Optional[bool]

class Version(TypedDict):
    version: str
    createdAt: str
    changelogEntry: List[ChangelogEntry]

def get_github_token() -> str:
    # This would need to be implemented to get the token from environment variables
    # or other auth mechanism
    return os.environ["GITHUB_TOKEN"]

def main() -> None:
    # Read and parse versions.yaml
    with open("versions.yaml", "r") as f:
        versions = yaml.safe_load(f)

    # Type checking would happen at runtime
    version_data: List[Version] = versions

    # Get latest version info
    latest = version_data[0]
    version = latest["version"]
    changelog_entries = latest["changelogEntry"]
    
    # Create changelog text
    changes = "\n".join(entry["summary"] for entry in changelog_entries)

    # Create the release
    token = get_github_token()
    g = Github(token)
    repo = g.get_repo("vellum-ai/vellum-client-generator")

    repo.create_git_release(
        tag=version,
        name=version,
        message=changes,
        prerelease=False
    )

    print(f"Successfully created release '{version}'")

if __name__ == "__main__":
    main()
