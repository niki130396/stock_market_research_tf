import os

from google.cloud.sql.connector import Connector, IPTypes
import pg8000

from sqlalchemy.engine.base import Engine
from sqlalchemy import (
    create_engine,
)


def connect_with_connector() -> Engine:
    """
    Initializes a connection pool for a Cloud SQL instance of Postgres.

    Uses the Cloud SQL Python Connector package.
    """
    # Note: Saving credentials in environment variables is convenient, but not
    # secure - consider a more secure solution such as
    # Cloud Secret Manager (https://cloud.google.com/secret-manager) to help
    # keep secrets safe.

    instance_connection_name = os.environ["STOCK_MARKET_RESEARCH_DB_HOST"]  # e.g. 'project:region:instance'
    db_user = os.environ["STOCK_MARKET_RESEARCH_DB_USERNAME"]  # e.g. 'my-db-user'
    db_pass = os.environ["STOCK_MARKET_RESEARCH_DB_USER_PASSWORD"] # e.g. 'my-db-password'
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


connection = connect_with_connector().raw_connection()
cursor = connection.cursor()


cursor.execute("SELECT * FROM information_schema.tables")
for row in cursor.fetchall():
    print(row)
