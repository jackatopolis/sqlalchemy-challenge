# Climate App
# By: Jack Cohen

# Import Dependencies
import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
import datetime as dt

# Database Setup
engine = create_engine("sqlite:///hawaii.sqlite")
Base = automap_base()
Base.prepare(engine,reflect=True)
Station = Base.classes.station
Measurement = Base.classes.measurement

# Create app
app = Flask(__name__)

# Define routes
@app.route("/")
def home():
    print("Server received request for 'Home' page...")
    return (
        f"Welcome to the Climate homepage!<br/>"
        f"<br/>"
        f"Routes available:<br/>"
        f"<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start-date<br/>"
        f"/api/v1.0/start-date/end-date<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    print("Server received request for 'Precipitation' page...")
    session = Session(engine)
    results = session.query(Measurement.date,Measurement.prcp).all()
    session.close()

    res_dict = {}
    for x in range(len(results)):
        res_dict[results[x][0]] = str(results[x][1])
    
    return jsonify(res_dict)

@app.route("/api/v1.0/stations")
def stations():
    print("Server received request for 'Stations' page...")
    session = Session(engine)
    results = session.query(Station.name).all()
    session.close()
    
    all_stations = list(np.ravel(results))
    
    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    print("Server received request for 'Temperature Observation' page...")
    session = Session(engine)
    m_stations = session.query(Measurement.station).all()

    sta = []
    for x in range(len(m_stations)):
        sta.append(m_stations[x][0])
    active_stations = pd.Series(sta).value_counts()
    df = pd.DataFrame(active_stations,columns=['Frequency'])
    df.dropna(inplace=True)
    df.reset_index(inplace=True)
    df.rename(columns={'index':'Station'},inplace=True)
    most_active_station = df.loc[df['Frequency']==df['Frequency'].max()]['Station'][0]

    query_date = dt.date(2017,8,23)-dt.timedelta(days=365)
    
    sel = [Measurement.date,Measurement.tobs]
    temp_info = session.query(*sel).\
        filter(Measurement.date >= query_date).\
        filter(Measurement.station==most_active_station)

    session.close()
    
    return jsonify(temp_info.all())

@app.route("/api/v1.0/<start_date>/<end_date>")
def startend(start_date,end_date):
    print("Server received request for 'Temperature Range' page...")
    
    session = Session(engine)
    
    sel = [func.min(Measurement.tobs),
       func.max(Measurement.tobs),
       func.avg(Measurement.tobs)]
    temp_year = session.query(*sel).\
        filter(Measurement.date >= start_date).\
        filter(Measurement.date <= end_date).\
        filter(Measurement.station=='USC00519281')

    session.close()
    
    temps={}
    temps['min']=temp_year[0][0]
    temps['max']=temp_year[0][1]
    temps['avg']=temp_year[0][2]

    return jsonify(temps)
    

@app.route("/api/v1.0/<start_date>")
def start(start_date):
    print("Server received request for 'Temperature Range' page...")          
    
    session = Session(engine)
    
    sel = [func.min(Measurement.tobs),
       func.max(Measurement.tobs),
       func.avg(Measurement.tobs)]
    temp_year = session.query(*sel).\
        filter(Measurement.date >= start_date).\
        filter(Measurement.station=='USC00519281')

    session.close()
    
    temps={}
    temps['min']=temp_year[0][0]
    temps['max']=temp_year[0][1]
    temps['avg']=temp_year[0][2]

    return jsonify(temps)


if __name__ == "__main__":
    app.run(debug=True)
    
    
