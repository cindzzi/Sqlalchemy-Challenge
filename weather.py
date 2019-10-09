import numpy as np
import datetime as dt
import sqlalchemy 
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
#We can view all of the classes that automap found
Base.classes.keys()
# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station
# Create our session (link) from Python to the DB
session = Session(engine)
app = Flask(__name__)

# Flask Routes

@app.route("/")
def welcome():
    """List all available routes"""
    return (
        f"Welcome to Climate Starter<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
    )
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # return query results
    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    last_months = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= query_date).\
        order_by(Measurement.date).all()

    session.close()
    # create a dictionary using date as key and prcp as values
    prcp_results = []
    for prcp, date in last_months:
        prcp_one = {}
        prcp_one["date"] = date
        prcp_one["prcp"] = prcp
        prcp_results.append(prcp_one)

    return jsonify (prcp_results)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # return list of stations
    stations = session.query(Measurement.station, func.count(Measurement.station)).group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).all()

    session.close()

    # jsonify
    all_stations = list(np.ravel(stations))

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # return list of temperature and dates for the busiest station
    most_active_stations = session.query(Measurement.station, func.count(Measurement.station)).group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).all()

    busiest_station2 = most_active_stations[0][0]

    station_temp = session.query(Measurement.date, Measurement.tobs).group_by(Measurement.date).\
        filter(Measurement.station == busiest_station2).\
        filter(Measurement.date <= '2017-08-23').filter(Measurement.date >= '2016-08-23').all()

    session.close()

    # jsonify
    station_temp = list(np.ravel(station_temp))

    return jsonify(station_temp)

if __name__ == "__main__":
    app.run(debug=True)