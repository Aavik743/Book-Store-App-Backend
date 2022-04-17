from flask import Flask
from flask_restful import Api
from db.connector import connect_database
from routes import all_routes

app = Flask(__name__)
api = Api(app)

connect_database()

def confirm_api():
    for data in all_routes:
        api_class = data[0]
        endpoint = data[1]
        api.add_resource(api_class, endpoint)


confirm_api()

if __name__ == '__main__':
    app.run(debug=True)
