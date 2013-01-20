from application import app
from flask.views import View
from flask import jsonify, render_template, request
from application import util

@app.route('index')
@app.route('/')
def index():
    def get(self):
        #extract user location from request data

        template_values = {
            'random' : random.random(),
            'posts' :
        }
    path = os.path.join(os.path.dirname(__file__), 'templates/index.html')
    self.response.out.write(template.render(path, template_values))

@app.route('/_update_view_query/<query>')
def update_view(query):
    concert_map.update({'_id'})
    return redirect("/")
