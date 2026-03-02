#!/bin/bash

# set current git branch sha and normalized branch name 

export GIT_SHA_SHORT=$(git rev-parse --short HEAD)
export GIT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
export GIT_BRANCH_NORM=$(echo $GIT_BRANCH | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]/-/g') 