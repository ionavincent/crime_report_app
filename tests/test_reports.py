import json
import os
import unittest

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
                                      'month': '11',
                                      'reported_by': 'Devon & Cornwall '
                                                     'Police',
                                      'year': '2016'},
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
                                      'month': '11',
                                      'reported_by': 'Devon & Cornwall '
                                                     'Police',
                                      'year': '2016'}]

        cls.expected_responses = {1: {'context': '',
                                      'crime_id': '',
                                      'crime_type': 'Anti-social behaviour',
                                      'falls_within': 'Devon & Cornwall '
                                                      'Police',
                                      'id': 1,
                                      'last_outcome': '',
                                      'latitude': 50.8308,
                                      'location': 'On or near Hartland '
                                                  'Terrace',
                                      'longitude': -4.546074,
                                      'lsoa_code': 'E01018936',
                                      'lsoa_name': 'Cornwall 001A',
                                      'month': '11',
                                      'reported_by': 'Devon & Cornwall '
                                                     'Police',
                                      'year': '2016'},
                                  2: {'context': '',
                                      'crime_id': '38f0b9485384b64c9c4c841666'
                                                  'c923b95d3aa8f631cc65f9223'
                                                  '4ac25a154fe08',
                                      'crime_type': 'Violence and sexual '
                                                    'offences',
                                      'falls_within': 'Devon & Cornwall '
                                                      'Police',
                                      'id': 2,
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
                                  3: {'context': '',
                                      'crime_id': '8fd3e0b78717ba4b7641f41ddd'
                                                  'ea2802a768c0346c24c28208d5'
                                                  '36597a036a51',
                                      'crime_type': 'Violence and sexual '
                                                    'offences',
                                      'falls_within': 'Devon & Cornwall '
                                                      'Police',
                                      'id': 3,
                                      'last_outcome': 'Offender given '
                                                      'suspended prison '
                                                      'sentence',
                                      'latitude': 50.635262,
                                      'location': 'On or near Edymeade Court',
                                      'longitude': -4.35589,
                                      'lsoa_code': 'E01018947',
                                      'lsoa_name': 'Cornwall 005B',
                                      'month': '11',
                                      'reported_by': 'Devon & Cornwall Police',
                                      'year': '2016'}}

    def setUp(self):
        self.test_csv = CsvFile(
            name="crime_reports.csv",
            reader=open(os.path.join(os.path.dirname(__file__),
                                     "data",
                                     "crime_reports.csv"), "r")
        )

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
            self.assertDictEqual(report, self.expected_responses[report["id"]])

    def test_ingest_csv(self):
        self.ingestor.ingest_csv(self.test_csv)

        response = self.client.get("/reports")
        self.assertEqual(len(json.loads(response.data)), 3)
        response_json = json.loads(response.data)

        for report in response_json:
            self.assertDictEqual(report, self.expected_responses[report["id"]])

    def test_get_content_list(self):
        reports = self.ingestor._get_content_list(self.test_csv)
        self.assertEqual(reports, self.expected_dict_reports)

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
            self.assertDictEqual(report, self.expected_responses[report["id"]])
