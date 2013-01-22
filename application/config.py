import os
basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

try:
    if 'DATABASE_URL' in os.environ:
        SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    except:
        print "Unexpected error:", sys.exc_info()
