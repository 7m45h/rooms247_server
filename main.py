import os
from flask import Flask
from flask_restful import Api

from controller import Room
from model import db

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.join(os.path.abspath(os.path.dirname(__file__)), 'rooms.db')}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
api = Api(app)
db.init_app(app)

api.add_resource(Room, "/room")

if __name__ == "__main__":
    app.run()
