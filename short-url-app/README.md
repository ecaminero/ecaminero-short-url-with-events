# A Short url App
A Meli tests

### Requirements 
* [Python 3.10](https://www.python.org/downloads/)
* [Poetry](https://python-poetry.org/docs/#installation)
* [Docker](https://docs.docker.com/get-docker/)
* [Docker Compose](https://docs.docker.com/compose/compose-file/)

## Install packages
```shell script
poetry install
```

## Run Tests 
```shell script
poetry run pytest
```

## Run Local
```shell script

## uvicorn server
poetry run uvicorn src.main:app --reload --port 8000

## hypercorn server
poetry run hypercorn src.main:app --bind 0.0.0.0:8000
```