from jinja2 import StrictUndefined
from flask import (Flask, render_template, redirect, request, flash,
                   session, jsonify)
from flask_debugtoolbar import DebugToolbarExtension

# initialize server
from model import User, Project, Crew, Callsheet, Schedule, Location, connect_to_db, db


# for darksky API
import time
from datetime import date, datetime
import requests
import random

# DarkSkyAPI variables for User Dashboard
days = {0: 'Sunday',
                1: 'Monday', 
                2: 'Tuesday', 
                3: 'Wednesday', 
                4: 'Thursday', 
                5: 'Friday',
                6: 'Saturday'}

months = { 1 : "January", 
                2 : "February", 
                3 : "March", 
                4 : "April", 
                5 : "May", 
                6 : "June", 
                7 : "July",
                8 : "August",
                9 : "September", 
                10 : "October", 
                11 : "November",
                12 : "December" } 


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """ Homepage, will prompt users to login or register."""
    
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        return render_template("projects/dashboard.html", user=user)
    else:
        users = User.query.all()
        return render_template("homepage.html", users=users)

@app.route('/register', methods = ['GET', 'POST'])
def registration_form():
    """Allow users to register, only their email and pw is required. """
    
    if request.method == 'GET':
        return render_template("/users/register.html")

    else:
        user_email = request.form.get("email")
        pw = request.form.get("pw")
        fname = request.form.get("fname")
        lname = request.form.get("lname")
        zipcode = request.form.get("zipcode")
        picture = request.form.get("picture")
        linkedin = request.form.get("linkedin")
        role = request.form.get("role")
        new_user = User(email=user_email, 
                            pw=pw,
                            fname=fname,
                            lname=lname,
                            zipcode=zipcode,
                            linkedin=linkedin,
                            role=role,
                            picture=picture)
                            
        db.session.add(new_user)
        db.session.commit()

        # session['user_id'] = request.form['user_id']
        session['user_id'] = new_user.user_id

        return redirect('/dashboard')

@app.route('/getusers', methods=['GET'])
def view_users():
    """ View all users. """

    users = User.query.all()
    allUsers = {}
    for i, user in enumerate(users):
        allUsers[i] = {}
        allUsers[i]['firstname'] = user.fname
        allUsers[i]['lastname'] = user.lname
        allUsers[i]['role'] = user.role
        allUsers[i]['user_id'] = user.user_id
    return jsonify(results=allUsers)

# user login
@app.route('/login', methods=['GET', 'POST'])
def log_in():
    """ User login. """

    if request.method == 'GET':
        return render_template("/users/login.html")

    else:
        email = request.form.get("email")
        pw = request.form.get("pw")

        #check if user email is in database
        if User.query.filter(User.email == email).first():
            #password validation
            user = User.query.filter(User.email == email).first()
            if user.pw == pw:
                session['user_id'] = user.user_id
                return redirect(f'dashboard')
            else: 
                return render_template("/users/login.html")
        else:
            return redirect('/register')


@app.route('/logout')
def log_out():
    """ User logout. """
    del session['user_id']
    flash('You are logged out.')

    return redirect('/')

@app.route('/dashboard')
def user_dashboard():
    """User's Dashboard Page."""

    # squalchemy from Users Projects, and Crews tables
    user = User.query.get(session['user_id'])
    user_projects = Project.query.filter_by(user_id=session['user_id'])
    specific_project = Project.query.filter_by(user_id=session['user_id']).first()
    numprojects = Project.query.filter_by(user_id=session['user_id']).count()
    crewed = Project.query.filter_by(user_id=session['user_id']).join(Crew, Crew.project_id == Project.project_id).count()

    # datetime for user view
    now = datetime.now()
    theday = now.today().weekday()
    date = now.day

    if 10 <= date % 100 < 20:
        today_date = str(date) + 'th'
    else:
       today_date = str(date) + {1 : 'st', 2 : 'nd', 3 : 'rd'}.get(date % 10, "th")


    # DarkSkyAPI
    r = requests.get("https://api.darksky.net/forecast/0b4f58622393c96c8910335b6428dda2/33.993396,-118.465193")
    weather = r.json()
    currently = weather['currently']
    current_temp = int(currently['temperature']) #66.51
    current_icon = currently['icon'] # clear-sky 
    current_summary = currently['summary'] # clear skies
    icons = {'clear-day': "fas fa-sun", 'clear-night': "fas fa-moon", 'rain': "fas fa-umbrella",'snow': "fas fa-snowflake",'fog': "fas fa-cloud",'wind': "fas fa-wind",'cloudy': "fas fa-cloud",'partly-cloudy-day': "fas fa-cloud-sun",'partly-cloudy-night': "fas fa-cloud-moon",'hail': "fas fa-cloud-showers-heavy",'thunderstorm': "fas fa-bolt",'tornado': "fas fa-umbrella" }
    icon = icons[current_icon] # fas fa-sun
    ts = int(currently['time'])
    month = now.month
    today_day = days[theday]
    today_month = months[month]
    # if you encounter a "year is out of range" error the timestamp
    # may be in milliseconds, try `ts /= 1000` in that case
    timeUnix = datetime.utcfromtimestamp(ts).strftime('%d/%m/%y')


    return render_template("/projects/dashboard.html", 
                            user=user, 
                            numprojects=numprojects, 
                            user_projects=user_projects,
                            current_temp=current_temp,
                            current_icon=current_icon,
                            current_summary=current_summary,
                            today_day=today_day,
                            today_month=today_month,
                            today_date=today_date,
                            icon=icon,
                            timeUnix=timeUnix,
                            crewed=crewed,
                            specific_project=specific_project)

