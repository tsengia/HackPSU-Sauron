# HackPSU-Sauron
Entry for [HackPSU](https://hackpsu.org/) Spring 2022.

Minimal Viable Product of an computer vision/AI/ML powered disaster event data aggregator.  
Powered by OpenCV, Google Cloud Platform, and Flask.  

# 🏆 Awards 🏆  
- 🥇 Won HackPSU 1st Place prize!  
- 🥇 Won the Nittany AI Challenge 1st Place prize!  

# Team Members
- Tyler Sengia
- Normen Yu
- Ralph Quartiano
- Jared Armagonst
- Michael Da Rocha

Check out [the hackathon](https://hackpsu-spring-2022.devpost.com/) and [our submission](https://devpost.com/software/sauron-ke72by) on DevPost.

# Architecture
The Sauron MVP has four main components:
- SQL Database
- Flask REST API
- Grafana Dashboard
- YouTube Event Source Demo

## SQL Database
The core of Sauron is its SQL database. The schema definition of this database is located in [`create_db.sql`](create_db.sql).  
The database tracks two types of data: Sources and Event Reports.  
A "Source" in Sauron represents a event data source such as a camera, drone, sensor or human reporter.  

Event Reports describe some sort of disaster-related event. Each Event Report has a timestamp, event type, and can have a description, geographic coordinates, and an attached image (frame) of the event being reported.

For the hackathon, we used GCP's Cloud SQL to host the database.

## Flask REST API
Event data is added to Sauron's database through either a direct SQL connection to the database, or by using a rudimentary Flask REST API to upload an Event Report.

This Flask REST API is located in the `flask-app` directory.  
There are only a few endpoints:
| URL | Method | Description  |
| ---:| ------ |:------------ |
| `/` | `POST` | Endpoint to add Event Reports. |
| `/` | `GET`  | HTML form for adding Event Reports. |
| `/clear` | `GET` | Clears all Event Reports. |
| `/clearall` | `GET` | Clears all Event Reports and Sources. |


## Grafana Dashboard
Users of Sauron are able to view Event Reports through a [Grafana Dashboard](https://grafana.com/grafana/).  
Our dashboard is defined in [`grafana-dashboard.json`](grafana-dashboard.json).

We made extensive use of Grafana's [GeoMap visualization](https://grafana.com/docs/grafana/latest/panels-visualizations/visualizations/geomap/).

Using the GeoMap, users can see where Event Reports are located, and can click on an event report to be taken to the image frame associated with that event.  There are also Table visualizations used to list the Event Reports and Event Sources individually.  

## YouTube Event Source Demo
To demonstrate Sauron's ability to aggregate event data, we created a simple Python script ([`detect-incidents-hardcoded.py`](detect-incidents-hardcoded.py)) to stream video from multiple YouTube livestreams of traffic. We stream the video by spawning a subprocess that runs [youtube-dl](https://youtube-dl.org/) on the Youtube livestream.  

This Python script acts as through it is a traffic camera reporting events to Sauron.  
Every few seconds, the Python script will randomly select a video frame to use as an Event Report, and adds a timestamp and location and submits it to the Sauron Event Report Database.



# Limitations
This project is purely a prototype, but here are some things we would add if this project were to continue:
1. Real anomaly detection for cameras
2. Authentication and Authorization (currently no requests/commands are authenticated)
3. Add API endpoint for adding Event Sources
4. Add API endpoints for retrieving data
