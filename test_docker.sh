export TEST=test
# export TEST=no
export DOCKER_IMG=aaqua_sys_img
export GRPC_PORT=8000
export REST_PORT=5000

docker build -t $DOCKER_IMG -f Dockerfile .
docker-compose build
docker-compose --profile $TEST up --remove-orphans
# docker-compose stop
