from flask import request
from flask_restplus import Resource

from restplus import api
from endpoints.serializers import event
from database import db
from database.models import Event

ns = api.namespace('events',
                   description='Operations relating to events')


@ns.route('/')
class EventCollection(Resource):

    @ns.marshal_list_with(event)
    def get(self):
        """
        Returns a list of all events, filtered by type if specified
        """
        if 'type' in request.args:
            events = Event.query.filter_by(type=request.args['type']).all()
        else:
            events = Event.query.all()

        return events, 200

    @ns.marshal_with(event)
    @ns.expect(event)
    def post(self):
        """
        Creates a new event
        """
        event = Event.from_json(request.json)
        try:
            db.session.add(event)
            db.session.commit()
        except:
            db.session.rollback()
            return 500

        return event, 201


@ns.route('/<int:id>')
class EventItem(Resource):

    @ns.marshal_with(event)
    def get(self, id):
        """
        Returns the event with the given id
        """
        event = Event.query.filter_by(id=id).one()
        return event, 200
