import argparse
import csv
import io
import logging
import zipfile
from collections import namedtuple

from app import app
from config import configure_app
from .models import CrimeReport
from . import db


CsvFile = namedtuple("CsvFile", ["name", "reader"])


class CrimeDataIngestor(object):

    def __init__(self, db):
        self.db = db
        logging.basicConfig(level=logging.INFO)

    def import_data(self, zip_file_path):
        """
        Imports the crime reports in the contained CSVs into the database
        :param zip_file_path: The full file path to a zip containing crime
        report CSVs
        :return: None
        """
        for csv_file in self._extract_zip(zip_file_path):
            self.ingest_csv(csv_file)

    def ingest_csv(self, csv_file):
        """
        Ingests each crime report in the given CSV into the database
        :param csv_file: The CsvFile tuple containing crime data
        :return: None
        """
        logging.info(("ingesting: {}").format(csv_file.name))
        reports = self._get_content_list(csv_file)
        self._bulk_import_reports(reports)

    def _get_content_list(self, csv_file):
        """
        Extracts all crime reports in the given csv into memory
        :param csv_file: The CsvFile tuple containing crime data
        :return: A list of dictionaries containing the data for each crime
        report
        """
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
        csv_file.reader.readline()

        reader = csv.DictReader(csv_file.reader, fieldnames=fieldnames)

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

    def _bulk_import_reports(self, reports):
        """
        Inserts a list of crime reports in to the database
        :param reports: A list of dictionaries containing all fields and values
        for each crime report
        :return: None
        """
        self.db.engine.execute(CrimeReport.__table__.insert(), reports)

    def _extract_zip(self, zip_file_path):
        """
        Extracts all CSVs in provided ZIP file into memory
        :param zip_file_path: The full file path to the zip file
        :return: A list of CsvFile tuples containing the file name and its
        file handler
        """
        input_zip = zipfile.ZipFile(zip_file_path)
        return [CsvFile(name,
                        io.StringIO(input_zip.read(name).decode("utf-8")))
                for name in input_zip.namelist() if name.endswith(".csv")]

    def _get_month(self, date):
        return date.split("-")[1]

    def _get_year(self, date):
        return date.split("-")[0]


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--csv", help="the file path to the crime data csv")
    parser.add_argument("--zip", help="the file path to a zip containing crime"
                        " report csvs, in dated directories")
    args = parser.parse_args()

    with app.app_context():
        configure_app(app, "default")
        db.init_app(app)

        ingestor = CrimeDataIngestor(db=db)

        if args.csv:
            ingestor.ingest_csv(args.csv)
        elif args.zip:
            ingestor.import_data(args.zip)
