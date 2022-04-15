from mongoengine import connect


def connect_database():
    connect("mongodb://127.0.0.1:27017/BookStore")
