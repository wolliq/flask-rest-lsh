from db import db


class CompanyModel(db.Model):
    __tablename__ = "company"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    revenue = db.Column(db.Integer, unique=False, nullable=False)
    accepted = db.Column(db.Boolean, unique=False, nullable=False)

    def __init__(self, name: str, revenue: int, accepted: bool):
        """
        Create a new CompanyModel object
        :param name:
        :param revenue:
        :param accepted:
        """
        self.name = name
        self.revenue = revenue
        self.accepted = accepted

    def __repr__(self):
        return f'<CompanyModel: {self.name}>'
