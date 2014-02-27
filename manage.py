import json
import urllib2
from flask.ext.script import Manager
from app import app, db
from app.models import Parking

manager = Manager(app)

@manager.command
def load_datasf():
    """
    Populates bicycle parking data from DataSF
    See: https://data.sfgov.org/Transportation/Bicycle-Parking-Public-/w969-5mn4
    """
    # Get DataSF data
    try:
        data_url = "http://data.sfgov.org/resource/w969-5mn4.json"
        resp = urllib2.urlopen(data_url)
        data = resp.read()  # Load all data in memory for small data
        parkings = json.loads(data)
    except IOError, e:
        return

    # Populate database with the data
    for i in range(len(parkings)):
        parking = parkings[i]
        print u"{}. {}".format(i, parking["location_name"])
        db.session.add(Parking(parking))
    db.session.commit()


@manager.command
def init_db():
    db.create_all()
    db.session.commit()


if __name__ == "__main__":
    manager.run()
