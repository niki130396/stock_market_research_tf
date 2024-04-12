import requests

from src.utils.sql_helpers import connect_to_cloud_sql
from src.definitions import (
    FINANCIAL_MODELLING_PREP_API,
    STOCK_MARKET_CLOUD_STORAGE_BUCKET,
)
from src.utils.google_storage import read_file_from_storage_bucket


def get_company_details():
    all_symbols = read_file_from_storage_bucket(STOCK_MARKET_CLOUD_STORAGE_BUCKET, "company_symbols.csv")
    not_available_symbols = all_symbols[(all_symbols["is_available"] == False) & (all_symbols["attempted"] == False)]
    print(len(not_available_symbols))


if __name__ == "__main__":

    connection = connect_to_cloud_sql().raw_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM information_schema.tables")
    for row in cursor.fetchall():
        print(row)

    get_company_details()
