from datetime import date, timedelta
from sqlalchemy.orm import Session

from stock_market_research_workloads.models.fundamentals import (
    CompanyMetaData,
    RetrievedStatementsLog,
    StatementTypeDefinition,
)
from stock_market_research_workloads.utils.sql_helpers import get_companies_to_retrieve


def test_retrieve_different_statement_type(setup_teardown_tables, connection_engine):
    """
    We've retrieved an income statement on the previous run and on the current run we're retrieving balance sheets.
    We want to make sure the company we've retrieved the income statement for will appear in the query result
    """
    company1 = CompanyMetaData(
        symbol="PWR",
        name="Quanta Services Inc",
        market_cap=10000000,
        country="United States",
        ipo_date="1991-02-05",
        volume="123213123123",
        sector="Technology",
        industry="Hardware"
    )
    income_statement = StatementTypeDefinition(
        statement_type="income_statement"
    )
    balance_sheet = StatementTypeDefinition(
        statement_type="balance_sheet_statement"
    )
    cash_flow_statement = StatementTypeDefinition(
        statement_type="cash_flow_statement"
    )

    with Session(connection_engine) as session:
        session.add_all([
            company1,
            income_statement,
            balance_sheet,
            cash_flow_statement,
        ])
        session.commit()

    with Session(connection_engine) as session:
        income_statement = session.query(StatementTypeDefinition).filter_by(statement_type="income_statement").first()
        quanta_services = session.query(CompanyMetaData).filter_by(symbol="PWR").first()

        retrieved_income_statement_quanta = RetrievedStatementsLog(
            symbol=quanta_services.symbol,
            statement_type=income_statement.id,
        )
        session.add(retrieved_income_statement_quanta)
        session.commit()

    symbols = get_companies_to_retrieve(connection_engine, "balance_sheet_statement")
    assert "PWR" in symbols


def test_retrieve_statements_one_year_later(setup_teardown_tables, connection_engine):
    """
    We've retrieved all the statements available, one year later we want to retrieve the new statements,
    so this company has to appear in the query result.
    """
    company1 = CompanyMetaData(
        symbol="PWR",
        name="Quanta Services Inc",
        market_cap=10000000,
        country="United States",
        ipo_date="1991-02-05",
        volume="123213123123",
        sector="Technology",
        industry="Hardware"
    )
    income_statement = StatementTypeDefinition(
        statement_type="income_statement"
    )
    balance_sheet = StatementTypeDefinition(
        statement_type="balance_sheet_statement"
    )
    cash_flow_statement = StatementTypeDefinition(
        statement_type="cash_flow_statement"
    )

    with Session(connection_engine) as session:
        session.add_all([
            company1,
            income_statement,
            balance_sheet,
            cash_flow_statement,
        ])
        session.commit()

    with Session(connection_engine) as session:
        income_statement = session.query(StatementTypeDefinition).filter_by(statement_type="income_statement").first()
        quanta_services = session.query(CompanyMetaData).filter_by(symbol="PWR").first()

        one_year_ago = date.today() - timedelta(days=365)

        retrieved_income_statement_quanta = RetrievedStatementsLog(
            symbol=quanta_services.symbol,
            statement_type=income_statement.id,
            retrieval_date=one_year_ago
        )
        session.add(retrieved_income_statement_quanta)
        session.commit()

    symbols = get_companies_to_retrieve(connection_engine, "income_statement")
    assert "PWR" in symbols

    with Session(connection_engine) as session:
        income_statement = session.query(StatementTypeDefinition).filter_by(statement_type="income_statement").first()
        quanta_services = session.query(CompanyMetaData).filter_by(symbol="PWR").first()

        retrieved_income_statement_quanta = RetrievedStatementsLog(
            symbol=quanta_services.symbol,
            statement_type=income_statement.id,
        )
        session.add(retrieved_income_statement_quanta)
        session.commit()

    symbols = get_companies_to_retrieve(connection_engine, "income_statement")
    assert "PWR" not in symbols
