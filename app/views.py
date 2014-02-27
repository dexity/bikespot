from flask import render_template, request, jsonify
from . import app
from .api import DirectionsAPI
from .models import Parking, get_nearest, point2latlng

@app.route("/")
def index():
    return render_template("index.html", api_key=app.config["GOOGLE_MAPS_KEY"])


@app.route("/directions")
def directions():
    "Returns directions to the nearest parkings"
    try:
        (lat, lng) = request.args.get("origin", "").split(",")
        origin = (lat, lng)
    except ValueError:
        return "Invalid location", 400

    # Find the nearest parking location from DataSF
    parking = get_nearest(*origin)
    destination = point2latlng(parking.geom)

    # Get directions from the current location to nearest parking
    dir = DirectionsAPI(origin, destination)
    dir.query()
    return dir.to_backbone()


@app.route("/parkings")
def parkings():
    "Returns list of bike parkings within the range"
    num = 50
    try:
        (lat, lng) = request.args.get("origin", "").split(",")
        origin = (lat, lng)
        # Display 50 nearest parkings from DataSF
        parkings = get_nearest(*origin, num=50)
    except ValueError:
        parkings = Parking.query.all()[:50]

    resp = []
    for parking in parkings:
        resp.append(parking.to_info())
    return jsonify(dict(data=resp))

