

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    """User Information."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(64), nullable=False)
    pw = db.Column(db.String(64), nullable=False)
    fname = db.Column(db.String(64), nullable=False)
    lname = db.Column(db.String(64), nullable=False)
    zipcode = db.Column(db.Integer, nullable=False)
    role = db.Column(db.String(64))
    linkedin = db.Column(db.String(64), nullable=True)
    picture = db.Column(db.String(120), nullable=True)
 
    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"""<User user_id={self.user_id} 
                        email={self.email}
                        pw={self.pw}
                        fname={self.fname}
                        lname={self.lname}
                        zipcode={self.zipcode}
                        role={self.role}
                        picture={self.picture}
                        linkedin={self.linkedin}>"""


class Project(db.Model):
    """Project Information."""

    __tablename__ = "projects"

    project_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title = db.Column(db.String(120), nullable=True)
    sdate = db.Column(db.String(64), nullable=True)
    edate = db.Column(db.String(64), nullable=True) # change to datetime later
    status = db.Column(db.Boolean, default=True, nullable=False)
    proj_desc = db.Column(db.String(300), nullable=True)
    user_id = db.Column(db.Integer, default=0, nullable=False)
    proj_img = db.Column(db.String(300), nullable=True)
    
    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"""<Project project_id={self.project_id} 
                        title={self.title}
                        start date={self.sdate}
                        end date={self.edate}
                        status={self.status}
                        proj_desc={self.proj_desc}
                        proj_img={self.proj_img}>"""

class Crew(db.Model):
    """User Information."""

    __tablename__ = "crews"

    crew_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    project_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    role = db.Column(db.String(64), nullable=True)
    users = db.relationship('User')
    fullname = db.Column(db.String(64))
 
    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"""<Crew crew_id={self.user_id} 
                        project_id={self.project_id}
                        user_id={self.user_id}
                        role={self.role}
                        fullname={self.fullname}>"""


class Callsheet(db.Model):
    """ User Callsheets."""

    __tablename__ = "callsheets"

    callsheet_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    day_number = db.Column(db.Integer, nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.project_id'))
    shoot_date = db.Column(db.String(64))
    lunch_time = db.Column(db.String(64))
    lunch_location = db.Column(db.String(64))
    hospital_name = db.Column(db.String(64))
    hostpital_location = db.Column(db.String(64))
    parking_address = db.Column(db.String(64))

    projects = db.relationship('Project')

    def __repr__(self):

        return f"""<Callsheet callsheet_id={self.callsheet_id}
                        day_number={self.day_number}
                        project_id={self.project_id}
                        shoot_date = {self.shoot_date}
                        lunch_time={self.lunch_time}
                        lunch_location={self.lunch_location}
                        hospital_name={self.hospital_name}
                        hostpital_location={self.hostpital_location}
                        parking_address={self.parking_address}>"""


class Schedule(db.Model):
    """Schedule Information."""

    __tablename__ = "schedules"

    schedule_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    callsheet_id = db.Column(db.Integer, db.ForeignKey('callsheets.callsheet_id'))
    daynight = db.Column(db.String(64))
    script = db.Column(db.String(64))
    shoot_time = db.Column(db.String(64))
    scene = db.Column(db.String(64))
    shoot_description = db.Column(db.String(64))
    talent = db.Column(db.String(64))

    callsheets = db.relationship('Callsheet')
 
    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"""<Schedule schedule_id={self.user_id} 
                        callsheet_id={self.callsheet_id}
                        daynight={self.daynight}
                        script={self.script}
                        shoot_time={self.shoot_time}
                        scene={self.scene}
                        shoot_description={self.shoot_description}
                        talent={self.talent}>"""


class Location(db.Model):
    """Location Information."""

    __tablename__ = "locations"

    location_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    schedule_id = db.Column(db.Integer, db.ForeignKey('schedules.schedule_id'))
    location_name = db.Column(db.String(64))
    address = db.Column(db.String(64))
    location_num = db.Column(db.Integer)

    schedules = db.relationship('Schedule')
 
    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"""<Location location_id={self.location_id} 
                        schedule_id={self.schedule_id}
                        address={self.callsheet_id}
                        location_name={self.location_name}
                        location_num={self.location_num}>"""


# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///buildacrew'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":

    from server import app
    connect_to_db(app)
    print("Connected to DB.")
