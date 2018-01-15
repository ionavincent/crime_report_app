from flask import request
from flask_restplus import Resource
from sqlalchemy import and_


from restplus import api
from endpoints.serializers import report
from endpoints.parsers import reports_request_parser
from database.models import CrimeReport

ns = api.namespace('reports',
                   description='Operations relating to crime reports')


@ns.route('/')
class ReportCollection(Resource):

    @ns.marshal_list_with(report)
    @api.expect(reports_request_parser, validate=True)
    def get(self):
        """
        Returns a list of all crime reports. Results are filters if filters
        are supplied and ordered by crime type, unless another 'order_by'
        value is supplied
        :returns: List of dictionaries describing each crime report matching
        the given filters, and ordered by crime type or the given 'order_by'
        value
        """
        args = reports_request_parser.parse_args()

        limit = args.get("limit")

        valid_orderings = {
            "crime_type": CrimeReport.crime_type,
            "year": CrimeReport.year,
            "month": CrimeReport.month
        }

        valid_filters = {
            "crime_id": lambda value: CrimeReport.crime_id.like(value),
            "year": lambda value: CrimeReport.year.like(value),
            "month": lambda value: CrimeReport.month.like(value),
            "reported_by": lambda value: CrimeReport.reported_by.like(value),
            "falls_within": lambda value: CrimeReport.falls_within.like(value),
            "longitude": lambda value: CrimeReport.longitude.like(value),
            "latitude": lambda value: CrimeReport.latitude.like(value),
            "location": lambda value: CrimeReport.location.like(
                "%{}%".format(value)
            ),
            "lsoa_code": lambda value: CrimeReport.lsoa_code.like(value),
            "lsoa_name": lambda value: CrimeReport.lsoa_name.like(value),
            "crime_type": lambda value: CrimeReport.crime_type.like(value),
            "last_outcome": lambda value: CrimeReport.last_outcome.like(
                "%{}%".format(value)
            ),
            "context": lambda value: CrimeReport.context.like(value)
        }

        ordering = valid_orderings.get(
            request.args.get("order_by"),
            CrimeReport.crime_type
        )

        filters = []
        for parameter_name, value in args.items():
            if parameter_name in valid_filters and value:
                filters.append(valid_filters[parameter_name](value))

        reports = (CrimeReport.query.filter(and_(*filters))
                   .order_by(ordering)
                   .limit(limit)
                   .all())

        return reports, 200
