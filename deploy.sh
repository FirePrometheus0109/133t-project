#!/bin/bash

# ENVIRONMENT=$1

python3 -m pip install --upgrade pip

python3 -m pip install --requirement backend/requirements/deploy.txt

# fab prepare_env:${ENVIRONMENT} lock_deploy stop_server docker_pull start_server unlock_deploy
fab prepare_env:production update_compose_file stop_server docker_pull start_server