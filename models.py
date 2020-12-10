from peewee import *
import datetime
from flask_login import UserMixin
from playhouse.db_url import connect
import os

if 'ON_HEROKU' in os.environ: # later we will manually add this env var
                              # in heroku so we can write this code
  DATABASE = connect(os.environ.get('DATABASE_URL')) # heroku will add this
                                                     # env var for you
                                                     # when you provision the
                                                     # Heroku Postgres Add-on
else:
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
