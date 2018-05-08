#!/bin/bash

set -e
CURRENT_VERSION=`python setup.py --version`

if ! git rev-parse $CURRENT_VERSION 2>/dev/null ; then
    git tag $CURRENT_VERSION
    git push --tags  # update the repository version
    python setup.py bdist_wheel  # build this package in the dist directory
    twine upload dist/* --username $PYPI_USERNAME --password $PYPI_PASSWORD  # publish
else
    echo "No deployment - Only non-functional elements were modified in this change"
fi
