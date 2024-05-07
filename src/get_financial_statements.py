import asyncio
from datetime import date
from os import environ

from sqlalchemy.orm import Session

from definitions import LOCAL_STATEMENT_TYPE_TO_ENDPOINT_MAPPING
from src.utils.sql_helpers import (
    connect_to_cloud_sql,
    get_companies_to_retrieve,
)
from src.utils.requests import get_company_information
from src.models.fundamentals import (
    CompanyMetaData,
)


if __name__ == "__main__":
    engine = connect_to_cloud_sql()

    # Since we're running it every day we are going to retrieve one statement type for each day.
    STATEMENTS_MAPPING = {
        1: "income_statement",
        2: "balance_sheet_statement",
        3: "cash_flow_statement"
    }

    STATEMENT_TYPE_TO_RETRIEVE = STATEMENTS_MAPPING[(date.today().day % 3) - 1]

    companies_to_retrieve = get_companies_to_retrieve(
        engine=engine,
        statement_type=STATEMENT_TYPE_TO_RETRIEVE
    )

    endpoint = LOCAL_STATEMENT_TYPE_TO_ENDPOINT_MAPPING[STATEMENT_TYPE_TO_RETRIEVE]
    results = get_company_information(
        endpoint=endpoint,
        symbols=companies_to_retrieve,
        apikey=environ["FINANCIAL_MODELING_PREP_API_TOKEN"],
        period="annual"
    )
    # start from the companies that we haven't attempted. We will only try companies from the US market,
    # because those are the ones we will have in the CompanyMetaData table anyway
    # The table should have columns that signal whether we have each of the statements available for a given company
    # Maybe have a is_financial_statement_available, is..._statement_available flag columns?
    # Is there a way we can use only one column to flag things and still make it work?
