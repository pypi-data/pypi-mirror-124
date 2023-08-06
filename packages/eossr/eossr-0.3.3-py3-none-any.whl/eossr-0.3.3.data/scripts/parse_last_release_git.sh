#!/usr/bin/env bash

REPOSITORY_NAME="$1"
REPOSITORY_BASE_URL="$2"

LAST_RELEASE=`git ls-remote --tags --refs --sort="v:refname" $REPOSITORY_BASE_URL.git | tail -n1 | sed 's/.*\///'`

if [ -z "$LAST_RELEASE" ]; then
    echo "No tag / new release found ! - Or error when parsing. Downloading last commit to the repository (master branch) ;"
    wget -O $REPOSITORY_NAME-master.zip "$REPOSITORY_BASE_URL"/-/archive/master/"$REPOSITORY_NAME"-master.zip
    mv $REPOSITORY_NAME-master.zip ./build
else
    echo "$LAST_RELEASE tag / release found !"
    wget -O $REPOSITORY_NAME-$LAST_RELEASE.zip "$REPOSITORY_BASE_URL"/-/archive/"$LAST_RELEASE"/"$REPOSITORY_NAME"-"$LAST_RELEASE".zip
    mv $REPOSITORY_NAME-$LAST_RELEASE.zip ./build
fi
