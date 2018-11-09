from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash,
                   session)

from flask_debugtoolbar import DebugToolbarExtension

from model import User, Project, connect_to_db, db


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """ Landing page."""
    
    if 'user_id' in session:
        return render_template("dashboard.html")
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
        role = request.form.get("role")
        new_user = User(email=user_email, 
                            pw=pw,
                            fname=fname,
                            lname=lname,
                            location=location,
                            portfolio=portfolio,
                            role=role)
                            
        db.session.add(new_user)
        db.session.commit()

        # session['user_id'] = request.form['user_id']
        session['user_id'] = new_user.user_id

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

    user_projects = Project.query.filter_by(user_id=session['user_id'])
    
    return render_template("userprojects.html", user_projects=user_projects)

@app.route('/projects/<project_id>')
def view_project(project_id):
    """ Frequently Asked Questions."""
    specific_project = Project.query.get(project_id)
    
    return render_template("project_id.html", specific_project=specific_project)


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




# @app.route('/edit-profile', methods = ['GET', 'POST'])
# def edit_profile():
#     """Allow users to register, only their email and pw is required. """
    
#     if request.method == 'GET':
#         return render_template("createprofile.html")

#     else:
#         user_email = request.form.get("email")
#         pw = request.form.get("pw")
#         fname = request.form.get("fname")
#         lname = request.form.get("lname")
#         location = request.form.get("location")
#         portfolio = request.form.get("portfolio")
#         role = request.form.get("role")
#         new_user = User(email=user_email, 
#                             pw=pw,
#                             fname=fname,
#                             lname=lname,
#                             location=location,
#                             portfolio=portfolio,
#                             role=role)
                            
#         db.session.add(new_user)
#         db.session.commit()
#         return redirect(f'/dashboard')


# @app.route('/edit-profile', methods=['GET', 'POST'])
# def edit():
#     """ User edit their profile. """
# qry = db_session.query(Album).filter(
# Album.id==id)
# album = qry.first()

# if album:
# form = AlbumForm(formdata=request.form, obj=album)
# if request.method == 'POST' and form.validate():
# # save edits
# save_changes(album, form)
# flash('Album updated successfully!')
# return redirect('/')
# return render_template('edit_album.html', form=form)
# else:
# return 'Error loading #{id}'.format(id=id)


@app.route('/user')
def user():
    """ User view of their private profile. """

    user = User.query.get(session['user_id'])

    return render_template('user.html', user=user)


# @app.route('/crew/<project_id>')
# def project_crew(project_id):
#     """ Crew list for a specific project."""

#     user = User.query.get(session['user_id'])
#     specific_project = Project.query.get(project_id)
#     user_projects = Project.query.get(user_id)

    
#     return render_template("crew.html", user=user, specific_project=specific_project)




@app.route('/crew/<project_id>')
def project_crew(project_id):
    """ Frequently Asked Questions."""
    specific_project = Project.query.get(project_id)
    user_projects = Project.query.filter_by(user_id=session['user_id'])
    
    return render_template("crew.html", specific_project=specific_project, user_projects=user_projects)


@app.route('/contacts')
def view_contacts():
    """ User's contact list."""
    
    return render_template("contacts.html")


@app.route('/faq')
def answer_questions():
    """ Frequently Asked Questions."""
    
    return render_template("faq.html")


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
