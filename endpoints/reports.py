from flask import request
from flask_restplus import Resource

from restplus import api
from endpoints.serializers import report
from database import db
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
        ordering_parm = request.args.get("order_by") or 'crime_type'

        if 'year' in request.args:
            reports = (CrimeReport.query.filter_by(year=request.args['year'])
                                        .order_by(getattr(CrimeReport, ordering_parm))
                                        .all())
        if 'month' in request.args:
            reports = CrimeReport.query.filter_by(
                    year=request.args['month']).all()
        if 'month' and 'year' in request.args:
            reports = CrimeReport.query.filter_by(
                    month=request.args['month']).filter_by(year=
                    request.args['year']).all()
        if 'crime_type' in request.args:
            reports = (CrimeReport.query.filter_by(crime_type=request.args['crime_type'])
                                        .order_by(getattr(CrimeReport, ordering_parm))
                                        .all())

        else:
            import time
            start = time.time()
            reports = CrimeReport.query.limit(1000).all()
            duration = time.time() - start
            print("Took {} seconds".format(duration))

        return reports, 200




@ns.route('/<int:id>')
class ReportItem(Resource):

    @ns.marshal_with(report)
    def get(self, id):
        """
        Returns the report with the given id
        """
        report = CrimeReport.query.filter_by(id=id).one()
        return report, 200
