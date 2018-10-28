#!/bin/bash


all: test

install:
	pip install --upgrade pip twine wheel
	pip install --editable .[tests,notebook] --upgrade

check-no-prints:
	@test -z "`git grep -w print openfisca_tunisia/model`"

check-syntax-errors:
	python -m compileall -q .

clean:
	rm -rf build dist
	find . -name '*.mo' -exec rm \{\} \;
	find . -name '*.pyc' -exec rm \{\} \;

flake8:
	@# Do not analyse .gitignored files.
	@# `make` needs `$$` to output `$`. Ref: http://stackoverflow.com/questions/2382764.
	flake8 `git ls-files | grep "\.py$$"`

test: check-syntax-errors check-no-prints
	# Launch tests from 'tests' directory (and not .) because TaxBenefitSystem must be initialized
	# before parsing source files containing formulas.
	@echo "> Python tests..."
	nosetests tests --exe --with-doctest
	@echo "> Yaml tests..."
	openfisca-run-test -c openfisca_tunisia  tests/
	@echo "> Notebooks tests..."
	python notebooks/test_notebooks.py notebooks/

# pre-condition: pip install jupyter
nb:
	jupyter notebook demo.ipynb
