#!/bin/bash

set -e

ARGS=$@
docker compose -f docker-compose.dev.yaml down $ARGS
