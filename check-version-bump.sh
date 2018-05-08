#! /bin/bash

CURRENT_VERSION=`python setup.py --version`

if ! git diff-index origin/master openfisca_tunisia
then
    if git rev-parse $CURRENT_VERSION
    then
        set +x
        echo "Version $CURRENT_VERSION already exists. Please update version number in setup.py before merging this branch into master."
        exit 1
    fi

    if git diff-index origin/master CHANGELOG.md
    then
        set +x
        echo "CHANGELOG.md has not been modified. Please update it before merging this branch into master."
        exit 1
    fi
fi
