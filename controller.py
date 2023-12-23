from flask_restful import Resource, reqparse, fields, marshal_with
from model import get_room, add_room, del_room

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
        room = get_room(args["id"])
        return room

    @marshal_with(rooms_fields)
    def post(self):
        args = room_post_args.parse_args()
        room = add_room(args["id"], args["addr"], args["tele"])
        return room, 201

    @marshal_with(rooms_fields)
    def delete(self):
        args = room_delete_args.parse_args()
        room = del_room(args["id"])
        if room == None:
            return {"error": "not found"}, 404
        return room
