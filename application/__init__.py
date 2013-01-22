import json, os, re, sys
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
__all__ = ['create_app','db']

# A list of app modules and their prefixes. Each APP entry must contain a
# 'name', the remaining arguments are optional. An optional 'models': False
# argument can be given to disable loading models for a given module.
MODULES = [
#   {'name': 'foo',  'url_prefix': '/admin' },
    {'name': 'aaa',  'url_prefix': '/'      },
    {'name': 'home', 'url_prefix': '/'      },
    {'name': 'mod1', 'url_prefix': '/'      },
    {'name': 'mod2', 'url_prefix': '/mod2'  },
    {'name': 'mod3', 'url_prefix': '/mod3'  },
]

# Create the Skeleton app
app = Flask(__name__, static_path='/static')
from application import views, models
# DB class
app.config['SQLALCHEMY_DATABASE_URI'] = = os.environ['DATABASE_URL']
db = SQLAlchemy(app)
