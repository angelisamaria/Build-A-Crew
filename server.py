"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash,
                   session)

# from flask.ext.session import Session

from flask_debugtoolbar import DebugToolbarExtension

from model import User, Project, connect_to_db, db


app = Flask(__name__)


# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""
    
    if 'user' in session:
        return render_template("login.html")
    else:
        return render_template("homepage.html")

@app.route('/register', methods = ['GET', 'POST'])
def registration_form():
    """Allow users to register, only their email and pw is required. """
    
    if request.method == 'GET':
        return render_template("createprofile.html")

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
        return redirect(f'/dashboard')


@app.route('/login', methods=['GET', 'POST'])
def log_in():

    if request.method == 'GET':
        return render_template("login.html")

    else:
        email = request.form.get("email")
        pw = request.form.get("pw")

        #check if user email is in database
        if User.query.filter(User.email == email).first():
            #password validation
            user = User.query.filter(User.email == email).first()
            if user.pw == pw:
                flash('You are logged in.')
                session['user_id'] = user.user_id

                return redirect(f'dashboard')

            else: #password does not match
                flash('Password does not match. Please try again.')

                return render_template("login.html")

        else: #if email is not in the database
            flash(f'No account with the email {email} exists. Please register.')

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
    
    return render_template("dashboard.html", user=user)


@app.route('/projects')
def user_projects():
    """ User's projects. """


    uprojects = Project.query.filter_by(user_id=session['user_id'])
    
    return render_template("userprojects.html", uprojects=uprojects)



@app.route('/projects', methods=['GET'])
def show_movie_details(project_id):
    """ Show release and more info link about a movie."""

    user_projects = Project.query.get(user_id)

    user_name = User.query.get(fname)

    session_user_id = session.get('user_id')

    if session_user_id:
        # get project info
        project_info = Project.query.all()
    else:
        project_info = None

    return render_template('project_id.html', user_projects=user_projects, user_name=user_name, user_id=user_id)

@app.route('/newproject', methods = ['GET', 'POST'])
def new_user_project():
    """ User's projects. """

    user_id = session['user_id']

    if request.method == 'GET':
        return render_template("newproject.html", user_id=user_id)

    else:
        title = request.form.get("title")
        sdate = request.form.get("sdate")
        edate = request.form.get("edate")
        location = request.form.get("location")
        proj_desc = request.form.get("proj_desc")
        user_id = request.form.get("user_id")
        new_proj = Project(title=title, 
                            sdate=sdate,
                            edate=edate,
                            location=location,
                            proj_desc=proj_desc,
                            user_id=user_id)
        db.session.add(new_proj)
        db.session.commit()

        return redirect("/projects")

# @app.route('/users/<int:user_id>')
# def show_individual_user(user_id):
#     """Show details about an individual user: their age, zipcode, 
#     and a list of movies they rated with the ratings. """

#     user = User.query.get(user_id)

#     return render_template('user.html', user=user)



@app.route('/user')
def user():
    """ User view their private profile. """
    user = User.query.get(session['user_id'])

    return render_template('user.html', user=user)

@app.route('/contacts')
def view_contacts():
    """ User's Contacts."""
    
    return render_template("contacts.html")



@app.route('/faq')
def answer_questions():
    """ Frequently Asked Questions."""
    
    return render_template("faq.html")



@app.route('/projects/<project_id>')
def view_project(project_id):
    """ Frequently Asked Questions."""
    specific_project = Project.query.get(project_id)
    
    return render_template("project_id.html", specific_project=specific_project)


if __name__ == "__main__":


    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)
    db.create_all()

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")
