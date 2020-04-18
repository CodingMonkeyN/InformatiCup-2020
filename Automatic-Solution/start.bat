docker build --no-cache --tag gameapi .
docker run --publish 50123:50123 --interactive --tty --rm gameapi
PAUSE