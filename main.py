from flask import Flask
from flask_restful import Api, Resource, reqparse

app = Flask(__name__)
api = Api(app)

rooms = {
    "room": [
        { "id": 123456789, "addr": "a/b/c", "tele": 123456789 },
        { "id": 987654321, "addr": "c/b/a", "tele": 987654321 }
    ]
}

room_get_args = reqparse.RequestParser()
room_get_args.add_argument("id", type=int, help="room id")

room_post_args = reqparse.RequestParser()
room_post_args.add_argument("id", type=int, help="room id", required=True)
room_post_args.add_argument("addr", type=str, help="room address", required=True)
room_post_args.add_argument("tele", type=int, help="telephone number", required=True)

room_delete_args = reqparse.RequestParser()
room_delete_args.add_argument("id", type=int, help="room id", required=True)

class Room(Resource):
    def get(self):
        args = room_get_args.parse_args()
        if args["id"] == None:
            return rooms
        else:
            for room in rooms["room"]:
                if room["id"] == args["id"]:
                    return {"room": [room]}

    def post(self):
        args = room_post_args.parse_args()
        rooms["room"].append(args)
        return {"room": [args]}, 201

    def delete(self):
        args = room_delete_args.parse_args()
        for room in rooms["room"]:
            if room["id"] == args["id"]:
                rooms["room"].remove(room)
                return {"room": [room]}
        

api.add_resource(Room, "/room")

if __name__ == "__main__":
    app.run(debug=True)
