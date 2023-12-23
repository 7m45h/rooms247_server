from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

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

    return results

def add_room(id, addr, tele):
    room = RoomModel(id=id, addr=addr, tele=tele)
    db.session.add(room)
    db.session.commit()
    return room

def del_room(id):
    room = RoomModel.query.get(args["id"])
    if room != None:
        db.session.delete(room)
        db.session.commit()
    return room
