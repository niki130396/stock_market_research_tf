import pytest
from sqlalchemy.orm import Session

from src.models.fundamentals import (
    Base,
    CompanyMetaData,
    StatementTypeDefinition,
    FinancialStatementAttribute,
    FinancialStatementFact,
)
from src.utils.validation_schemas import COMPANY_METADATA_RESPONSE_SCHEMA_VALIDATOR


def test_db_engine_is_sqlite(connection_engine):
    engine = connection_engine

    assert engine.url.get_driver_name() == "pysqlite"


def test_tables_created(setup_teardown_tables, connection_engine):
    tables = Base.metadata.tables
    assert "company_meta_data" in tables
    assert "statement_type_definition" in tables
    assert "financial_statement_attribute" in tables
    assert "financial_statement_fact" in tables


def test_models(setup_teardown_tables, connection_engine):
    engine = connection_engine

    company1 = CompanyMetaData(
        symbol="AAPL",
        name="Apple Inc",
        market_cap=10000000,
        country="United States",
        ipo_date="1991-02-05",
        volume="123213123123",
        sector="Technology",
        industry="Hardware"
    )

    company2 = CompanyMetaData(
        symbol="MSFT",
        name="Microsoft Inc",
        market_cap=100020000,
        country="United States",
        ipo_date="1992-01-01",
        volume="1232131123123",
        sector="Technology",
        industry="Software"
    )

    with Session(engine) as session:
        session.add_all([company1, company2])
        session.commit()

    income_statement = StatementTypeDefinition(
        statement_type="income_statement"
    )
    balance_sheet = StatementTypeDefinition(
        statement_type="balance_sheet"
    )
    cash_flow_statement = StatementTypeDefinition(
        statement_type="cash_flow_statement"
    )

    with Session(engine) as session:
        session.add_all([income_statement, balance_sheet, cash_flow_statement])
        session.commit()

    with Session(engine) as session:
        companies = session.query(CompanyMetaData).all()
        for company in companies:
            assert company.symbol in ["AAPL", "MSFT"]

    with Session(engine) as session:
        income_statement = session.query(StatementTypeDefinition).filter_by(statement_type="income_statement").first()

        revenue = FinancialStatementAttribute(
            name="revenue",
            friendly_name="Revenue",
            description="This is the revenue",
            statement_type_id=income_statement.id,
            statement_type=income_statement
        )
        cost_of_revenue = FinancialStatementAttribute(
            name="costOfRevenue",
            friendly_name="Cost of Revenue",
            description="This is the cost of revenue",
            statement_type_id=income_statement.id,
            statement_type=income_statement
        )
        gross_profit = FinancialStatementAttribute(
            name="grossProfit",
            friendly_name="Gross Profit",
            description="This is the gross profit",
            statement_type_id=income_statement.id,
            statement_type=income_statement
        )

        session.add_all([revenue, cost_of_revenue, gross_profit])
        session.commit()

    with Session(engine) as session:
        financial_statement_attributes = session.query(FinancialStatementAttribute).all()
        for attribute in financial_statement_attributes:
            assert attribute.name in ["revenue", "costOfRevenue", "grossProfit"]

    with Session(engine) as session:
        aapl = session.query(CompanyMetaData).filter_by(symbol="AAPL").first()
        revenue = session.query(FinancialStatementAttribute).filter_by(name="revenue").first()
        cost_of_revenue = session.query(FinancialStatementAttribute).filter_by(name="costOfRevenue").first()
        gross_profit = session.query(FinancialStatementAttribute).filter_by(name="grossProfit").first()
        revenue_aapl_2024_q1 = FinancialStatementFact(
            company_symbol=aapl.symbol,
            financial_statement_attribute=revenue.id,
            fiscal_year=2024,
            value=1_000_000_000
        )
        cost_of_revenue_aapl_2024_q1 = FinancialStatementFact(
            company_symbol=aapl.symbol,
            financial_statement_attribute=cost_of_revenue.id,
            fiscal_year=2024,
            value=700_000_000
        )
        gross_profit_aapl_2024_q1 = FinancialStatementFact(
            company_symbol=aapl.symbol,
            financial_statement_attribute=gross_profit.id,
            fiscal_year=2024,
            value=300_000_000
        )

        session.add_all([revenue_aapl_2024_q1, cost_of_revenue_aapl_2024_q1, gross_profit_aapl_2024_q1])
        session.commit()

    with Session(engine) as session:
        revenue_aapl_2024_q1 = session.query(FinancialStatementFact).filter_by(company_symbol="AAPL").first()
        revenue = session.query(FinancialStatementAttribute).filter_by(id=revenue_aapl_2024_q1.financial_statement_attribute).first()
        assert revenue_aapl_2024_q1.value == 1_000_000_000
        assert revenue.name == "revenue"
        assert revenue.friendly_name == "Revenue"


def test_model_with_mixin(setup_teardown_tables, connection_engine):
    engine = connection_engine

    test_data = {
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
        "ipoDate": "1980-12-12",
        "cik": "0000320193",
        "isin": "US0378331005",
        "cusip": "037833100",
        "exchange": "NASDAQ Global Select",
        "exchangeShortName": "NASDAQ",
        "industry": "Consumer Electronics",
        "description": "Apple Inc.",
        "ceo": "Mr. Timothy D. Cook",
        "sector": "Technology",
        "country": "US",
        "fullTimeEmployees": "164000",
    }
    company1 = CompanyMetaData.map_fields(
        COMPANY_METADATA_RESPONSE_SCHEMA_VALIDATOR, test_data
    )

    with Session(engine) as session:
        session.add(company1)
        session.commit()

        aapl = session.query(CompanyMetaData).filter_by(symbol="AAPL").first()

        assert aapl.currency == "USD"
