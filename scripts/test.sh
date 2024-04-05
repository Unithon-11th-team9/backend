#!/bin/bash

set -ex


ARGS=$@
poetry install --sync
docker compose -f docker-compose.dev.yaml up -d db
pytest $ARGS
docker compose -f docker-compose.dev.yaml down