#!/bin/bash

set -e

ARGS=$@
docker compose -f docker-compose.dev.yaml build
docker compose -f docker-compose.dev.yaml up $ARGS