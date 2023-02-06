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


def test_new_company_with_fixture(new_company):
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the email and password_hashed fields are defined correctly
    """
    assert new_company.name == "my_test_company_7"
    assert new_company.revenue != 100
