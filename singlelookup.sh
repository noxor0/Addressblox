# Runs single look up commands from the docker container
DOCKER_NAME=$(grep -o "=.*" config.env)
DOCKER_NAME=${DOCKER_NAME:1:${#DOCKER_NAME}-1}
app_running=$(docker ps | grep -o $DOCKER_NAME)

if [[ ${#app_running} == 0 ]] ; then
  make build
  make run
fi

docker exec -it $DOCKER_NAME python src/addressblox/search.py $@
