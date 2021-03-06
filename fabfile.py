from fabric.api import *

# the user to use for the remote commands
#env.user = settings.deployment["user"]
#env.password = settings.deployment["password"]
# the servers where the commands are executed
#env.hosts = [settings.deployment["host"]]

def create_db():
    from application import db
    db.create_all()
    print 'created db'

def _reload():
    sudo("service uwsgi restart")
    sudo("service nginx restart")

def _copy():
    put(settings.deployment["localpath"], settings.deployment["remotepath"])

def _delete_local_extra_files():
    local("find . -name \*.pyc -delete")
    local("find . -name \.DS_Store -delete")

def deploy():
    _delete_local_extra_files()
    _copy()
    _reload()
