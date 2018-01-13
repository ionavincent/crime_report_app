from database import db


class Event(db.Model):

    __tablename__ = "event"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    type = db.Column(db.String(255))

    @staticmethod
    def from_json(data):
        name = data.get("name")
        type = data.get("type")
        if not name:
            raise RuntimeError("No event name given")
        return Event(name=name, type=type)

    def to_json(self):
        return {"name": self.name,
                "type": self.type}