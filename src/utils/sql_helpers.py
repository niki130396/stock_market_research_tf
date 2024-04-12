import os

from google.cloud.sql.connector import Connector, IPTypes
import pg8000

from sqlalchemy.engine.base import Engine
from sqlalchemy import (
    create_engine,
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
