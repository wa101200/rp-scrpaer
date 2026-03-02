#!/bin/bash

export GIT_DIFF_HASH=$((git diff; git diff --cached) | sha1sum | awk '{print $1}')
