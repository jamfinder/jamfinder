from application import app
from flask.views import View
from utils import get_concert_songs
import settings, random, os
from flask import Blueprint, request, redirect, render_template, url_for
import json
from flask import Markup

zipcode = 19104

@app.route('/')
def index():
    concerts = get_concert_songs(zipcode)
    print type(concerts)
    return render_template('index.html', google_maps_api_key = settings.GOOGLE_MAPS_API_KEY,
                           concerts = Markup(concerts))

# class UpdateView(View):
#     if request.form['location']:



#    def get_context(self, slug):
#         post = Post.objects.get_or_404(slug=slug)

#     def get(self, slug):
#         post =

        # @app.route("/update", methods = ['POST'])

def update():
    return redirect('/')
