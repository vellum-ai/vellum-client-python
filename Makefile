SHELL := /bin/bash

################################
# Setup
################################

setup: setup-python setup-poetry install-deps setup-pre-commit

setup-python:
	brew list python@3.9 || brew install python@3.9

setup-poetry:
	which poetry || curl -sSL https://install.python-poetry.org | python - -y --version 1.5.1

install-deps:
	poetry lock && poetry install

setup-pre-commit:
	pre-commit install \
	&& pre-commit install -t pre-push


################################
# Testing
################################

test:
	fern test --command "poetry run pytest -rEf -s -vv $(file)"

test-raw:
	poetry run pytest -rEf -s -vv $(file)
