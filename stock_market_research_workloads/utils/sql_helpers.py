import os

from google.cloud.sql.connector import Connector, IPTypes
import pg8000
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import Session
from sqlalchemy import (
    create_engine,
    func,
)

from stock_market_research_workloads.models.fundamentals import (
    CompanyMetaData,
    RetrievedStatementsLog,
    StatementTypeDefinition,
)


def connect_to_cloud_sql() -> Engine:
    """
    Initializes a connection pool for a Cloud SQL instance of Postgres.

    Uses the Cloud SQL Python Connector package.
    """

    instance_connection_name = os.environ["STOCK_MARKET_RESEARCH_DB_HOST"]
    db_user = os.environ["STOCK_MARKET_RESEARCH_DB_USERNAME"]
    db_pass = os.environ["STOCK_MARKET_RESEARCH_DB_USER_PASSWORD"]
    db_name = "postgres"  # e.g. 'my-database'

    ip_type = IPTypes.PRIVATE if os.environ.get("PRIVATE_IP") else IPTypes.PUBLIC

    # initialize Cloud SQL Python Connector object
    connector = Connector()

    def getconn() -> pg8000.dbapi.Connection:
        conn: pg8000.dbapi.Connection = connector.connect(
            instance_connection_name,
            "pg8000",
            user=db_user,
            password=db_pass,
            db=db_name,
            ip_type=ip_type,
        )
        return conn

    # The Cloud SQL Python Connector can be used with SQLAlchemy
    # using the 'creator' argument to 'create_engine'
    pool = create_engine(
        "postgresql+pg8000://",
        creator=getconn,
        # ...
    )
    return pool


def get_companies_to_retrieve(engine, statement_type, days_threshold=365, limit=200):
    """
    Retrieve symbols of companies for which statements need to be retrieved based on specified criteria.

    This function queries the database to identify symbols of companies for which financial statements
    need to be retrieved, considering the specified statement type, days threshold since the last retrieval,
    and limit on the number of results.

    Args:
        engine (Engine): SQLAlchemy engine object used for database connection.
        statement_type (str): Type of statement to retrieve ('Income Statement', 'Balance Sheet', 'Cash Flow Statement').
        days_threshold (int, optional): Number of days threshold since the last retrieval (default: 365).
        limit (int, optional): Maximum number of results to return (default: 200).

    Returns:
        List[str]: List of company symbols for which statements need to be retrieved.

    Example:
        # Create an engine
        engine = create_engine('sqlite:///your_database.db')

        # Retrieve symbols of companies for which balance sheets need to be retrieved
        symbols_to_retrieve = get_companies_to_retrieve(engine, 'Balance Sheet', days_threshold=365, limit=200)

    Example Case:
        Assume the function is called to collect balance sheets after income statements have already been collected.
        If a company's income statement has been collected previously, but its balance sheet has not,
        and it satisfies the days threshold condition, its symbol should be included in the output.

        Additionally, if 365 days or more have passed since the last retrieval of a given statement type
        for a given company, it will also be included in the output.
    """
    with Session(engine) as session:
        # Subquery to get symbols for which statements have been retrieved
        subquery_stmt = session.query(RetrievedStatementsLog.symbol.distinct().label("symbol")).join(
            StatementTypeDefinition,
            RetrievedStatementsLog.statement_type == StatementTypeDefinition.id
        ).filter(
            StatementTypeDefinition.statement_type == statement_type
        ).subquery()

        # Subquery to get the maximum retrieval date for each company symbol for statements
        subquery_max_date = session.query(
            RetrievedStatementsLog.symbol,
            func.max(RetrievedStatementsLog.retrieval_date).label('last_retrieval_date')
        ).join(
            StatementTypeDefinition,
            RetrievedStatementsLog.statement_type == StatementTypeDefinition.id
        ).filter(
            StatementTypeDefinition.statement_type == statement_type
        ).group_by(RetrievedStatementsLog.symbol).subquery()

        # Query to retrieve symbols of companies for which statements need to be retrieved
        query = session.query(CompanyMetaData.symbol).outerjoin(
            subquery_stmt,
            CompanyMetaData.symbol == subquery_stmt.c.symbol
        ).outerjoin(
            subquery_max_date,
            CompanyMetaData.symbol == subquery_max_date.c.symbol
        ).filter(
            (subquery_stmt.c.symbol == None) |
            (subquery_max_date.c.last_retrieval_date == None) |
            (subquery_max_date.c.last_retrieval_date <= func.date('now', f'-{days_threshold} days'))
        ).limit(limit)

        # Execute the query and retrieve results
        results = query.all()

        # Extract symbols from the results
        symbols = [result[0] for result in results]

    return symbols
