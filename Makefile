all: test

uninstall:
	pip freeze | grep -v "^-e" | xargs pip uninstall -y

clean:
	rm -rf build dist
	find . -name '*.pyc' -exec rm \{\} \;

deps:
	pip install --upgrade pip build twine

install: deps
	@# Install OpenFisca-Tunisia for development.
	@# `make install` installs the editable version of OpenFisca-Tunisia.
	@# This allows contributors to test as they code.
	pip install --editable .[dev] --upgrade
	pip install openfisca-core[web-api]

build: clean deps
	@# Install OpenFisca-Tunisia for deployment and publishing.
	@# `make build` allows us to be be sure tests are run against the packaged version
	@# of OpenFisca-Tunisia, the same we put in the hands of users and reusers.
	python -m build
	pip uninstall --yes openfisca-tunisia
	find dist -name "*.whl" -exec pip install {}[dev] \;
	pip install openfisca-core[web-api]

check-syntax-errors:
	python -m compileall -q .

format-style:
	@# Do not analyse .gitignored files.
	@# `make` needs `$$` to output `$`. Ref: http://stackoverflow.com/questions/2382764.
	autopep8 `git ls-files | grep "\.py$$"`

check-style:
	@# Do not analyse .gitignored files.
	@# `make` needs `$$` to output `$`. Ref: http://stackoverflow.com/questions/2382764.
	flake8 `git ls-files | grep "\.py$$"`

check-path-length:
	@# Verify that there is no path exceeding Windows limit
	python openfisca_tunisia/scripts/check_path_length.py

check-yaml:
	@# check yaml style
	.github/lint-changed-yaml-tests.sh

check-all-yaml:
	@# check yaml style
	yamllint openfisca_tunisia/parameters
	yamllint tests

test: clean check-syntax-errors check-style
	@# Launch tests from openfisca_tunisia/tests directory (and not .) because TaxBenefitSystem must be initialized
	@# before parsing source files containing formulas.
	@echo "> Yaml tests..."
	openfisca test --country-package openfisca_tunisia tests
	@# @echo "> Notebooks tests..."
	@# python openfisca_tunisia/notebooks/test_notebooks.py notebooks/
