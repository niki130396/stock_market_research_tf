import asyncio
from datetime import date
from os import environ

from sqlalchemy.orm import Session

from definitions import LOCAL_STATEMENT_TYPE_TO_ENDPOINT_MAPPING
from stock_market_research_workloads.utils.sql_helpers import (
    connect_to_cloud_sql,
    get_companies_to_retrieve,
)
from stock_market_research_workloads.utils.requests import financial_modeling_prep_async_request
from stock_market_research_workloads.models.fundamentals import (
    StatementTypeDefinition,
    RetrievedStatementsLog,
)


if __name__ == "__main__":
    engine = connect_to_cloud_sql()

    with Session(engine) as session:
        income_statement = session.query(StatementTypeDefinition).filter_by(statement_type="income_statement").first()
        balance_sheet = session.query(StatementTypeDefinition).filter_by(statement_type="balance_sheet_statement").first()
        cash_flow_statement = session.query(StatementTypeDefinition).filter_by(statement_type="cash_flow_statement").first()

    # Since we're running it every day we are going to retrieve one statement type for each day.
    STATEMENTS_MAPPING = {
        1: income_statement,
        2: balance_sheet,
        3: cash_flow_statement
    }

    statement_type_object = STATEMENTS_MAPPING[(date.today().day % 3) - 1]

    companies_to_retrieve = get_companies_to_retrieve(
        engine=engine,
        statement_type=statement_type_object.statement_type
    )

    endpoint = LOCAL_STATEMENT_TYPE_TO_ENDPOINT_MAPPING[statement_type_object.statement_type]
    results, _ = asyncio.run(financial_modeling_prep_async_request(
        endpoint=endpoint,
        symbols=companies_to_retrieve,
        apikey=environ["FINANCIAL_MODELING_PREP_API_TOKEN"],
        period="annual"
    ))

    retrieved_statement_logs = []
    for symbol in companies_to_retrieve:
        obj = RetrievedStatementsLog(
            symbol=symbol,
            statement_type=statement_type_object.id
        )
        retrieved_statement_logs.append(obj)

    with Session(engine) as session:
        session.add_all(retrieved_statement_logs)
        session.commit()



    # start from the companies that we haven't attempted. We will only try companies from the US market,
    # because those are the ones we will have in the CompanyMetaData table anyway
    # The table should have columns that signal whether we have each of the statements available for a given company
    # Maybe have a is_financial_statement_available, is..._statement_available flag columns?
    # Is there a way we can use only one column to flag things and still make it work?
