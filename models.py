
import os
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
import json
import psycopg2

database_name = "capstone"
database_path = os.environ['DATABASE_URL']
db = SQLAlchemy()

'''
setup_db(app)
    binding between  flask application and  SQLAlchemy service
'''


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


def flase_nullable(*args, **kwargs):
    kwargs["nullable"] = kwargs.get("nullable", False)
    return db.Column(*args, **kwargs)


'''
Actor

'''


class Actor(db.Model):
    __tablename__ = 'actors'

    id = Column(Integer, primary_key=True)
    actor = flase_nullable(String)
    gender = flase_nullable(String)
    movie = flase_nullable(String)

    def __init__(self, actor, gender, movie):
        self.actor = actor
        self.gender = gender
        self.movie = movie

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'actor': self.actor,
            'gender': self.gender,
            'movie': self.movie,
        }


'''
Movie

'''


class Movie(db.Model):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True)
    movie = flase_nullable(String)
    catogry = flase_nullable(String)

    def __init__(self, movie, catogry):
        self.movie = movie
        self.catogry = catogry

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'movie': self.movie,
            'catogry': self.catogry
        }
