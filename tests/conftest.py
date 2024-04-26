import pytest
from sqlalchemy import create_engine

from src.models.fundamentals import Base


@pytest.fixture
def connection_engine():
    return create_engine("sqlite:///:memory:")


@pytest.fixture
def setup_teardown_tables(connection_engine):
    Base.metadata.create_all(connection_engine)

    yield

    Base.metadata.drop_all(connection_engine)


class MockResponse:
    def __init__(self, json):
        self._json = json

    async def json(self):
        return self._json

    async def __aexit__(self, exc_type, exc, tb):
        pass

    async def __aenter__(self):
        return self


@pytest.fixture
def patch_client_response_get_company_information(monkeypatch):
    def patch(*args, **kwargs):
        mocker = MockResponse([
            {
                "symbol": "AAPL",
                "price": 178.72,
                "beta": 1.286802,
                "volAvg": 58405568,
                "mktCap": 2794144143933,
                "lastDiv": 0.96,
                "range": "124.17-198.23",
                "changes": -0.13,
                "companyName": "Apple Inc.",
                "currency": "USD",
                "cik": "0000320193",
                "isin": "US0378331005",
                "cusip": "037833100",
                "exchange": "NASDAQ Global Select",
                "exchangeShortName": "NASDAQ",
                "industry": "Consumer Electronics",
                "website": "https://www.apple.com",
                "description": "Apple Inc. designs, manufactures, and markets smartphones, personal computers, tablets, ",
                "ceo": "Mr. Timothy D. Cook",
                "sector": "Technology",
                "country": "US",
                "fullTimeEmployees": "164000",
                "phone": "408 996 1010",
                "address": "One Apple Park Way",
                "city": "Cupertino",
                "state": "CA",
                "zip": "95014",
                "dcfDiff": 4.15176,
                "dcf": 150.082,
                "image": "https://financialmodelingprep.com/image-stock/AAPL.png",
                "ipoDate": "1980-12-12",
                "defaultImage": False,
                "isEtf": False,
                "isActivelyTrading": False,
                "isAdr": False,
                "isFund": False
            }
        ])
        return mocker

    monkeypatch.setattr("src.utils.requests.aiohttp.ClientSession.get", patch)


@pytest.fixture
def patch_client_response_get_company_information_free_plan(monkeypatch):
    def patch(*args, **kwargs):
        mocker = MockResponse({
            "Error Message": "Free plan is limited to US stocks only please visit our subscription page to upgrade your plan at https://site.financialmodelingprep.com/developer/docs/pricing"
        })
        return mocker

    monkeypatch.setattr("src.utils.requests.aiohttp.ClientSession.get", patch)


@pytest.fixture
def patch_client_response_get_company_information_limit_reach(monkeypatch):
    def patch(*args, **kwargs):
        mocker = MockResponse({
            "Error Message": "Limit Reach ."
        })
        return mocker

    monkeypatch.setattr("src.utils.requests.aiohttp.ClientSession.get", patch)
