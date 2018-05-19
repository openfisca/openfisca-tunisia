#! /bin/bash

VERSION_CHANGE_TRIGGERS="setup.py MANIFEST.in openfisca_tunisia"

if git diff-index origin/master -- $VERSION_CHANGE_TRIGGERS ":(exclude)*.md"
then
    exit 0  # there are no changes at all, the version is correct
fi

CURRENT_VERSION=`python setup.py --version`

if ! git diff-index origin/master openfisca_tunisia
then
    if git rev-parse --verify $CURRENT_VERSION
    then
        set +x
        echo "Version $CURRENT_VERSION already exists."
        git --no-pager log -1 $CURRENT_VERSION
        echo
        echo "Please update version number in setup.py before merging this branch into master."
        echo "Look at the CONTRIBUTING.md file to learn how the version number should be updated."
        exit 1
    fi

    if git diff-index origin/master CHANGELOG.md
    then
        set +x
        echo "CHANGELOG.md has not been modified."
        echo "Please explain what you changed in CHANGELOG.md before merging this branch into master."
        echo "Look at the CONTRIBUTING.md file to learn how to write that."
        exit 2
    fi
fi
