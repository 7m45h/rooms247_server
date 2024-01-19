import os
from flask import Flask
from flask_cors import CORS
from flask_restful import Api, Resource, reqparse
from flask_sqlalchemy import SQLAlchemy

# setup and init
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URI")

CORS(app)

api = Api(app)
db = SQLAlchemy(app)

# databes models
class RoomModel(db.Model):
    room_id = db.Column(db.String(64), primary_key=True)
    dist = db.Column(db.String(64), nullable=False)
    addr = db.Column(db.String(512), nullable=False)
    tele = db.Column(db.String(64), nullable=False)
    del_key = db.Column(db.String(64), nullable=False)

    def __repr__(self):
        return f"<Room {self.room_id}>"

def get_rooms():
    results = db.session.execute(db.select(RoomModel.room_id ,RoomModel.dist, RoomModel.addr, RoomModel.tele).order_by(RoomModel.room_id))

    return results

def add_room(room_id, dist, addr, tele, del_key):
    room = RoomModel(room_id=room_id, dist=dist, addr=addr, tele=tele, del_key=del_key)
    db.session.add(room)
    db.session.commit()
    return [room]

def del_room(room_id, del_key):
    room = RoomModel.query.get(room_id)
    if room == None:
        return None

    if room.del_key == del_key:
        db.session.delete(room)
        db.session.commit()
        return [room]

    return None

# controllers and api endpoints
room_post_args = reqparse.RequestParser()
room_post_args.add_argument("room_id", type=str, help="room room_id required", required=True)
room_post_args.add_argument("dist", type=str, help="distance required", required=True)
room_post_args.add_argument("addr", type=str, help="room address required", required=True)
room_post_args.add_argument("tele", type=str, help="telephone number required", required=True)
room_post_args.add_argument("del_key", type=str, help="delete key required", required=True)

room_delete_args = reqparse.RequestParser()
room_delete_args.add_argument("room_id", type=str, help="room room_id required", required=True)
room_delete_args.add_argument("del_key", type=str, help="delete key required", required=True)

def mk_room_res(rooms):
    room = {"room": []}
    for rm in rooms:
        room["room"].append({"room_id": rm.room_id, "dist": rm.dist, "addr": rm.addr, "tele": rm.tele})
    return room

class Room(Resource):
    def get(self):
        room = get_rooms()
        room = mk_room_res(room)
        return room

    def post(self):
        args = room_post_args.parse_args()
        room = add_room(args["room_id"], args["dist"], args["addr"], args["tele"], args["del_key"])
        room = mk_room_res(room)
        return room, 201

    def delete(self):
        args = room_delete_args.parse_args()
        room = del_room(args["room_id"], args["del_key"])
        if room == None:
            return {"error": "not found"}, 404

        room = mk_room_res(room)
        return room

api.add_resource(Room, "/room")
