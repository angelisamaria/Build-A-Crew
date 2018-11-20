from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash,
                   session)

from flask_debugtoolbar import DebugToolbarExtension

from model import User, Project, Crew, Callsheet, connect_to_db, db

import time
from datetime import date


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """ Landing page."""
    
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        return render_template("projects/dashboard.html", user=user)
    else:
        return render_template("homepage.html")

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
        location = request.form.get("location")
        portfolio = request.form.get("portfolio")
        new_user = User(email=user_email, 
                            pw=pw,
                            fname=fname,
                            lname=lname,
                            location=location,
                            portfolio=portfolio)
                            
        db.session.add(new_user)
        db.session.commit()

        # session['user_id'] = request.form['user_id']
        session['user_id'] = new_user.user_id

        return redirect('/dashboard')


@app.route('/login', methods=['GET', 'POST'])
def log_in():

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

    del session['user_id']
    flash('You are logged out.')

    return redirect('/')


@app.route('/dashboard')
def user_dashboard():
    """User's Dashboard Page."""

    user = User.query.get(session['user_id'])
    user_projects = Project.query.filter_by(user_id=session['user_id'])
    numprojects = Project.query.filter_by(user_id=session['user_id']).count()
    
    return render_template("/projects/dashboard.html", user=user, user_projects=user_projects, numprojects=numprojects)


@app.route('/projects')
def user_projects():
    """ User's projects. """

    user_projects = Project.query.filter_by(user_id=session['user_id'])
    
    return render_template("/projects/userprojects.html", user_projects=user_projects)

@app.route('/projects/<project_id>')
def view_project(project_id):
    """ View projet details."""
    specific_project = Project.query.get(project_id)

    
    return render_template("/projects/project_id.html", specific_project=specific_project)


@app.route('/newproject', methods = ['GET', 'POST'])
def new_user_project():
    """ User's projects. """

    user_id = session['user_id']

    if request.method == 'GET':
        return render_template("/projects/newproject.html", user_id=user_id)

    else:
        title = request.form.get("title")
        sdate = request.form.get("sdate")
        edate = request.form.get("edate")
        location = request.form.get("location")
        proj_desc = request.form.get("proj_desc")
        user_id = request.form.get("user_id")
        proj_img = request.form.get("proj_img")
        new_proj = Project(title=title, 
                            sdate=sdate,
                            edate=edate,
                            location=location,
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

@app.route('/crew/<project_id>', methods=['GET', 'POST'])
def project_crew(project_id):
    """ Frequently Asked Questions."""

    if request.method == 'POST':
        project_id = project_id
        user_id = request.form.get("name")
        role = request.form.get("role")
        crewMember = Crew(project_id=project_id, 
                            user_id=user_id,
                            role=role)
        db.session.add(crewMember)
        db.session.commit()
        users = User.query.all()

    specific_project = Project.query.get(project_id)
    user_projects = Project.query.filter_by(user_id=session['user_id'])
    crew = Crew.query.filter_by(project_id=project_id)
    users = User.query.all()
    
    return render_template("/crews/crew.html", specific_project=specific_project, user_projects=user_projects, crew=crew, users=users)


@app.route('/callsheets/<project_id>',  methods=['GET', 'POST'])
def all_callsheets(project_id):
    """ User's contact list."""

    if request.method == 'POST':
        project_id = project_id
        day_number = request.form.get("day_number")
        shoot_date = request.form.get("shoot_date")
        lunch_time = request.form.get("lunch_time")
        lunch_location = request.form.get("lunch_location")
        newCallsheet = Callsheet(project_id=project_id, 
                            day_number=day_number,
                            shoot_date=shoot_date,
                            lunch_time=lunch_time,
                            lunch_location=lunch_location)
        db.session.add(newCallsheet)
        db.session.commit()
        users = User.query.all()

    specific_project = Project.query.get(project_id)
    user_projects = Project.query.filter_by(user_id=session['user_id'])
    # crew = Crew.query.filter_by(project_id=project_id)
    callsheets = Callsheet.query.all()
    
    return render_template("/projects/callsheets.html", callsheets=callsheets, specific_project=specific_project, user_projects=user_projects)


@app.route('/callsheets/<project_id>/<callsheet_id>')
def view_callsheet(project_id, callsheet_id):
    """ User's contact list."""
    
    specific_callsheet = Callsheet.query.get(callsheet_id)
    specific_project = Project.query.get(project_id)
    user_projects = Project.query.filter_by(user_id=session['user_id'])

    return render_template("projects/callsheet_id.html", specific_project=specific_project, specific_callsheet=specific_callsheet)


@app.route('/contacts')
def view_contacts():
    """ User's contact list."""

    users = User.query.all()
    # location = location.replace('(', '').replace(')', '')
    # location = location.split(",")
    # lat = location[0]
    # lon = location[1]
    
    return render_template("users/contacts.html", users=users)


@app.route('/faq')
def answer_questions():
    """ Frequently Asked Questions."""
    
    return render_template("faq.html")


if __name__ == "__main__":

    app.debug = True
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)
    db.create_all()

    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")
