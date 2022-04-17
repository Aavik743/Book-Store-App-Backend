import os

from mongoengine import connect


def connect_database():
    connect(host=os.getenv("server"))