@app.route('/projects')
def user_projects():
    """ View all user's owned projects. """

    user_projects = Project.query.filter_by(user_id=session['user_id'])
    crewmembers = Crew.query.all()
    numprojects = Project.query.filter_by(user_id=session['user_id']).count()
    crew = Crew.query.join(Project, Crew.project_id==Project.project_id).join(User, Project.user_id==session['user_id'])
    numcrew = Crew.query.join(Project, Crew.project_id==Project.project_id).join(User, Project.user_id==session['user_id']).count()
    callsheets = Callsheet.query.all()
    usercallsheets = User.query.join(Project, session['user_id']==Project.user_id).join(Callsheet, Project.project_id==Callsheet.project_id).count()
    
    return render_template("/projects/userprojects.html", 
                            user_projects=user_projects,
                            crew=crew,
                            callsheets=callsheets,
                            usercallsheets=usercallsheets,
                            numcrew=numcrew,
                            crewmembers=crewmembers,
                            numprojects=numprojects)

@app.route('/projects/<project_id>')
def view_project(project_id):
    """ View details of a specific project."""
    specific_project = Project.query.get(project_id)
    crew = Crew.query.filter_by(project_id=project_id)

    return render_template("/projects/project_id.html", specific_project=specific_project, crew=crew)

@app.route('/newproject', methods = ['GET', 'POST'])
def new_user_project():
    """ User can add a new project. """

    user_id = session['user_id']

    if request.method == 'GET':
        return render_template("/projects/newproject.html", user_id=user_id)

    else:
        title = request.form.get("title")
        sdate = request.form.get("sdate")
        edate = request.form.get("edate")
        proj_desc = request.form.get("proj_desc")
        user_id = request.form.get("user_id")
        proj_img = request.form.get("proj_img")
        new_proj = Project(title=title, 
                            sdate=sdate,
                            edate=edate,
                            proj_desc=proj_desc,
                            user_id=user_id,
                            proj_img=proj_img)
        db.session.add(new_proj)
        db.session.commit()

        return redirect("/projects")

@app.route('/user', methods=['GET', 'POST'])
def user():
    """ User view of their private profile. """

    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        if request.method == 'POST':
            user.fname = request.form['fname']
            user.lname = request.form['lname']
            user.email  = request.form['email']
            user.pw   = request.form['pw']

            db.session.commit()

        return render_template("/users/user.html", user=user)
   
    else:
        return render_template("homepage.html")

@app.route('/user/<user_id>')
def profile(user_id):
    """ User view of their public profiles. """

    specific_user = User.query.get(user_id)
    
    return render_template("/users/publicprofile.html", specific_user=specific_user)


@app.route('/callsheets/<project_id>',  methods=['GET', 'POST'])
def all_callsheets(project_id):
    """ User's contact list."""

    if request.method == 'POST':
        project_id = project_id
        day_number = request.form.get("day_number")
        shoot_date = request.form.get("shoot_date")
        lunch_time = request.form.get("lunch_time")
        lunch_location = request.form.get("lunch_location")
        hospital_name = request.form.get("hospital_name")
        hostpital_location = request.form.get("hostpital_location")
        parking_address = request.form.get("parking_address")
        newCallsheet = Callsheet(project_id=project_id, 
                            day_number=day_number,
                            shoot_date=shoot_date,
                            lunch_time=lunch_time,
                            lunch_location=lunch_location,
                            hospital_name=hospital_name,
                            hostpital_location=hostpital_location,
                            parking_address=parking_address)

        db.session.add(newCallsheet)
        db.session.commit()
        users = User.query.all()

    specific_project = Project.query.get(project_id)
    user_projects = Project.query.filter_by(user_id=session['user_id'])
    callsheets = Callsheet.query.all()
    
    return render_template("/projects/callsheets.html", callsheets=callsheets, 
                                specific_project=specific_project, 
                                user_projects=user_projects,
                                users=users)




