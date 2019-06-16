import datetime
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

database = SqliteDatabase('data.sqlite3')

class BaseModel(Model):
    
    class Meta:
        database = database

class User(BaseModel):
    username = CharField(max_length=20)
    name = CharField(max_length=40)
    firstname = CharField(max_length=20)
    mail = CharField(max_length=30)
    mdp = CharField(max_length=30)

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