# Use uv run for all Python/package commands. Override with: make UV=python to use system Python.
UV = uv run

all: test

uninstall:
	uv pip uninstall openfisca-tunisia-pension -y 2>/dev/null || true

clean:
	rm -rf build dist
	find . -name '*.pyc' -exec rm \{\} \;

deps:
	uv pip install build twine

install:
	@# Install OpenFisca-Tunisia-Pension for development (editable).
	uv sync --extra dev

build: clean deps
	@# Build and install the package from wheel to test the distributed version.
	uv build
	uv pip uninstall openfisca-tunisia-pension -y 2>/dev/null || true
	find dist -name "*.whl" -exec uv pip install {}[dev] \;

check-syntax-errors:
	uv run python -m compileall -q .

format-style:
	uv run ruff format .
	uv run ruff check --fix .

check-style:
	uv run ruff check .

check-path-length:
	uv run python openfisca_tunisia_pension/scripts/check_path_length.py

check-yaml:
	@# `uv run` fournit yamllint au script, qui appelle le binaire par son nom.
	uv run .github/lint-changed-yaml-tests.sh

check-all-yaml:
	uv run yamllint openfisca_tunisia_pension/parameters
	uv run yamllint tests

test: clean check-syntax-errors check-style check-yaml
	@echo "> Yaml tests..."
	uv run openfisca test --country-package openfisca_tunisia_pension tests
