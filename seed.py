"""Utility file to seed User database from Faker data """

import datetime
from sqlalchemy import func

from model import User, Project, Schedule, Location, Callsheet, connect_to_db, db
from server import app
from faker import Faker
import random
import requests


def load_users():
    """Load users from Faker into database."""

    fake = [Faker() for i in range(10)]
    roles = ["Art Director", "Production Designer", "Prop Master", "Set Designer",
                "Voiceover Talent", "Music Composer", "Boom Operator", 
                "Sound Mixer/Recordist", "Foley Artist", "First Assistant Camera (1st AC)",
                "Second Assistant Camera (2nd AC)", "Director of Photography", 
                "Digital Imaging Technician (DIT)", "Steadicam Operator", "Drone Operator",
                "Best Boy Grip + Electric", "Gaffer", "Grip", "Key Grip", "Director",
                "Assistant Director", "Executive Producer", "Producer", 
                "Production Coordinator", "Production Assistant", "Costume Designer", 
                "Hair Stylist", "Make Up Artist", "Hair + MUA", 
                "Special Effects Makeup Artist", "Wardrobe Stylist"]

    pics = ["https://randomuser.me/api/portraits/thumb/women/95.jpg",
                "https://randomuser.me/api/portraits/thumb/women/94.jpg",
                "https://randomuser.me/api/portraits/thumb/women/93.jpg",
                "https://randomuser.me/api/portraits/thumb/women/92.jpg",
                "https://randomuser.me/api/portraits/thumb/women/91.jpg",
                "https://randomuser.me/api/portraits/thumb/women/90.jpg",
                "https://randomuser.me/api/portraits/thumb/women/89.jpg",
                "https://randomuser.me/api/portraits/thumb/women/88.jpg",
                "https://randomuser.me/api/portraits/thumb/women/87.jpg",
                "https://randomuser.me/api/portraits/thumb/women/86.jpg",
                "https://randomuser.me/api/portraits/thumb/women/85.jpg",
                "https://randomuser.me/api/portraits/thumb/women/84.jpg",
                "https://randomuser.me/api/portraits/thumb/women/83.jpg",
                "https://randomuser.me/api/portraits/thumb/women/82.jpg",
                "https://randomuser.me/api/portraits/thumb/women/81.jpg",
                "https://randomuser.me/api/portraits/thumb/women/80.jpg",
                "https://randomuser.me/api/portraits/thumb/women/79.jpg",
                "https://randomuser.me/api/portraits/thumb/women/78.jpg",
                "https://randomuser.me/api/portraits/thumb/women/77.jpg",
                "https://randomuser.me/api/portraits/thumb/women/76.jpg",
                "https://randomuser.me/api/portraits/thumb/women/75.jpg",
                "https://randomuser.me/api/portraits/thumb/women/74.jpg",
                "https://randomuser.me/api/portraits/thumb/women/73.jpg",
                "https://randomuser.me/api/portraits/thumb/women/72.jpg"]

    r = requests.get('https://randomuser.me/api/?inc=picture')
    randomuser = r.json()
    results = randomuser['results'][0]
    pic = results['picture']['thumbnail']

    for f in fake:
        user = f.simple_profile()
        email=user['mail']
        pw=f.password(length=10, special_chars=True, digits=True, upper_case=True, lower_case=True)
        fname=f.first_name_female()
        lname=f.last_name()
        zipcode=f.zipcode()
        linkedin = ("www.linkedin.com/in/{}{}".format(fname,lname))
        role = random.choice(roles)
        picture = random.choice(pics)

        new_user = User(email=email, 
                            pw=pw,
                            fname=fname,
                            lname=lname,
                            zipcode=zipcode,
                            role=role,
                            linkedin=linkedin,
                            picture=picture)              
        db.session.add(new_user)
        db.session.commit()

def load_projects():
    """Load projects from Faker into database."""

    fake = [Faker() for i in range(20)]
    u_id = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    for f in fake:
        title = f.sentence(nb_words=6, variable_nb_words=True, ext_word_list=None).rstrip(".")
        sdate = f.date_between_dates(date_start=None, date_end=None)
        edate = f.date_between_dates(date_start=None, date_end=None)
        proj_desc = f.text(max_nb_chars=200, ext_word_list=None)
        user_id = random.choice(u_id)
        proj_img = f.image_url(width=150, height=150)
        new_proj = Project(title=title, 
                            sdate=sdate,
                            edate=edate,
                            proj_desc=proj_desc,
                            user_id=user_id, 
                            proj_img=proj_img)         
        db.session.add(new_proj)
        db.session.commit()


def load_callsheets():
    """Load callsheets into database."""

    p_id = [1, 2, 3, 4, 5]

    for i in range(10):
        callsheet_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
        day_number = 1
        project_id = random.choice(p_id)
        shoot_date = "11/24/2018"
        lunch_time = "12:00 PM"
        lunch_location = "Pearl's Burgers"
        hospital_name = "St. Francis Memorial Hospital"
        hostpital_location = " 900 Hyde St, San Francisco, CA 94109"
        parking_address = "400 Taylor StSan Francisco, CA 94102"
        new_callsheet = Callsheet(day_number=day_number, 
                                project_id=project_id,
                                shoot_date=shoot_date,
                                lunch_time=lunch_time,
                                lunch_location=lunch_location, 
                                hospital_name=hospital_name,
                                hostpital_location=hostpital_location,
                                parking_address=parking_address)         
    db.session.add(new_callsheet)
    db.session.commit()


def load_schedules():
    """Load schedules into database."""

    for i in range(10):
        schedule_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
        daynight = "Day"
        script = "Pages 1-4"
        shoot_time = "10:00 AM"
        scene = "Bedroom Scene"
        shoot_description = "Bob begins to start his day, converses with mother, Lisa."
        talent = "Bob Eliott, Lisa Stremner"
        new_sched = Schedule(daynight=daynight,
                                script=script,
                                shoot_time=shoot_time,
                                scene=scene, 
                                shoot_description=shoot_description,
                                talent=talent)         
        db.session.add(new_sched)
        db.session.commit()


def load_locations():
    """Load locations into database."""

    s_id = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    l_nu = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    for i in range(10):
        location_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
        location_name = "Bob's Place"
        address = "1 HTML Way, Santa Cruz, CA 95060"
        location_num = random.choice(l_nu)
        new_loc = Location(location_name=location_name,
                                address=address,
                                location_num=location_num)         
        db.session.add(new_loc)
        db.session.commit()



if __name__ == "__main__":
    connect_to_db(app)
    db.create_all()

    load_users()
    load_projects()
    load_schedules()
    load_callsheets()
    load_locations()