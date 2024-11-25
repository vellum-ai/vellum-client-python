# Contributing to Vellum Python SDKs

Thank you for your interest in contributing to the Vellum Python SDKs! This document provides guidelines and instructions for contributing.

## Setup

1. Clone the repository:

```bash
git clone https://github.com/vellum-ai/vellum-python-sdks.git
```

2. Setup your development environment:

```bash
make setup
```

3. Verify installation is correct by running tests and ensuring success:

```bash
make test
```

## Development

Each contribution should be made in its own branch, and accompanied with a test:

- `src/vellum/workflows/**/tests` - if unit testing the relevant file is sufficient for testing the new feature
- `tests/workflows` - if you need to test the new feature in the context of an entire workflow
- `vellum_ee/**/tests` - if you need to test the new feature in the context of Vellum Enterprise feature, such as serialization
- `tests/client` - these tests are generated automatically by [Fern](https://buildwithfern.com/) and should not be modified manually

To actually run the tests:

- `make test` - runs the test while spinning up Fern's mock server. Useful for running their tests specifically. Supports a `file` argument for running a specific file or directory.
- `make test-raw` - runs the test just using poetry. Useful for running tests that don't require the mock server, such as all Workflows SDK tests. Supports a `file` argument for running a specific file or directory.
