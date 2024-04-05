import pytest
from sqlalchemy.orm import Session

from src.models.fundamentals import (
    Base,
    CompanyMetaData,
    StatementTypeDefinition,
    FinancialStatementAttribute,
    FinancialStatementFact,
)


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
        ipo_year="1991",
        volume="123213123123",
        sector="Technology",
        industry="Hardware"
    )

    company2 = CompanyMetaData(
        symbol="MSFT",
        name="Microsoft Inc",
        market_cap=100020000,
        country="United States",
        ipo_year="1992",
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


def some_test():
    assert 1 == 0
