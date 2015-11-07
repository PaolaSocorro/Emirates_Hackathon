from flask_sqlalchemy import SQLAlchemy
import psycopg2

import os

db = SQLAlchemy()


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

