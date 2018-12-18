# Build a Crew
Build a crew is a place for Video Producers to manage their projects, crewmembers and callsheets all in one place.


## Solution:

Step 1: Create profile
Your role
Your portfolio
Headshot
Skillset
Connect to Facebook
Add connections
LinkedIn profile
Email
Contact phone #
Status: Seeking work, seeking [crew type]
Rates (range OK?)
User to user: reviews, endorsements

Step 2: Create a posting
Project info
Dates
Location
Crew needed
Rates
Required skills

Step 3: Book a gig
Search gigs
Apply - matches your skill set
Green vs red: still available/closed

Step 4: Review booking request (hiring)
Green vs red:
Matching skills
Matching location
Matching pay range
Portfolio info
Read reviews

Step 5: Book a crew member
Select crew type
Select pay range
Select availability times
Select locations

Step 6: Review
Review crew member after gig
Add to preferred connections
Payment

## Features
### MVP features
Create Profile - username, password, portfolio or LinkedIn, skillset (role) and location
Create Project - title, logline, start date and end date
Manage Crew - Drag users to Crew for specific project
Manage Callsheets - Add callsheets to specific project

### 2.0
Dark Sky API - Weather for the day, both for the user and for each callsheet shoot date
Chart JS - Data visualization of project and crew progress
To-Do list - taken from Postgres database using SQLAlchemy + user additions

### Future
User-to-user interaction
Local resources page
Sharing callsheet PDF's via email
Calendar invites
Location scouting
Project brainstorm forum/message board

## Tools
- Dark Sky API
- Chart JS
- Jquery UI Library

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

