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
The core of Sauron is its SQL database. The schema definition of this database is located in [`create_db.sql`](create_db.sql).  

## SQL Database
The database tracks two types of data: Sources and Event Reports.  
A "Source" in Sauron represents a event data source such as a camera, drone, sensor or human reporter.  

Event Reports describe some sort of disaster-related event. Each Event Report has a timestamp, event type, and can have a description, geographic coordinates, and an attached image (frame) of the event being reported.

For the hackathon, we used GCP's Cloud SQL to host the database.

## Flask REST API
Event data is added to Sauron's database through either a direct SQL connection to the database, or by using a rudimentary Flask REST API to upload an Event Report.

This Flask REST API is located in the `flask-app` directory.  
There are only a few endpoints:
| URL | Method | Description  |
| ----| ------ |------------- |
| `/` | `POST` | Endpoint to add Event Reports. |
| `/` | `GET`  | HTML form for adding Event Reports. |
| `/clear` | `GET` | Clears all Event Reports. |
| `/clearall` | `GET` | Clears all Event Reports and Sources. |


