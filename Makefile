#!/bin/bash

all: test

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
	@# Launch tests from openfisca_tunisia/tests directory (and not .) because TaxBenefitSystem must be initialized
	@# before parsing source files containing formulas.
	nosetests openfisca_tunisia/tests --exe --with-doctest
	openfisca-run-test -c openfisca_tunisia  openfisca_tunisia/tests/
	python notebooks/test_notebooks.py notebooks/

nb:
	python notebooks/test_notebooks.py notebooks/
