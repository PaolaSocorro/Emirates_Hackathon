from flask_sqlalchemy import SQLAlchemy
import psycopg2

import os, requests, json

db = SQLAlchemy()

# XOLA_API_KEY = os.environ["XOLA_API_KEY"]

# this is for airport codes database
class AirportCode(db.Model):
    """Airport code for departure and arrival destinations."""

    __tablename__ = "airportcodes"

    code = db.Column(db.String(3), primary_key=True)
    location = db.Column(db.String(50), nullable=False)
    longitude = db.Column(db.Float)
    latitude = db.Column(db.Float)


    def __repr__ (self):
        """Statement when printed."""

        return "<Object Airport Code:%s for %s>" % (self.code, self.location)

class Experience(db.Model):
    """Xola experiences"""
    __tablename__ = "expereinces"

    id = db.Column(db.String(50), primary_key=True)
    longitude = db.Column(db.Float)
    latitude = db.Column(db.Float)

    def __repr__(self):

        return "<Object experience id: %s>" % (self.id)

    @classmethod
    def get_experience_by_lat_long(cls, original_lat, original_lng):
        """given the original latitude and longitude, output a list of experience objects that are within the range"""
        lower_lat = original_lat - 1
        higher_lat = original_lat + 1

        lower_lng = original_lng - 1
        higher_lng = original_lng + 1

        query_lat_lng = cls.query.filter(cls.latitude <= higher_lat, cls.latitude >= lower_lat,
                                         cls.longitude <= higher_lng, cls.longitude >= lower_lng).limit(5).all()

        return query_lat_lng

    @classmethod
    def get_experience_by_id(cls, id):
        return cls.query.get(id)

    def get_detailed_info(self):
        """get the detailed info for a specific experience object"""
        headers = {
        'Content-type':'application/json'
    }
        url = 'https://dev.xola.com/api/experiences/' + self.id
        r = requests.get(url, headers=headers, verify=False)
        experience = json.loads(r.text)

        return experience




#########THIS CONNECTS TO DATABASE SO WE CAN WORK INTERACTIVELY IN CONSOLE

def connect_to_db(app):
    """Connect the database to our Flask app."""


    DATABASE_URL = os.environ.get("DATABASE_URL",
                              "postgresql://localhost/emirates")
    # Configure to use SQLite database
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///airportandcampsites.db'
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
    db.app = app
    db.init_app(app)



if __name__ == "__main__":
# allows working with the database directly

    from server import app
    connect_to_db(app)
    print "Connected to DB."

