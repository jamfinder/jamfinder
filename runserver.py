from application import app

from os.path import abspath, dirname; app.root_path = abspath(dirname(__file__))

if app.config['DEBUG']:
    app.debug = True

app.run(debug = True)
