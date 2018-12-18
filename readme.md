# Build a Crew
Build a crew is a place for Video Producers to manage their projects, crewmembers and callsheets all in one place.

![Image of Crew](http://i65.tinypic.com/2ahh46w.gif)

## Problem

Film Producers have multiple projects, names, roles, emails and dates they need to keep track of. In working with lots of talent, it is easy to lose track of a crewmember's availability, their contact information and their location. This results in multiple back-and-forth emails, spreadsheets, folders and manual sharing of documents.

## Solution

Build-a-Crew is meant to provide ease for a Film Producer, tracking their projects, crewmembers and schedules all in one place. 

### Step 1: Create profile
Users create a profile with basic information to log in and track their projects.

### Step 2: Create a project
Creating a project is simple and lives in their user dashboard.

### Step 3: Add crewmembers
Using the Jquery UI library's Draggable and Sortable, Producers and drag and drop users from the user table directly into the crews table via AJAX. Each users name, role and image are shown.

### Step 4: Dashboard
Users can view their project progress in the dashboard, their to-do list based on SQLAlchemy queries that quantify their project data. They are also given a visual representation of their project progress via Chart.js.

## Features
### MVP features
- Create Profile - username, password, portfolio or LinkedIn, skillset (role) and location
- Create Project - title, logline, start date and end date
- Manage Crew - Drag users to Crew for specific project
- Manage Callsheets - Add callsheets to specific project

### 2.0
- Dark Sky API - Weather for the day, both for the user and for each callsheet shoot date
- Chart JS - Data visualization of project and crew progress
- To-Do list - taken from Postgres database using SQLAlchemy + user additions

### Future
- User-to-user interaction
- Local resources page
- Sharing callsheet PDF's via email
- Calendar invites
- Location scouting
- Project brainstorm forum/message board

## Languages/Frameworks/Libraries/Tools
- Python
- Flask
- SQL (SQLAlchemy)
- PostgreSQL
- Bootstrap
- HTML5
- CSS3
- JavaScript
- Dark Sky API
- Chart JS
- Jquery UI Library (Draggable & Sortable)

## Database

### Table: User
- user_id*
- First name
- Last name
- Email
- Password
- Portfolio or LinkedIn
- Profile image

### Table: Project
- project_id*
- user_id (fk)
- Title
- Logline
- Start Date
- End Date
- Project image URL

### Table: Crew
- crew_id*
- project_id (fk)

