#!/bin/sh

source ./percona_build_env.sh

cd ${BUILD_DIR}

make install

cd ${PWD_PATH}
