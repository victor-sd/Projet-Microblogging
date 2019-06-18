import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from peewee import (
    SqliteDatabase, 
    Model,
    CharField,
    DateField,
    DateTimeField,
    FloatField,
    ForeignKeyField,
    TextField,
)
from flask_login import UserMixin


database = SqliteDatabase('data.sqlite3')

class BaseModel(Model):
    
    class Meta:
        database = database

class User(UserMixin, BaseModel):
    username = CharField(max_length=20)
    mail = CharField(max_length=30)
    mdp = CharField(max_length=80)

class Post(BaseModel):
    title = TextField()
    body = TextField()
    dateCreate = DateField()
    refUser = ForeignKeyField(User, backref="auteur")



def create_tables():
    with database:
        database.create_tables([User, Post])


def drop_tables():
    with database:
        database.drop_tables([User, Post])
