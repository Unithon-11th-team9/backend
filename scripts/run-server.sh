#!/bin/bash

set -e

ARGS=$@
# poetry install --sync
pip install -r requirements.txt
# uvicorn app.main:app --host 0.0.0.0 --port 8000 $ARGS

# TODO: 삭제 예정
nohup uvicorn app.main:app --host 0.0.0.0 --port 3390 &