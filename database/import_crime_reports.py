import argparse
import csv
import logging
import os
import zipfile

from app import app
from config import configure_app
from models import CrimeReport
from . import db


class CrimeDataIngestor(object):

    def __init__(self, db):
        self.db = db
        logging.basicConfig(level=logging.INFO)

    def import_data(self, zip_file_path):
        unziped_dir = self._unzip_data(zip_file_path)

        paths = self._get_all_csv_paths(unziped_dir)

        for p in paths:
            self.ingest_csv(p)

    def ingest_csv(self, csv_file_path):
        logging.info(("ingesting: {}").format(csv_file_path))
        reports = self._get_dict_representations(csv_file_path)
        self._bulk_import_reports(reports)

    def _get_dict_representations(self, csv_file_path):

        with open(csv_file_path) as csv_file:
            reports = self._get_content_list(csv_file)

        return reports

    def _get_content_list(self, file_handler):
        reports = []
        fieldnames = ("crime_id",
                      "date",
                      "reported_by",
                      "falls_within",
                      "longitude",
                      "latitude",
                      "location",
                      "lsoa_code",
                      "lsoa_name",
                      "crime_type",
                      "last_outcome",
                      "context")

        # skip the first line of the file containing the headers
        file_handler.readline()

        reader = csv.DictReader(file_handler, fieldnames=fieldnames)

        for row in reader:
            row["year"] = self._get_year(row["date"])
            row["month"] = self._get_month(row["date"])
            row["longitude"] = float(row["longitude"]) if \
                row["longitude"] else None
            row["latitude"] = float(row["latitude"]) if \
                row["latitude"] else None
            del row["date"]
            reports.append(row)

        return reports

    def _get_all_csv_paths(self, top_level_dir):
        all_paths = []

        for root, dir, files in os.walk(top_level_dir):
            if root == top_level_dir:
                continue

            for f in files:
                if f.endswith('csv'):
                    all_paths.append(os.path.join(root, f))

        return all_paths

    def _bulk_import_reports(self, reports):
        self.db.engine.execute(CrimeReport.__table__.insert(), reports)

    def _unzip_data(self, zip_file_path):
        zip_ref = zipfile.ZipFile(zip_file_path, 'r')

        dirname, filename = os.path.split(os.path.abspath(__file__))
        temp_dir = os.path.join(dirname, "temp")

        zip_ref.extractall(temp_dir)
        zip_ref.close()

        return temp_dir

    def _get_month(self, date):
        return date.split("-")[1]

    def _get_year(self, date):
        return date.split("-")[0]


if __name__=="__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--csv", help="the file path to the crime data csv")
    parser.add_argument("--zip", help="the file path to a zip containing crime "
                                    "report csvs, in dated directories")
    args = parser.parse_args()

    with app.app_context():
        configure_app(app, "default")
        db.init_app(app)

        ingestor = CrimeDataIngestor(db=db)

        if args.csv:
            ingestor.ingest_csv(args.csv)
        elif args.zip:
            ingestor.import_data(args.zip)
