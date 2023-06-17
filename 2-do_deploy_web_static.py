#!/usr/bin/python3
"""Compress web static package
"""
from fabric.api import *
from datetime import datetime
from os import path


env.hosts = ['52.3.220.193', '18.210.33.70']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/id_rsa'


def do_deploy(archive_path):
    """Deploy web files to server
    """
    try:
        if not path.exists(archive_path):
            return False

        # Upload archive
        put(archive_path, '/tmp/')

        # Create target dir
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        run('sudo mkdir -p /data/web_static/releases/web_static_{}/'.format(timestamp))

        # Uncompress archive and delete .tgz
        run('sudo tar -xzf /tmp/{}.tgz -C /data/web_static/releases/web_static_{}/'.format(timestamp, timestamp))

        # Remove archive
        run('sudo rm /tmp/{}.tgz'.format(timestamp))

        # Move contents into host web_static
        run('sudo mv /data/web_static/releases/web_static_{}/web_static/* /data/web_static/releases/web_static_{}/'.format(timestamp, timestamp))

        # Remove extraneous web_static dir
        run('sudo rm -rf /data/web_static/releases/web_static_{}/web_static'.format(timestamp))

        # Delete pre-existing symbolic link
        run('sudo rm -rf /data/web_static/current')

        # Re-establish symbolic link
        run('sudo ln -s /data/web_static/releases/web_static_{}/ /data/web_static/current'.format(timestamp))
    except:
        return False

    # Return True on success
    return True
