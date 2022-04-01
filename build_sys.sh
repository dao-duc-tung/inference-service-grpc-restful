#!/bin/bash

# TEST in ["none", "test"]
export TEST=$1
# PYTEST_OPT in ["", "--runslow"]
export PYTEST_OPT=$2

if [ "$TEST" != "test" ]
then
    export TEST=none
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
