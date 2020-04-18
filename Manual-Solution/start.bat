cd ./manual_solution/
docker build --tag frontend .
docker run --publish 4200:4200 --interactive --tty --rm frontend
PAUSE