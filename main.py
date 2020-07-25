from flask import Flask, render_template, jsonify, request
from socket import gethostname
import urllib
import json

app = Flask(__name__)

CLIENT_ID = "A3F72945ACFCA109BFC672EF1FA58A679AAB238B"
CLIENT_SECRET = "B02EF4FC7AA1F189ED2CDE9E91D86C536828EFA0"

API_PARAMS = "?client_id={}&client_secret={}"

TRENDING = "https://api.untappd.com/v4/beer/trending"

LOCAL = "https://api.untappd.com/v4/thepub/local"
LOCAL_PARAMS = "&lat={}&lng={}&radius=75"

user_data = []
user_id = 0

@app.route("/post", methods=["POST"])
def post():

    req_data = request.get_json()
    location = json.dumps(req_data)
    location_data = json.loads(location)

    lat = location_data['lat']
    lon = location_data['lon']

    user_data.append(location_data)

    global user_id

    user_id = user_id + 1

    print(user_data, user_id)

    response = 'SUCCESS'

    return response

@app.route("/", methods=["GET", "POST"])
def home():

    api_url = TRENDING + API_PARAMS.format(CLIENT_ID, CLIENT_SECRET)
    trending_response = urllib.request.urlopen(api_url)
    json_data = trending_response.read()
    data = json.loads(json_data)

    beers = data['response']['macro']['items']

    return render_template("home.html", beers=beers)

@app.route("/local", methods=["GET"])
def local():

    print(user_id)

    user_location = user_data[user_id-1]
    lat = user_location['lat']
    lon = user_location['lon']

    local_url = LOCAL + API_PARAMS.format(CLIENT_ID, CLIENT_SECRET) + LOCAL_PARAMS.format(lat, lon)
    local_response = urllib.request.urlopen(local_url)
    json_data = local_response.read()
    data = json.loads(json_data)
    local_beers = data['response']['checkins']['items']

    return render_template("home.html", beers=local_beers)

if __name__ == "__main__":
    if 'liveconsole' not in gethostname():
        app.run(debug=True)
