import pandas as pd
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from db import db
from models import CompanyModel
from schemas import CompanySchema
from scorers.scorer import SparkLshScorer

blp = Blueprint("Company", "company", description="Operations on companies")


@blp.route("/score/<string:company_id>")
class CompanyScore(MethodView):
    def get(self, company_id):
        CompanyModel.query.get_or_404(company_id)

        companies = CompanyModel.query.all()

        df_companies = pd.DataFrame(
                [c.__dict__ for c in companies]
            ).drop(columns='_sa_instance_state')

        print(df_companies.head(10))

        scorer = SparkLshScorer(model_provider="spark",
                                dataset=df_companies,
                                company_id=company_id)

        scorer.process_delta_feature_store(dataset_path=f"./lakehouse/company")
        scorer.train(model_path="./lsh_brp", save_model=True)
        res = scorer.score()

        return {"message": f"Company credit advice: {res}."}


@blp.route("/company/<string:company_id>")
class Company(MethodView):
    @blp.response(200, CompanySchema)
    def get(self, company_id):
        company = CompanyModel.query.get_or_404(company_id)
        return company

    def delete(self, company_id):
        company = CompanyModel.query.get_or_404(company_id)
        db.session.delete(company)
        db.session.commit()
        return {"message": "Company deleted."}

    @blp.arguments(CompanySchema)
    @blp.response(200, CompanySchema)
    def put(self, company_data, company_id):
        company = Company.query.get(company_id)

        if company:
            company.name = company_data["name"]
            company.revenue = company_data["revenue"]
        else:
            company = CompanyModel(id=company_id, **company_data)

        db.session.add(company)
        db.session.commit()

        return company


@blp.route("/company")
class CompanyList(MethodView):
    @blp.response(200, CompanySchema(many=True))
    def get(self):
        return CompanyModel.query.all()

    @blp.arguments(CompanySchema)
    @blp.response(201, CompanySchema)
    def post(self, company_data):
        company = CompanyModel(**company_data)

        try:
            db.session.add(company)
            db.session.commit()
        except IntegrityError:
            abort(
                400,
                message="A company with that name already exists.",
            )
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the company.")

        return company
