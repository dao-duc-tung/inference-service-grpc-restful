#!/bin/bash

export TEST=$1
export TEST_SLOW=$2

export PYTEST_OPT=""

if [ "$TEST" == "1" ]
then
    export TEST=test
else
    export TEST=no
fi

if [ "$TEST_SLOW" == "1" ]
then
    export PYTEST_OPT="${PYTEST_OPT} --runslow"
fi

export DOCKER_IMG=aaqua_sys_img
export GRPC_PORT=8000
export REST_PORT=5000

export DB_HOST_NAME=aaqua_db
export DB_PORT=6379

docker build -t $DOCKER_IMG -f Dockerfile .
docker-compose build
docker-compose --profile $TEST up --remove-orphans
# docker-compose stop
