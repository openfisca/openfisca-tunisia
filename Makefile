# Use uv for all Python/package commands. Override with: make UV=python to use system Python.
UV = uv run

all: test

uninstall:
	uv pip uninstall openfisca-tunisia -y 2>/dev/null || true

clean:
	rm -rf build dist
	find . -name '*.pyc' -exec rm \{\} \;

deps:
	uv pip install build twine

install:
	@# Install OpenFisca-Tunisia for development (editable).
	uv sync --extra dev

build: clean deps
	@# Build and install the package from wheel to test the distributed version.
	uv build
	uv pip uninstall openfisca-tunisia -y 2>/dev/null || true
	find dist -name "*.whl" -exec uv pip install {}[dev] \;

check-syntax-errors:
	$(UV) python -m compileall -q .

format-style:
	$(UV) ruff format .
	$(UV) ruff check --fix .

check-style:
	$(UV) ruff check .

check-path-length:
	$(UV) python openfisca_tunisia/scripts/check_path_length.py

check-yaml:
	.github/lint-changed-yaml-tests.sh

check-all-yaml:
	$(UV) yamllint openfisca_tunisia/parameters
	$(UV) yamllint tests

test: clean check-syntax-errors check-style
	@echo "> Yaml tests..."
	$(UV) openfisca test --country-package openfisca_tunisia tests
