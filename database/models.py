from database import db


class CrimeReport(db.Model):
    """
    SQLAlchemy model for the database entry for each crime report
    """
    __tablename__ = "CrimeReport"
    id = db.Column(db.Integer, primary_key=True)
    crime_id = db.Column(db.String(255))
    year = db.Column(db.Integer)
    month = db.Column(db.Integer)
    reported_by = db.Column(db.String(255))
    falls_within = db.Column(db.String(255))
    longitude = db.Column(db.Float)
    latitude = db.Column(db.Float)
    location = db.Column(db.String(255))
    lsoa_code = db.Column(db.String(255))
    lsoa_name = db.Column(db.String(255))
    crime_type = db.Column(db.String(255), index=True)
    last_outcome = db.Column(db.String(255))
    context = db.Column(db.String(255))

    @staticmethod
    def from_json(data):
        """
        Creates a CrimeReport object from the supplied json
        :param data: json
        :return: CrimeReport
        """
        name = data.get("name")
        type = data.get("type")
        if not name:
            raise RuntimeError("No event name given")
        return CrimeReport(name=name, type=type)
