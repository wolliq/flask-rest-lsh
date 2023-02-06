import pytest


from models import CompanyModel


# --------
# Fixtures
# --------

@pytest.fixture(scope='module')
def new_company():
    company = CompanyModel("my_test_company_7", 95, False)
    return company
