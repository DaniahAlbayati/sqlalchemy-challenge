import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement= Base.classes.measurement
Station = Base.classes.station



#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
            )


#Convert the query results to a dictionary using `date` as the key and `prcp` as the value.
# Create our session (link) from Python to the DB

@app.route("/api/v1.0/precipitation")
def precipitations():
    session = Session(engine)
    
    query_date=session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    
    session.close()
    
    query_date = query_date[0]
    query_date = dt.datetime.strptime(query_date,'%Y-%m-%d').date()
    start_date= query_date - dt.timedelta(days=365)
    result = session.query(Measurement.date,Measurement.prcp).\
        filter(Measurement.date > start_date).all()
    prcp={date:prcp for date,prcp in result}
    return jsonify (prcp)

 
#Return a JSON list of stations from the dataset.
@app.route("/api/v1.0/stations")
def stations():
    
    session = Session(engine)
    
    query = session.query(Station.name).all()
    
    session.close()
    
    result=list(np.ravel(query))
    return jsonify(result)
    

#Query the dates and temperature observations of the most active station for the last year of data.
#Return a JSON list of temperature observations (TOBS) for the previous year.
    
@app.route("/api/v1.0/tobs")
def tobs():
    
        session = Session(engine)
        query = session.query(Measurement.date,Measurement.tobs).\
        filter(Measurement.date>="2016-08-23").\
        filter(Measurement.date<="2017-08-23").all()
        
        session.close()
        
        result=list(np.ravel(query))
        return jsonify(result)


    
#Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
# When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date.
#When given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` for dates between the start and end date inclusive.

@app.route("/api/v1.0/<start><br/>")
def start():
    
    session = Session(engine)
    query= session.query((Measurment.date, func.min(Measurement.tobs),func.avg(Measuremnet.tobs),func.max(Measurement.tobs)).\
    filter(Meausrement.date)>=date).all()
    
    session.close()
    
    return jsonify(result)
    
if __name__ == '__main__':
app.run(debug=True)
    
    
    
        