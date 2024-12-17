SHELL := /bin/bash

################################
# Setup
################################

setup: setup-python setup-poetry install-deps setup-pre-commit setup-fern

setup-python:
	brew list python@3.9 || brew install python@3.9

setup-poetry:
	python3 -m scripts.install_poetry -y --version 1.5.1

# We use the full path to poetry to avoid any issues with the shell configuration from the setup-poetry step
install-deps:
	$(HOME)/.local/bin/poetry env use 3.9 && $(HOME)/.local/bin/poetry lock && $(HOME)/.local/bin/poetry install

setup-pre-commit:
	pre-commit install \
	&& pre-commit install -t pre-push

setup-node:
	command -v nvm >/dev/null 2>&1 || (curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh | bash) \
	&& (nvm use $(cat ee/codegen/.nvmrc) || nvm install $(cat ee/codegen/.nvmrc))

setup-fern:
	which fern || npm install -g fern-api


################################
# Testing
################################

test:
	fern test --command "poetry run pytest -rEf -s -vv $(file)"

test-raw:
	poetry run pytest -rEf -s -vv $(file)


################################
# Linting
################################

format:
	poetry run black . \
	&& poetry run isort .

