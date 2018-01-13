from flask_restplus import fields
from restplus import api

event = api.model('event', {
    "id": fields.Integer(readOnly=True, description='The unique identifier for '
                         'an event'),
    "name": fields.String(description='The name of an event'),
    "type": fields.String(description='The event type')
})