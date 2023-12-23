import os
from flask import Flask
from flask_restful import Api, Resource, reqparse, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.join(os.path.abspath(os.path.dirname(__file__)), 'rooms.db')}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
api = Api(app)
db = SQLAlchemy(app)

class RoomModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    addr = db.Column(db.String(512), nullable=False)
    tele = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<Room {self.id}>"

room_get_args = reqparse.RequestParser()
room_get_args.add_argument("id", type=int, help="room id")

room_post_args = reqparse.RequestParser()
room_post_args.add_argument("id", type=int, help="room id", required=True)
room_post_args.add_argument("addr", type=str, help="room address", required=True)
room_post_args.add_argument("tele", type=int, help="telephone number", required=True)

room_delete_args = reqparse.RequestParser()
room_delete_args.add_argument("id", type=int, help="room id", required=True)

rooms_fields = {
    "id": fields.Integer,
    "addr": fields.String,
    "tele": fields.Integer
}

class Room(Resource):
    @marshal_with(rooms_fields)
    def get(self):
        args = room_get_args.parse_args()
        if args["id"] == None:
            results = RoomModel.query.all()
        else:
            results = RoomModel.query.filter_by(id=args["id"]).first()

        return results

    @marshal_with(rooms_fields)
    def post(self):
        args = room_post_args.parse_args()
        room = RoomModel(id=args["id"], addr=args["addr"], tele=args["tele"])
        db.session.add(room)
        db.session.commit()
        return room, 201

    @marshal_with(rooms_fields)
    def delete(self):
        args = room_delete_args.parse_args()
        room = RoomModel.query.get(args["id"])
        if room != None:
            db.session.delete(room)
            db.session.commit()
            return room

        return {"error": "not found"}, 404
            

api.add_resource(Room, "/room")

if __name__ == "__main__":
    app.run(debug=True)
