from flask_restplus import fields

from restplus import api

report = api.model('report', {
    "id": fields.Integer(readOnly=True, description='The unique identifier '
                         'for a crime report'),
    "crime_id": fields.String(description=''),
    "month": fields.String(description=''),
    "year": fields.String(description=''),
    "reported_by": fields.String(description=''),
    "falls_within": fields.String(description=''),
    "longitude": fields.Float(description=''),
    "latitude": fields.Float(description=''),
    "location": fields.String(description=''),
    "lsoa_code": fields.String(description=''),
    "lsoa_name": fields.String(description=''),
    "crime_type": fields.String(description=''),
    "last_outcome": fields.String(description=''),
    "context": fields.String(description='')

})
