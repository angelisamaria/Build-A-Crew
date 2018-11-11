

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


##############################################################################
# Model definitions

class User(db.Model):
    """User Information."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(64), nullable=False)
    pw = db.Column(db.String(64), nullable=False)
    fname = db.Column(db.String(64), nullable=True)
    lname = db.Column(db.String(64), nullable=True)
    location = db.Column(db.String(64), nullable=True)
    portfolio = db.Column(db.String(64), nullable=True)
 
    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"""<User user_id={self.user_id} 
                        email={self.email}
                        pw={self.pw}
                        fname={self.fname}
                        lname={self.lname}
                        location={self.location}
                        portfolio={self.portfolio}>"""


class Project(db.Model):
    """Project Information."""

    __tablename__ = "projects"

    project_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title = db.Column(db.String(64), nullable=True)
    sdate = db.Column(db.String(64), nullable=True)
    edate = db.Column(db.String(64), nullable=True) # change to datetime later
    location = db.Column(db.String(64), nullable=True)
    status = db.Column(db.Boolean, default=True, nullable=False)
    proj_desc = db.Column(db.String(300), nullable=True)
    user_id = db.Column(db.Integer, nullable=False)
    
    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"""<Project project_id={self.project_id} 
                        title={self.title}
                        start date={self.sdate}
                        end date={self.edate}
                        location={self.location}
                        status={self.status}
                        proj_desc={self.proj_desc}>"""



##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///buildacrew'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print("Connected to DB.")
