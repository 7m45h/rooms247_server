import os
from flask import Flask
from flask_restful import Api, Resource, reqparse
from flask_sqlalchemy import SQLAlchemy

# define paths
app_dir_path = os.path.abspath(os.path.dirname(__file__))
room_db_path = os.path.join(app_dir_path, 'rooms.db')

# setup and init
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{room_db_path}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

api = Api(app)
db = SQLAlchemy(app)


# databes models
class RoomModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    addr = db.Column(db.String(512), nullable=False)
    tele = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<Room {self.id}>"

def get_room(id):
    if id == None:
        results = RoomModel.query.all()
    else:
        results = RoomModel.query.filter_by(id=id).first()
        if results == None:
            return None
        results = [results]

    return results

def add_room(id, addr, tele):
    room = RoomModel(id=id, addr=addr, tele=tele)
    db.session.add(room)
    db.session.commit()
    return [room]

def del_room(id):
    room = RoomModel.query.get(id)
    if room == None:
        return None

    db.session.delete(room)
    db.session.commit()
    return [room]


# controllers and api endpoints
room_get_args = reqparse.RequestParser()
room_get_args.add_argument("id", type=int, help="room id")

room_post_args = reqparse.RequestParser()
room_post_args.add_argument("id", type=int, help="room id required", required=True)
room_post_args.add_argument("addr", type=str, help="room address required", required=True)
room_post_args.add_argument("tele", type=int, help="telephone number required", required=True)

room_delete_args = reqparse.RequestParser()
room_delete_args.add_argument("id", type=int, help="room id required", required=True)

def mk_room_res(rooms):
    room = {"room": []}
    for rm in rooms:
        room["room"].append({"id": rm.id, "addr": rm.addr, "tele": rm.tele})
    return room

class Room(Resource):
    def get(self):
        args = room_get_args.parse_args()
        room = get_room(args["id"])
        if room == None:
            return {"error": "not found"}, 404
        room = mk_room_res(room)
        return room

    def post(self):
        args = room_post_args.parse_args()
        room = add_room(args["id"], args["addr"], args["tele"])
        room = mk_room_res(room)
        return room, 201

    def delete(self):
        args = room_delete_args.parse_args()
        room = del_room(args["id"])
        if room == None:
            return {"error": "not found"}, 404

        room = mk_room_res(room)
        return room

api.add_resource(Room, "/room")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        db.drop_all()
        db.create_all()

    app.run()
