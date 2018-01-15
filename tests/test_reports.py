import json
import os
import unittest
from collections import OrderedDict

from flask import Flask

from app import init_app
from database import db
from database.import_crime_reports import CsvFile, CrimeDataIngestor


class TimeReportsCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.expected_dict_reports = [{'context': '',
                                      'crime_id': '',
                                      'crime_type': 'Anti-social behaviour',
                                      'falls_within': 'Devon & Cornwall '
                                                      'Police',
                                      'last_outcome': '',
                                      'latitude': 50.8308,
                                      'location': 'On or near Hartland '
                                                  'Terrace',
                                      'longitude': -4.546074,
                                      'lsoa_code': 'E01018936',
                                      'lsoa_name': 'Cornwall 001A',
                                      'month': '01',
                                      'reported_by': 'Devon & Cornwall '
                                                     'Police',
                                      'year': '2017'},
                                     {'context': '',
                                      'crime_id': '38f0b9485384b64c9c4c841666'
                                                  'c923b95d3aa8f631cc65f92234'
                                                  'ac25a154fe08',
                                      'crime_type': 'Violence and sexual '
                                                    'offences',
                                      'falls_within': 'Devon & Cornwall '
                                                      'Police',
                                      'last_outcome': 'Unable to prosecute '
                                                      'suspect',
                                      'latitude': 50.828441,
                                      'location': 'On or near Church Path',
                                      'longitude': -4.551129,
                                      'lsoa_code': 'E01018936',
                                      'lsoa_name': 'Cornwall 001A',
                                      'month': '11',
                                      'reported_by': 'Devon & Cornwall Police',
                                      'year': '2016'},
                                     {'context': '',
                                      'crime_id': '8fd3e0b78717ba4b7641f41ddd'
                                                  'ea2802a768c0346c24c28208d5'
                                                  '36597a036a51',
                                      'crime_type': 'Violence and sexual '
                                                    'offences',
                                      'falls_within': 'Devon & Cornwall '
                                                      'Police',
                                      'last_outcome': 'Offender given '
                                                      'suspended prison '
                                                      'sentence',
                                      'latitude': 50.635262,
                                      'location': 'On or near Edymeade Court',
                                      'longitude': -4.35589,
                                      'lsoa_code': 'E01018947',
                                      'lsoa_name': 'Cornwall 005B',
                                      'month': '10',
                                      'reported_by': 'Devon & Cornwall '
                                                     'Police',
                                      'year': '2015'}]

    def setUp(self):
        self.test_csv = CsvFile(
            name="crime_reports.csv",
            reader=open(os.path.join(os.path.dirname(__file__),
                                     "data",
                                     "crime_reports.csv"), "r")
        )

        with open(os.path.join(os.path.dirname(__file__),
                               "data",
                               "expected_response.json")) as f:
            self.expected_responses = json.load(f)

        self.test_app = Flask(__name__)
        self.app_context = self.test_app.app_context()
        self.app_context.push()
        init_app(self.test_app, "testing")
        db.init_app(self.test_app)
        db.create_all()

        self.client = self.test_app.test_client()
        self.client.testing = True

        self.ingestor = CrimeDataIngestor(db=db)

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_bulk_import_reports(self):
        report_dicts = self.ingestor._get_content_list(self.test_csv)
        self.ingestor._bulk_import_reports(report_dicts)

        response = self.client.get("/reports")

        self.assertEqual(len(json.loads(response.data)), 3)
        response_json = json.loads(response.data)

        for report in response_json:
            self.assertDictEqual(
                report, self.expected_responses[str(report["id"])])

    def test_ingest_csv(self):
        self.ingestor.ingest_csv(self.test_csv)

        response = self.client.get("/reports")
        self.assertEqual(len(json.loads(response.data)), 3)
        response_json = json.loads(response.data)

        for report in response_json:
            self.assertDictEqual(
                report, self.expected_responses[str(report["id"])])

    def test_get_content_list(self):
        self.maxDiff = None
        reports = self.ingestor._get_content_list(self.test_csv)
        for i, report in enumerate(reports):
            self.assertDictEqual(
                OrderedDict(sorted(report.items())),
                OrderedDict(sorted(self.expected_dict_reports[i].items()))
            )

    def test_get_month(self):
        month = self.ingestor._get_month("2015-3")
        self.assertEqual(month, "3")

    def test_get_year(self):
        year = self.ingestor._get_year("2015-3")
        self.assertEqual(year, "2015")

    def test_get_reports(self):
        # populate db with dummy data
        self.ingestor.ingest_csv(self.test_csv)

        # validate returned data is correct
        response = self.client.get("/reports")
        self.assertEqual(len(json.loads(response.data)), 3)

        response_json = json.loads(response.data)

        for report in response_json:
            self.assertDictEqual(
                report, self.expected_responses[str(report["id"])])

    def test_get_filtered_by_crime_id(self):
        self.ingestor.ingest_csv(self.test_csv)
        response = self.client.get("/reports?crime_id=38f0b9485384b64c9c4c84"
                                   "1666c923b95d3aa8f631cc65f92234ac25a154fe"
                                   "08")
        reports = json.loads(response.data)
        self.assertEqual(len(reports), 1)
        self.assertEqual(
            len([r for r in reports if r["crime_id"] == "38f0b9485384b64c9c4c"
                                                        "841666c923b95d3aa8f"
                                                        "631cc65f92234ac25a15"
                                                        "4fe08"]), 1
        )

    def test_get_filtered_by_year(self):
        self.ingestor.ingest_csv(self.test_csv)
        response = self.client.get("/reports?year=2016")
        reports = json.loads(response.data)
        self.assertEqual(len(reports), 1)
        self.assertEqual(
            len([r for r in reports if r["year"] == 2016]), 1
        )

    def test_get_filtered_by_month(self):
        self.ingestor.ingest_csv(self.test_csv)
        response = self.client.get("/reports?month=10")
        reports = json.loads(response.data)
        self.assertEqual(len(reports), 1)
        self.assertEqual(
            len([r for r in reports if r["month"] == 10]), 1
        )

    def test_get_filtered_by_reported_by(self):
        self.ingestor.ingest_csv(self.test_csv)
        response = self.client.get("/reports?reported_by=Devon %26 "
                                   "Cornwall Police")
        reports = json.loads(response.data)
        self.assertEqual(len(reports), 3)
        self.assertEqual(len([r for r in reports if r["reported_by"] ==
                              "Devon & Cornwall Police"]), 3
                         )

    def test_get_filtered_by_falls_within(self):
        self.ingestor.ingest_csv(self.test_csv)
        response = self.client.get("/reports?falls_within=Devon %26 "
                                   "Cornwall Police")
        reports = json.loads(response.data)
        self.assertEqual(len(reports), 3)
        self.assertEqual(len([r for r in reports if r["falls_within"] ==
                              "Devon & Cornwall Police"]), 3
                         )

    def test_get_filtered_by_longitude(self):
        self.ingestor.ingest_csv(self.test_csv)
        response = self.client.get("/reports?longitude=%2D4.546074")
        reports = json.loads(response.data)
        self.assertEqual(len(reports), 1)
        self.assertEqual(len([r for r in reports if r["longitude"] ==
                              -4.546074]), 1
                         )

    def test_get_filtered_by_latitude(self):
        self.ingestor.ingest_csv(self.test_csv)
        response = self.client.get("/reports?latitude=50.830800")
        reports = json.loads(response.data)
        self.assertEqual(len(reports), 1)
        self.assertEqual(len([r for r in reports if r["latitude"] ==
                              50.830800]), 1
                         )

    def test_get_filtered_by_location(self):
        self.ingestor.ingest_csv(self.test_csv)
        response = self.client.get("/reports?location=On or near Church Path")
        reports = json.loads(response.data)
        self.assertEqual(len(reports), 1)
        self.assertEqual(len([r for r in reports if r["location"] ==
                              "On or near Church Path"]), 1
                         )

    def test_get_filtered_by_lsoa_code(self):
        self.ingestor.ingest_csv(self.test_csv)
        response = self.client.get("/reports?lsoa_code=E01018936")
        reports = json.loads(response.data)
        self.assertEqual(len(reports), 2)
        self.assertEqual(len([r for r in reports if r["lsoa_code"] ==
                              "E01018936"]), 2
                         )

    def test_get_filtered_by_lsoa_name(self):
        self.ingestor.ingest_csv(self.test_csv)
        response = self.client.get("/reports?lsoa_name=Cornwall 001A")
        reports = json.loads(response.data)
        self.assertEqual(len(reports), 2)
        self.assertEqual(len([r for r in reports if r["lsoa_name"] ==
                              "Cornwall 001A"]), 2
                         )

    def test_get_filtered_by_crime_type(self):
        self.ingestor.ingest_csv(self.test_csv)
        response = self.client.get("/reports?crime_type=Violence and sexual "
                                   "offences")
        reports = json.loads(response.data)
        self.assertEqual(len(reports), 2)

        self.assertEqual(
            len([r for r in reports if r["crime_type"] ==
                 "Violence and sexual offences"]),
            2
        )

    def test_get_filtered_by_last_outcome(self):
        self.ingestor.ingest_csv(self.test_csv)
        response = self.client.get("/reports?last_outcome=Offender given "
                                   "suspended prison sentence")
        reports = json.loads(response.data)
        self.assertEqual(len(reports), 1)

        self.assertEqual(
            len([r for r in reports if r["last_outcome"] ==
                 "Offender given suspended prison "
                 "sentence"]),
            1
        )

    def test_get_filtered_by_context(self):
        self.ingestor.ingest_csv(self.test_csv)
        response = self.client.get("/reports?context=")
        reports = json.loads(response.data)
        self.assertEqual(len(reports), 3)

        self.assertEqual(
            len([r for r in reports if r["context"] ==
                 ""]),
            3
        )

    def test_get_sorted_by_year(self):
        self.ingestor.ingest_csv(self.test_csv)
        response = self.client.get("/reports?order_by=year")
        reports = json.loads(response.data)
        self.assertEqual(len(reports), 3)
        self.assertEqual(
            reports[0]["crime_id"],
            "8fd3e0b78717ba4b7641f41dddea2802a768c0346c24c28208d536597a036a51"
        )
        self.assertEqual(
            reports[1]["crime_id"],
            "38f0b9485384b64c9c4c841666c923b95d3aa8f631cc65f92234ac25a154fe08"
        )
        self.assertEqual(
            reports[2]["crime_id"],
            ""
        )

    def test_get_sorted_by_month(self):
        self.ingestor.ingest_csv(self.test_csv)
        response = self.client.get("/reports?order_by=month")
        reports = json.loads(response.data)
        self.assertEqual(len(reports), 3)
        self.assertEqual(
            reports[0]["crime_id"],
            ""
        )
        self.assertEqual(
            reports[1]["crime_id"],
            "8fd3e0b78717ba4b7641f41dddea2802a768c0346c24c28208d536597a036a51"
        )
        self.assertEqual(
            reports[2]["crime_id"],
            "38f0b9485384b64c9c4c841666c923b95d3aa8f631cc65f92234ac25a154fe08"
        )

    def test_get_sorted_by_crime_type(self):
        self.ingestor.ingest_csv(self.test_csv)
        response = self.client.get("/reports?order_by=month")
        reports = json.loads(response.data)
        self.assertEqual(len(reports), 3)
        self.assertEqual(
            reports[0]["crime_id"],
            ""
        )
        self.assertEqual(
            reports[1]["crime_id"],
            "8fd3e0b78717ba4b7641f41dddea2802a768c0346c24c28208d536597a036a51"
        )
        self.assertEqual(
            reports[2]["crime_id"],
            "38f0b9485384b64c9c4c841666c923b95d3aa8f631cc65f92234ac25a154fe08"
        )
