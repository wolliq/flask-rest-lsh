from models import CompanyModel


def test_new_company():
    """
    GIVEN a CompanyModel model
    WHEN a new CompanyModel is created
    THEN check the name, revenue and accepted are defined correctly
    """
    company = CompanyModel("my_test_company_7", 95, False)
    assert company.name == "my_test_company_7"
    assert company.revenue == 95
    assert company.accepted is False
