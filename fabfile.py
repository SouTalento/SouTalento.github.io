# encoding: utf-8

import os

from fabric.api import env, sudo
from fabric.operations import local
from fabric.contrib.project import rsync_project
from fabric.contrib.files import append

env.use_ssh_config = False

env.local_dir = os.path.join(os.path.dirname(__file__), '_site', '')


def staging():
    env.environment = 'staging'
    env.user = 'ubuntu'
    env.hosts = ['staging.empreguei.com']
    env.site_url = 'staging.empreguei.com'

    env.remote_home_dir = os.path.join('/home', env.user)
    env.remote_dir = os.path.join(env.remote_home_dir, 'jobn-website', '')

    env.restart_server = lambda: sudo('systemctl reload nginx')
    env.stop_server = lambda: sudo('systemctl stop nginx')


def production():
    env.environment = 'production'
    env.user = 'ubuntu'
    env.hosts = ['empreguei.com']
    env.site_url = 'empreguei.com'

    env.remote_home_dir = os.path.join('/home', env.user)
    env.remote_dir = os.path.join(env.remote_home_dir, 'jobn-website', '')

    env.restart_server = lambda: sudo('systemctl reload nginx')
    env.stop_server = lambda: sudo('systemctl stop nginx')


def deploy():
    local_render()
    # env.stop_server()
    delete_project()
    upload_project()
    restart_server()


def local_render():
    append('_config.yml', 'url: ' + env.site_url)
    local('jekyll build')


def upload_project():
    rsync_project(
        local_dir=env.local_dir,
        remote_dir=env.remote_dir,
    )


def delete_project():
    try:
        os.remove(env.remote_dir)
    except Exception as e:
        print(e)
    finally:
        try:
            os.mkdir(env.remote_dir)
        except Exception as e:
            print(e)


def restart_server():
    env.restart_server()


def stop_server():
    env.stop_server()
