#!/usr/bin/env bash

REPOSITORY_NAME="$1"
REPOSITORY_ROOT_DIR="$2"
REPOSITORY_URL=`git config --get remote.origin.url`
LAST_RELEASE=`git ls-remote --tags --refs --sort="v:refname" $REPOSITORY_URL | tail -n1 | sed 's/.*\///'`

mkdir -p ./build

if [ -z "$LAST_RELEASE" ]; then
    echo "No tag / new release found ! - Or error when parsing. Downloading last commit to the repository (master branch) ;"
    eossr-zip-repository -d $REPOSITORY_ROOT_DIR -n $REPOSITORY_NAME
    mv $REPOSITORY_NAME.zip ./build
else
    echo "$LAST_RELEASE tag / release found !"
    eossr-zip-repository -d $REPOSITORY_ROOT_DIR -n $REPOSITORY_NAME-$LAST_RELEASE
    mv $REPOSITORY_NAME-$LAST_RELEASE.zip ./build
fi

if [[ -f ./codemeta.json ]]; then
    cp ./codemeta.json ./build
fi