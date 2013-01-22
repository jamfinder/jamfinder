from application import app
from flask.views import MethodView
from utils import get_concert_songs
import settings, random, os
from flask import Blueprint, request, redirect, render_template, url_for
import json, re
from flask import Markup

zipcode = 19104

@app.route('/')
def index():
    concerts = get_concert_songs(zipcode)
    print type(concerts)
    return render_template('index.html', google_maps_api_key = settings.GOOGLE_MAPS_API_KEY,
                           concerts = Markup(concerts))

class UpdateView(MethodView):
    current_addr = zipcode
    def post(self):
        radius = request.form['radius']
        date = request.form['date']
        addr = request.form['address']
        if not addr:
            addr = current_addr
        if not re.match(r'\d{5}', addr):
            addr = get_zipcode_from_address(addr)
        concerts = get_concert_songs(addr, radius = radius,
                                     end_date = date)
        current_addr = addr
        response= make_response(concerts)
        response.content_type = 'application/json'
        return response

app.add_url_rule('/update/', view_func=UpdateView.as_view('update'))
