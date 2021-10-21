# Climate Analysis for Trip Planning


## Background
The goal of this project is to conduct a climate analysis to help with trip planning. The climate data was explored and analyzed using Python, SQLAlchemy ORM queries, Pandas, and Matplotlib.

## Details
* Use SQLAlchemy `create_engine` to connect to sqlite database
* Link Python to the database by creating an SQLAlchemy session
* Precipitation Analysis:
    * Retrieve the last 12 months of precipitation data
    * Organize query results and load into Pandas DataFrame
    * Plot results for precipitation ocer time
    * Print summary statistics for precipitation data
* Station Analysis
    * Conduct analysis on weather stations
    * Query the most active station
    * Plot results as a histogram with bins
* Design multi-route Flask API to display data
    * `/` - Homepage that lists routes available
    * `/api/v1.0/precipitation` - 
