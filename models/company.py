from db import db


class CompanyModel(db.Model):
    __tablename__ = "company"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    revenue = db.Column(db.Integer, unique=False, nullable=False)
    accepted = db.Column(db.Boolean, unique=False, nullable=False)