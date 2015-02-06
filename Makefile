IGNORE_OPT=
TESTS_DIR=openfisca_tunisia/tests

check-tests-syntax:
	pyflakes $(TESTS_DIR)

test: check-tests-syntax
	nosetests -v  $(TESTS_DIR) $(IGNORE_OPT)

test-with-coverage:
	nosetests -v $(TESTS_DIR) $(IGNORE_OPT) --with-coverage --cover-package=openfisca_tunisia --cover-erase --cover-branches --cover-html
