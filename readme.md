# Build a Crew

![Image of Crew](http://i65.tinypic.com/2ahh46w.gif)

Build a crew is a place for Video Producers to manage their projects, crewmembers and callsheets all in one place. Film Producers have multiple projects, names, roles, emails and dates they need to keep track of. In working with lots of talent, it is easy to lose track of a crewmember's availability, their contact information and their location. This results in multiple back-and-forth emails, spreadsheets, folders and manual sharing of documents. Build-a-Crew is meant to provide ease for a Film Producer, tracking their projects, crewmembers and schedules all in one place. 


## Navigation

* [Tech Stack](#tech-stack)
* [Setup and Installation](#setup)
* [Usage](#usage)
* [Version 2.0](#version2point0)

## <a name="tech-stack"></a>Tech Stack

__Frontend:__ HTML5, CSS3, JavaScript, Bootstrap, Jinja, jQuery
__Backend:__ Python, Flask, PostgreSQL, SQLAlchemy
__APIs:__ DarkSky
__Testing:__ Selenium


## <a name="installation"></a>Setup/Installation

#### Requirements:
- PostgreSQL
- Python 3.6

To run Build a Crew on your local computer, please follow the below steps:

Clone repository:
```
$ git clone https://github.com/angelisamaria/Build-A-Crew.git
```
Create a virtual environment in the UniMuse/UniMuse folder:
```
$ virtualenv env
```
Activate virtual environment:
```
$ source env/bin/activate
```
Install dependencies:
```
$ pip install -r BuildaCrew/requirements.txt
```
Create database 'buildacrew'.
```
$ createdb buildacrew
```
Create your database tables.
```
$ python3 models.py
```
Fill database with seed file.
```
$ python3 seed.py
```
Run the app from the command line.
```
$ python3 server.py
```
## <a name="usage"></a> Usage

### Step 1: Create profile
Users create a profile with basic information to log in and track their projects.

### Step 2: Create a project
Creating a project is simple and lives in their user dashboard.

### Step 3: Add crewmembers
Using the Jquery UI library's Draggable and Sortable, Producers and drag and drop users from the user table directly into the crews table via AJAX. Each users name, role and image are shown.

### Step 4: Dashboard
Users can view their project progress in the dashboard, their to-do list based on SQLAlchemy queries that quantify their project data. They are also given a visual representation of their project progress via Chart.js.

## <a name="future"></a> Next Steps - Version 2.0
* User-to-user interaction
* Exporting callsheets as PDF
* Calendar invites
* Google Docs integration