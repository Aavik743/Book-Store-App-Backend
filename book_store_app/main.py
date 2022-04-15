from flask import Flask
from db.connector import connect_database

app = Flask(__name__)

connect_database()

if __name__ == '__main__':
    app.run(debug=True)
