from application import app
from flask.views import View
from utils import get_concert_songs

zipcode = 19104

@app.route('index')
@app.route('/')
def index():
    template_values = {
        'google_maps_api_key' : settings.GOOGLE_MAPS_API_KEY,
        'random' : random.random(),
        'concerts' : get_concert_songs(zipcode)
    }
    path = os.path.join(os.path.dirname(__file__), 'templates/index.html')
    self.response.out.write(template.render(path, template_values))

@app.route("/update", methods = ['POST'])
def update():

    return redirect('/')
