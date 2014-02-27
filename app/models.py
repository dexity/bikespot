import json
import geoalchemy2.functions as func
from geoalchemy2 import Geometry
from geoalchemy2.elements import WKTElement
from . import db


class Parking(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    placement = db.Column(db.String(100))
    racks_installed = db.Column(db.Integer)
    spaces = db.Column(db.Integer)
    racks = db.Column(db.String(100))
    location_name = db.Column(db.String(100))
    status_description = db.Column(db.String(100))
    status = db.Column(db.String(100))
    yr_installed = db.Column(db.String(10))
    status_detail = db.Column(db.String(100))
    installed_by_2 = db.Column(db.String(100))
    yr_inst = db.Column(db.String(100))
    acting_agent = db.Column(db.String(100))
    action = db.Column(db.String(100))
    bike_parking = db.Column(db.String(100))
    geom = db.Column(Geometry(geometry_type="POINT", srid=4326))


    def __init__(self, p):
        cls = self.__class__
        self.placement = p.get("placement", "")
        self.racks_installed = cls.to_int(p.get("racks_installed", ""))
        self.spaces = cls.to_int(p.get("spaces", ""))
        self.racks = p.get("racks", "")
        self.location_name = p.get("location_name", "")
        self.status_description = p.get("status_description", "")
        self.status = p.get("status", "")
        self.yr_installed = p.get("yr_installed", "")
        self.status_detail = p.get("status_detail", "")
        self.installed_by_2 = p.get("installed_by_2", "")
        self.yr_inst = p.get("yr_inst", "")
        self.acting_agent = p.get("acting_agent", "")
        self.action = p.get("action", "")
        self.bike_parking = p.get("bike_parking", "")
        lat = p["coordinates"].get("latitude", "")
        lng = p["coordinates"].get("longitude", "")
        self.geom = "SRID=4326;POINT({} {})".format(lng, lat)


    def to_info(self):
        return dict(
            location_name=self.location_name,
            bike_parking=str(self.bike_parking).capitalize(),
            status=" ".join([w.capitalize() for w in str(self.status_detail).split("_")]),
            acting_agent=self.acting_agent,
            location=point2latlng(self.geom)
        )

    @classmethod
    def to_int(cls, val):
        try:
            return int(val)
        except ValueError:
            return -1


def get_nearest(lat, lng, num=1):
    """
    Find the nearest point to the coordinates
    Convert the coordinates to a WKT point and query for nearest point
    """
    point = WKTElement("POINT({} {})".format(lng, lat), srid=4326)
    parkings = Parking.query.order_by(Parking.geom.distance_box(point))
    if num == 1:
        return parkings.first()
    return parkings[:num]


def point2latlng(point):
    "Converts point to lat and lng"
    geom_json = json.loads(db.session.scalar(func.ST_AsGeoJSON(point)))
    coords = geom_json['coordinates']
    coords.reverse()
    return coords

