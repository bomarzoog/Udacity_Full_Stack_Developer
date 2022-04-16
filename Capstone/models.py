import os
import datetime
from sqlalchemy import Column, String, create_engine, Integer
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import json

database_path = os.getenv('DATABASE_URI')
if database_path.startswith("postgres://"):
   database_path = database_path.replace("postgres://", "postgresql://", 1)


db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_ECHO"] =True
    db.app = app
    db.init_app(app)
    migrate = Migrate(app, db)
    

  


'''
Actor Class
ID, Name, Age, Gender
'''
class Actor(db.Model):  
  __tablename__ = 'actors'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String, nullable=False)
  age = db.Column(db.Integer)
  gender = db.Column(db.String)

  def __init__(self, name, age, gender):
    self.name = name
    self.age = age
    self.gender = gender

# define format function

  def format(self):
    return {
      'id': self.id,
      'name': self.name,
      'age': self.age,
      'gender': self.gender
    }

  def __repr__(self):
    return f'<Actor ID: {self.id}, name: {self.name}, age: {self.age}, gender: {self.gender}>'

    '''
 insert() 
    insert new Actor model into database 

    eg: 
      actor = Actor(name=Joe,age=25,gender=male)
      actor.insert()
'''

  def insert(self):
    db.session.add(self)
    db.session.commit()


  '''
  delete() 
    delete Actor model from database 

    eg: 
      actor = Actor(name=Joe,age=25,gender=male)
      actor.delete()
  '''

  def delete(self):
    db.session.delete(self)
    db.session.commit()
  

  '''
 update() 
    update Actor model attributes

    eg: 
      actor = Actor(name=Joe,age=25,gender=male)
      actor.name = "John"
      actor.upate()
'''

  def update(self):
    db.session.commit()
    
'''
Movie Class
ID, title, category, release_date
'''


class Movie(db.Model):
  __tablename__ = 'movies'
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String, nullable =False)
  category = db.Column(db.String)
  release_date = db.Column(db.DateTime)

  def __init__(self, title, category, release_date):
    self.title = title
    self.category = category
    self.release_date = release_date


  def format(self):
   return {
     'id': self.id,
     'title': self.title,
     'category': self.category,
     'release_date': self.release_date.strftime("%Y-%m-%d")
   }
 
  def __repr__(self):
    return f'<Movie ID: {self.id}, title: {self.title}, category: {self.category}, release_date: {self.release_date}>'

  '''
  insert() 
    insert new Movie model into database 

    eg: 
      movie = Movie(title=Gladiator,category=history,release_date=2000)
      movie.insert()
  '''


  def insert(self):
    db.session.add(self)
    db.session.commit()

  


  '''
  delete() 
    delete Movie model from database 

    eg: 
      movie = Movie(title=Gladiator,category=history,release_date=2000)
      movie.delete()
  '''

  def delete(self):
    db.session.delete(self)
    db.session.commit()
  

  '''
    update() 
    update Movie model attributes

      movie = Movie(title=Gladiator,category=history,release_date=2000)
      movie.category = 'drama'
      movie.update()
  '''

  def update(self):
    db.session.commit()
    

