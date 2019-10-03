import datetime as dt
import numpy as np
import pandas as pd

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

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station
# Create our session (link) from Python to the DB
session = Session(engine)
# Flask Setup
app = Flask(__name__)

# Flask Routes
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"<p>Welcome to the Hawaii weather API!</p>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/temp/start<br/>"
        f"/api/v1.0/temp/start/end"        
    )

@app.route("/api/v1.0/precipitation")
def precipitation():  

    """Return a query """
    # Query to retrieve the last 12 months of precipitation data and plot the results
    last_months = session.query(Measurement.date,(Measurement.prcp)).\
    filter(Measurement.date >= query_date ).\
    order_by(Measurement.date).all()

    # Convert 
    precipitation_list = list(np.ravel(results))

    return jsonify(precipitation_list)
    
    #create JSON results
        

@app.route("/api/v1.0/stations")
    #"""Return a list of stations from the dataset"""
def stations():
    # Query stations
    stations= session.query(Station.station).all()
    stations2 = list(np.ravel(station_name))
    return jsonify(stations2

@app.route("/api/v1.0/Tobs")    
 #  """ query for the dates and temperature observations from a year from the last data point.
  #* Return a JSON list of Temperature Observations (tobs) for the previous year."""
        # Calculate the date 1 year ago from the last data point in the database                   
# def tobs():
#     query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
#     temp_observations=session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= query_date).all()
#     Temp_observations = {date: tobs for date, tobs in temp_observations}
#     return jsonify(Temp)               
                   
@app.route("/api/v1.0/Temp_observations<start>/<end>" )    
# def date_start_end():
#  #       """ Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
# #  * When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date.
#  # * When given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` for dates between the start and end date inclusive. """
        
#      record= [func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)]
#      Start&End = session.query(record)filter(Measurement.date>= start).filter(Measurement.date<=end).all()
#      temp_OB=list(np.ravel(Start&End))
#      temp_OB
#      return jsonify(temp_OB)         


if __name__ == '__main__':
    app.run(debug=True)




