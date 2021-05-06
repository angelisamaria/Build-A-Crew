# Build a Crew

Build a crew is a place for Video Producers to manage their projects, crewmembers and callsheets all in one place. Film Producers have multiple projects, names, roles, emails and dates they need to keep track of. In working with lots of talent, it is easy to lose track of a crewmember's availability, their contact information and their location. This results in multiple back-and-forth emails, spreadsheets, folders and manual sharing of documents. Build-a-Crew is meant to provide ease for a Film Producer, tracking their projects, crewmembers and schedules all in one place. 


## Navigation

* [Tech Stack](#tech-stack)
* [Setup and Installation](#setup)
* [Navigate and Interact with the Application](#usage)
* [Next Steps](#next)

## <a name="tech-stack"></a>Tech Stack

* __Frontend:__ HTML5, CSS3, JavaScript, Bootstrap, Jinja, jQuery
* __Backend:__ Python, Flask, PostgreSQL, SQLAlchemy, [Faker](https://faker.readthedocs.io/en/master/) to seed database with mock data
* __API:__ DarkSky


## <a name="installation"></a>Setup/Installation

Please be sure to have __Python 3.6__ and __PostgreSQL__ downloaded before you clone this repository.

To run Build a Crew on your local computer, please follow the below steps:

Clone repository (HTTPS/SSH/CLI):
```
$ git clone https://github.com/angelisamaria/Build-A-Crew.git
```
Create a virtual environment in the BuildACrew folder:
```
$ python3 -m venv env
```
Activate virtual environment:
```
$ source env/bin/activate
```
(to deactivate the virtual environment, simply type `deactivate` in your shell)
Install dependencies:
```
$ pip install -r requirements.txt
```
Confirm you have PostgreSQL installed locally, otherwise follow [these steps](https://www.postgresql.org/download/). Once you've confirmed PostgreSQL is installed, create a new database:
```
$ createdb buildacrew
```
Build database tables:
```
$ python3 model.py
```
Fill database with seed file:
```
$ python3 seed.py
```
Run the app via command line:
```
$ python3 server.py
```
## <a name="usage"></a> Navigate and Interact with the Application

### Step 1: Create profile
* Register via landing page

### Step 2: Create a project
* Create new project via To-Do list
* Add additional projects via Projects page > [ + Project ]

### Step 3: Add crewmembers
* Drag and drop users into Crew for your specific project

### Step 4: Dashboard
* Add additional items to To-Do list
* View # crewmembers you are working with
* View weather with DarkSky API based on your location
* View Chart.js data visualizing your projects & crew

## <a name="next"></a> Next Steps
* User-to-user interaction
* Upload option for profile photos or provide an option with default images
* Exporting callsheets as PDF
* Google Docs integration: Calendar, Docs and Sheets