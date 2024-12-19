# Vellum SDK Automation

This is a mini package hosting all of the automation scripts needed for managing Vellum SDKs from within each SDK repository. During the release process of this repository, this directory is copied into the `ee/automation` directory of each of the respective SDKs.

## Scripts

Here are all the scripts we support.

### `npm run create-release`

This script is used to create a release for a given SDK. It is triggered by a pull request in the SDK repository being merged into the `main` branch with the `release` label. The GitHub action for this trigger is defined in `release.yml` and copied into the SDK repository within the `.github/workflows` directory.
