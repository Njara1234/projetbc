from app import db
from flask_login import UserMixin
from sqlalchemy.orm import relationship

class Admin(db.Model):
    __tablename__='admin'
    id=db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(255), nullable=False)
    password=db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f'Admin("{self.username}","{self.id}")'

class User(db.Model,UserMixin):
    __tablename__='users'
    id=db.Column(db.Integer, primary_key=True)
    fname=db.Column(db.String(255), nullable=False)
    lname=db.Column(db.String(255), nullable=False)
    email=db.Column(db.String(255), nullable=False)
    username=db.Column(db.String(255), nullable=False)
    password=db.Column(db.String(255), nullable=False)
    status=db.Column(db.Integer,default=0, nullable=False)
   
    def __repr__(self):
        return f'User("{self.username}","{self.id}")'


    
class Superadmin(db.Model):
    __tablename__='superadmin'
    id=db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(255), nullable=False)
    password=db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f'Superdmin("{self.username}","{self.id}")'


    




  