@app.route('/callsheets/<project_id>/<callsheet_id>')
def view_callsheet(project_id, callsheet_id):
    """ User's contact list."""
    
    specific_callsheet = Callsheet.query.get(callsheet_id)
    specific_project = Project.query.get(project_id)
    user_projects = Project.query.filter_by(user_id=session['user_id'])
    user = User.query.filter_by(user_id=session['user_id'])
    crew = Crew.query.all()
    schedule = Schedule.query.all()
    location = Location.query.all()
    callsheet = Callsheet.query.all()

    r = requests.get("https://api.darksky.net/forecast/0b4f58622393c96c8910335b6428dda2/37.8267,-122.4233")
    weather = r.json()
    currently = weather['currently']
    current_temp = int(currently['temperature']) #66.51
    current_icon = currently['icon'] # clear-sky icon
    current_summary = currently['summary'] # clear skies


    return render_template("projects/callsheet_id.html", specific_project=specific_project,
                                specific_callsheet=specific_callsheet, user=user, crew=crew, 
                                current_temp=current_temp, current_icon=current_icon, 
                                current_summary=current_summary, schedule=schedule,
                                location=location)


@app.route('/contacts')
def view_contacts():
    """ User's contact list."""

    users = User.query.all()
    user_one = User.query.filter_by(user_id=1)

    return render_template("users/contacts.html", users=users, user_one=user_one)


# DONT DELETE
# @app.route('/crew/<project_id>', methods=['GET', 'POST'])
# def my_original_crew_route(project_id):
#     """ Crew Page"""
    
#     if request.method == 'POST':
#         project_id = project_id
#         user_id = request.form.get("user_id")
#         role = request.form.get("role")
#         crewMember = Crew(project_id=project_id, 
#                             user_id=user_id,
#                             role=role)
#         db.session.add(crewMember)
#         db.session.commit()



#     specific_project = Project.query.get(project_id)
#     user_projects = Project.query.filter_by(user_id=session['user_id'])
#     crew = Crew.query.filter_by(project_id=project_id)
#     crews = Crew.query.all()
#     users = User.query.all()
#     first_usr = User.query.first()

#     return render_template("/crews/crew.html", 
#                             specific_project=specific_project, user_projects=user_projects, 
#                             crew=crew, users=users, first_usr=first_usr)

# EDITED VERSION
@app.route('/crew/<project_id>')
def project_crew(project_id):
    """ Crew Page"""
    
    specific_project = Project.query.get(project_id)
    user_projects = Project.query.filter_by(user_id=session['user_id'])
    crew = Crew.query.join(Project, Crew.project_id==project_id).join(User, Project.user_id==session['user_id']).all()

    users = User.query.all()
    return render_template("/crews/crew.html", 
                                specific_project=specific_project, user_projects=user_projects, 
                                crew=crew, users=users)


    
        

# POST CREW
# @app.route('/addcrew', methods=['POST'])
# def add_crew():
#     """ Crew Page"""
    

#     fullname= request.form.get("fullname")
#     role = request.form.get("userrole")
#     role = request.form.get("userid")
#     project_id = project_id
#     new_crew = Crew(fullname=fullname, 
#                         project_id=project_id,
#                         role=role)
                        
#     db.session.add(new_crew)
#     db.session.commit()

#     return redirect('/crew/<project_id>')



# # GET CREW
@app.route('/getcrew', methods=['GET'])
def view_crew():
    """ Crew JSON"""

    # squalchemy from Crews table
    crew = Crew.query.all()

    projectCrew = {}
    for i, crewmember in enumerate(crew):
        projectCrew[i] = {}
        projectCrew[i]['crew_id'] = crewmember.crew_id
        projectCrew[i]['project_id'] = crewmember.project_id
        projectCrew[i]['user_id'] = crewmember.user_id
        projectCrew[i]['fullname'] = crewmember.fullname
        projectCrew[i]['role'] = crewmember.role
    return jsonify(results=projectCrew)


@app.route('/faq')
def answer_questions():
    """ Frequently Asked Questions."""
    
    return render_template("faq.html")


if __name__ == "__main__":

    app.debug = True
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)
    db.create_all()

    # DebugToolbarExtension(app)

    app.run(host="0.0.0.0")
