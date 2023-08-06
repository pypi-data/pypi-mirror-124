#!/usr/bin/env bash

REPOSITORY_NAME="$1"
REPOSITORY_ROOT_DIR="$2"
BUILD_DIR="$3"
if [ -z "$BUILD_DIR" -a "${BUILD_DIR+xxx}" = "xxx" ]; then BUILD_DIR="_OSSR_BUILD"; fi;
REPOSITORY_URL=`git config --get remote.origin.url`
LAST_RELEASE=`git ls-remote --tags --refs --sort="v:refname" $REPOSITORY_URL | tail -n1 | sed 's/.*\///'`

mkdir -p $BUILD_DIR

if [ -z "$LAST_RELEASE" ]; then
    echo "No tag / new release found ! - Or error when parsing. Downloading last commit to the repository (master branch) ;"
    eossr-zip-repository -d $REPOSITORY_ROOT_DIR -n $REPOSITORY_NAME
    mv $REPOSITORY_NAME.zip $BUILD_DIR
else
    echo "$LAST_RELEASE tag / release found !"
    eossr-zip-repository -d $REPOSITORY_ROOT_DIR -n $REPOSITORY_NAME-$LAST_RELEASE
    mv $REPOSITORY_NAME-$LAST_RELEASE.zip $BUILD_DIR
fi

if [[ -f ./codemeta.json ]]; then
    cp ./codemeta.json $BUILD_DIR
fi