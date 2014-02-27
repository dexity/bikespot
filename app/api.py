import urllib
import urllib2
import json

from . import app

class Step(object):

    def __init__(self, num, step):
        self.num = num
        self.distance = step["distance"]["text"]
        self.duration = step["duration"]["text"]
        self.path = step["polyline"]["points"]
        sl = step["start_location"]
        el = step["end_location"]
        self.start_location = (sl["lat"], sl["lng"])
        self.end_location = (el["lat"], el["lng"])
        self.html_instructions = step["html_instructions"]

    def __str__(self):
        return self.html_instructions

    def to_dict(self):
        return dict(
            step=self.num,
            direction=self.html_instructions,
            distance=self.distance,
            duration=self.duration,
            polyline=self.path
        )


class DirectionsAPI(object):

    def __init__(self, origin, destination):
        self.origin = origin
        self.destination = destination
        self.total_distance = None
        self.total_duration = None
        self.directions = []


    def query(self):
        "Makes query to Directions API and populations directions list"
        cls = self.__class__
        orig = cls.to_latlng(self.origin)
        dest = cls.to_latlng(self.destination)
        data = cls.make_request(orig, dest)
        routes = data["routes"]
        if len(routes) == 0:
            return
        leg = routes[0]["legs"][0]
        self.total_distance = leg["distance"]["text"] # Example: 94.9 mi
        self.total_duration = leg["duration"]["text"] # Example: 1 hour 38 mins
        steps = leg["steps"]

        for i in range(len(steps)):
            self.directions.append(Step(i+1, steps[i]))


    def to_backbone(self):
        "Return json response for backbone"
        return json.dumps(dict(
            directions=[step.to_dict() for step in self.directions],
            meta=dict(
                total_distance=self.total_distance,
                total_duration=self.total_duration
            )
        ))


    @classmethod
    def to_latlng(cls, latlng):
        return "{},{}".format(*latlng)


    @classmethod
    def make_request(cls, origin, destination):
        endpoint = "https://maps.googleapis.com/maps/api/directions/json"
        params = dict(
            origin = origin,
            destination = destination,
            sensor = "false",     # Change to "true"?
            mode = "bicycling",
            key = app.config["GOOGLE_DIRECTIONS_KEY"],
        )
        url = "%s?%s" % (endpoint, urllib.urlencode(params))
        resp = urllib2.urlopen(url)
        return json.loads(resp.read())