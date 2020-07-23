from flask import Flask, render_template, jsonify, request
from socket import gethostname
import urllib
import json

app = Flask(__name__)

# location urly
location_url = "http://api.ipstack.com/{}?access_key=1151c98fdaced8a6c62e7c37a44e8da7"


CLIENT_ID = "A3F72945ACFCA109BFC672EF1FA58A679AAB238B"
CLIENT_SECRET = "B02EF4FC7AA1F189ED2CDE9E91D86C536828EFA0"

API_PARAMS = "?client_id={}&client_secret={}"

TRENDING = "https://api.untappd.com/v4/beer/trending"

@app.route("/", methods=["GET"])
def home():

    ip = request.environ['REMOTE_ADDR']
    print(ip)

    location_request = location_url.format(ip)
    location_response = urllib.request.urlopen(location_request)
    location_data_temp = location_response.read()
    location_data = json.loads(location_data_temp)
    print(location_data)

    lat = location_data['latitude']
    lon = location_data['longitude']

    print(lat, lon)

    api_url = TRENDING + API_PARAMS.format(CLIENT_ID, CLIENT_SECRET)
    trending_response = urllib.request.urlopen(api_url)
    json_data = trending_response.read()
    data = json.loads(json_data)

    beers = data['response']['macro']['items']

    return render_template("home.html", beers=beers, lat=lat, lon=lon)

if __name__ == "__main__":
    if 'liveconsole' not in gethostname():
        app.run(debug=True)
