from flask_restplus import reqparse


reports_request_parser = reqparse.RequestParser()
reports_request_parser.add_argument(
    "order_by",
    required=False,
    help="Order by (e.g. 'crime_type', 'year')",
    type=str,
    location="args"
)
reports_request_parser.add_argument(
    "limit",
    required=False,
    help="Number of results to return",
    type=int,
    location="args",
    default=-1
)
reports_request_parser.add_argument(
    "crime_id",
    required=False,
    help="Crime ID",
    type=str,
    location="args"
)
reports_request_parser.add_argument(
    "year",
    required=False,
    help="Year",
    type=int,
    location="args"
)
reports_request_parser.add_argument(
    "month",
    required=False,
    help="Month",
    type=int,
    location="args"
)
reports_request_parser.add_argument(
    "reported_by",
    required=False,
    help="Reported by",
    type=str,
    location="args"
)
reports_request_parser.add_argument(
    "falls_within",
    required=False,
    help="Falls within",
    type=str,
    location="args"
)
reports_request_parser.add_argument(
    "longitude",
    required=False,
    help="Longitude",
    type=float,
    location="args"
)
reports_request_parser.add_argument(
    "latitude",
    required=False,
    help="Latitude",
    type=float,
    location="args"
)
reports_request_parser.add_argument(
    "location",
    required=False,
    help="Location",
    type=str,
    location="args"
)
reports_request_parser.add_argument(
    "lsoa_code",
    required=False,
    help="LSAO code",
    type=str,
    location="args"
)
reports_request_parser.add_argument(
    "lsoa_name",
    required=False,
    help="LSAO name",
    type=str,
    location="args"
)
reports_request_parser.add_argument(
    "crime_type",
    required=False,
    help="Crime type",
    type=str,
    location="args"
)
reports_request_parser.add_argument(
    "last_outcome",
    required=False,
    help="Last outcome",
    type=str,
    location="args"
)
reports_request_parser.add_argument(
    "context",
    required=False,
    help="Context",
    type=str,
    location="args"
)
