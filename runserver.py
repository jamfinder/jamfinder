from application import app

if app.config['DEBUG']:
    app.debug = True

app.run(debug = True)
