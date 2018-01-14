from flask import request
from flask_restplus import Resource

from restplus import api
from endpoints.serializers import report
from database.models import CrimeReport

ns = api.namespace('reports',
                   description='Operations relating to crime reports')


@ns.route('/')
class ReportCollection(Resource):

    @ns.marshal_list_with(report)
    def get(self):
        """
        Returns a list of all crime types, filtered by year, if provided
        """
        valid_orderings = {
            "crime_type": CrimeReport.crime_type,
            "year": CrimeReport.year,
            "month": CrimeReport.month
        }

        valid_filters = {
            "year": lambda x: CrimeReport.year.like(int(x)),
            "month": lambda x: CrimeReport.month.like(int(x)),
            "crime_type": lambda x: CrimeReport.crime_type.like(x)
        }

        ordering = valid_orderings.get(
            request.args.get("order_by"),
            CrimeReport.crime_type
        )

        filters = []
        for parameter_name, value in request.args.items():
            if parameter_name in valid_filters:
                filters.append(valid_filters[parameter_name](value))

        reports = (CrimeReport.query.filter(*filters)
                   .order_by(ordering)
                   .limit(100)
                   .all())

        return reports, 200
