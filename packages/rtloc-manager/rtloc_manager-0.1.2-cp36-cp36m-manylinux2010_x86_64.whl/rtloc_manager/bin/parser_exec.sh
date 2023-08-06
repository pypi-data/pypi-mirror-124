#!/bin/bash

# run script independent of calling directory
cd "$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"

export LD_LIBRARY_PATH=.
./parser $1
