from sqlalchemy.orm import Session

from src.utils.sql_helpers import connect_to_cloud_sql
from src.models.fundamentals import (
    CompanyMetaData,
)

if __name__ == "__main__":
    engine = connect_to_cloud_sql()

    with Session(engine) as session:
        companies_to_process = session.query(CompanyMetaData).filter(
            ~CompanyMetaData.statements_flag.op("&")(7) == 7
        ).all()
    # start from the companies that we haven't attempted. We will only try companies from the US market,
    # because those are the ones we will have in the CompanyMetaData table anyway
    # The table should have columns that signal whether we have each of the statements available for a given company
    # Maybe have a is_financial_statement_available, is..._statement_available flag columns?
    # Is there a way we can use only one column to flag things and still make it work?


