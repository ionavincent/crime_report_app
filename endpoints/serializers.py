from flask_restplus import fields

from restplus import api

report = api.model('report', {
    "id": fields.Integer(readOnly=True, description='The unique identifier '
                         'for a crime report'),
    "crime_id": fields.String(description='Crime ID'),
    "month": fields.Integer(description='Month'),
    "year": fields.Integer(description='Year'),
    "reported_by": fields.String(description='Reported By'),
    "falls_within": fields.String(description='Falls Within'),
    "longitude": fields.Float(description='Longitude'),
    "latitude": fields.Float(description='Latitude'),
    "location": fields.String(description='Location'),
    "lsoa_code": fields.String(description='LSOA Code'),
    "lsoa_name": fields.String(description='LSOA Name'),
    "crime_type": fields.String(description='Crime Type'),
    "last_outcome": fields.String(description='Last Outcome'),
    "context": fields.String(description='Context')
})
