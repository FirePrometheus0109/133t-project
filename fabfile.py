#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import with_statement

import os
import time
from base64 import b64decode
from tempfile import NamedTemporaryFile

from dotenv import find_dotenv, load_dotenv
from fabric.api import cd, env, run, task, put


def get_env_value(key, env_name=None):
    if env_name is None:
        value = os.environ.get(key)
    else:
        value = os.environ.get(str(env_name).upper() + '_' + key)
    # for local deploy
    # print('Getting from env', env_name, key, value)
    return value


def put_to_global(env_name, key):
    value = get_env_value(key, env_name)
    os.environ[key] = value


@task
def prepare_env(env_name):
    load_dotenv(find_dotenv(), verbose=True)
    # prepare fabric
    # env.hosts = get_env_value('SERVER_IP')
    # env.user = get_env_value('SSH_USER')
    # env.port = get_env_value('SSH_PORT')
    env.hosts = '165.227.83.243'
    env.user = 'root'
    env.port = 22
    # ssh_key = NamedTemporaryFile(delete=False)
    # ssh_key.write(b64decode(get_env_value('SSH_PRIVATE_KEY', env_name)))
    env.key_filename = '~/.ssh/one33t.pem'
    # prepare global environmane variables
    # global_keys = ['MAIN_PATH', 'LOCK_FILENAME', 'BUILD_ENVIRONMENT']
    global_keys = ['MAIN_PATH']
    for global_key in global_keys:
        put_to_global(env_name, global_key)
    env.dotenv_path = os.path.join(get_env_value('MAIN_PATH'), '.env')


@task
def lock_deploy():

    def str2bool(v):
        return v.lower() in ('yes', 'true', 't', '1')

    LOCK_FILE = get_env_value('LOCK_FILENAME')
    check_lock_command = (
        'python3 -c '
        '\'import os; '
        'print(os.path.isfile("{filename}"))\''.format(filename=LOCK_FILE)
    )
    locked = False
    while not locked:
        not_locked = not str2bool(run(check_lock_command))
        if not_locked:
            run('touch ' + LOCK_FILE)
            locked = True
        else:
            print('Locked by another process, wait 10 secs')
            time.sleep(10)


@task
def stop_server():
    with cd(get_env_value('MAIN_PATH')):
        # run('make down-prod')
        run('docker-compose -f production.yml down --remove-orphans')


@task
def git_pull():
    with cd(get_env_value('MAIN_PATH')):
        current_branch = run("git branch | grep \\* | cut -d ' ' -f2")
        run('git config user.name server')
        run('git config user.email server@server.com')
        run('git reset --hard HEAD')
        run('git pull origin {}'.format(current_branch))


@task
def docker_pull():
    with cd(get_env_value('MAIN_PATH')):
        # BUILD_ENVIRONMENT = get_env_value('BUILD_ENVIRONMENT')
        # run('make build-prod BUILD_ENVIRONMENT={}'.format(BUILD_ENVIRONMENT))
        run('docker-compose -f production.yml pull')


@task
def start_server():
    with cd(get_env_value('MAIN_PATH')):
        # run('make start-prod') # docker-compose -f production.yml up -d
        run('docker-compose -f production.yml up -d') # docker-compose -f production.yml up -d
        # run('make migrate-prod')  # docker-compose -f production.yml exec django /entrypoint -- ./manage.py migrate
        run('docker-compose -f production.yml exec django /entrypoint -- ./manage.py migrate')


@task
def unlock_deploy():
    LOCK_FILE = get_env_value('LOCK_FILENAME')
    run('rm ' + LOCK_FILE)


@task
def exec_commands():
    with open('commands.txt') as f:
        lines = f.readlines()
        for line in lines:
            run(line)

@task
def update_compose_file():
    env.key_filename = '~/.ssh/one33t.pem'
    with cd(get_env_value('MAIN_PATH')):
        put('production.yml', 'production.yml')