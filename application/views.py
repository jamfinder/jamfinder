from application import app
from flask.views import View
from utils import get_concert_songs
import settings, random, os
from flask import Blueprint, request, redirect, render_template, url_for

zipcode = 19104

@app.route('/')
def index():
    path = os.path.join(os.path.dirname(__file__), 'template/index.html')
    return render_template(path, google_maps_api_key = settings.GOOGLE_MAPS_API_KEY, concerts = get_concert_songs(zipcode))

# class UpdateView(View):
#     def get_context(self, slug):
#         post = Post.objects.get_or_404(slug=slug)

#     def get(self, slug):
#         post =

# @app.route("/update", methods = ['POST'])

def update():
    return redirect('/')
