from peewee import *
import datetime
from flask_login import UserMixin
from playhouse.db_url import connect
import os

DATABASE = SqliteDatabase('walks.sqlite')


class User(UserMixin, Model):
    username=CharField(unique=True)
    email=CharField(unique=True)
    password=CharField()

    class Meta:
        database = DATABASE


class Walk(Model):
    name = CharField()
    author = ForeignKeyField(User, backref='walks')
    tools = CharField()
    materials = CharField()
    edging = CharField()
    path = CharField()
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = DATABASE


def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Walk], safe=True)
    print("TABLES Created")
    DATABASE.close()
