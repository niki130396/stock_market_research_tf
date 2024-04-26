from os import environ
import asyncio

from src.utils.sql_helpers import connect_to_cloud_sql
from src.definitions import (
    FINANCIAL_MODELLING_PREP_API,
    STOCK_MARKET_CLOUD_STORAGE_BUCKET,
    COMPANY_PROFILE_ENDPOINT,
    REQUEST_ATTEMPTS_BEFORE_FAIL,
)
from src.utils.google_storage import read_file_from_storage_bucket, write_dataframe_as_csv_to_storage_bucket
from src.utils.requests import get_company_information
from src.utils.validation import (
    COMPANY_METADATA_RESPONSE_SCHEMA_VALIDATOR,
    validate_json_objects,
)


def get_company_details():
    all_symbols = read_file_from_storage_bucket(STOCK_MARKET_CLOUD_STORAGE_BUCKET, "company_symbols.csv")
    not_available_symbols = all_symbols[(all_symbols["is_available"] == False) & (all_symbols["attempted"] == False)]["symbol"].tolist()[:REQUEST_ATTEMPTS_BEFORE_FAIL]

    ENDPOINT = FINANCIAL_MODELLING_PREP_API + COMPANY_PROFILE_ENDPOINT

    fetched_items, attempted_items = asyncio.run(get_company_information(
        ENDPOINT,
        not_available_symbols,
        apikey=environ["FINANCIAL_MODELING_PREP_API_TOKEN"]
    ))
    newly_available_symbols = [item["symbol"] for item in fetched_items]

    validated_items = validate_json_objects(fetched_items, COMPANY_METADATA_RESPONSE_SCHEMA_VALIDATOR)

    all_symbols.loc[all_symbols["symbols"].isin(newly_available_symbols), "is_available"] = True
    all_symbols.loc[all_symbols["symbols"].isin(attempted_items), "attempted"] = True

    write_dataframe_as_csv_to_storage_bucket(STOCK_MARKET_CLOUD_STORAGE_BUCKET, "company_symbols.csv", all_symbols)
    return validated_items


if __name__ == "__main__":

    connection = connect_to_cloud_sql().raw_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM information_schema.tables")
    for row in cursor.fetchall():
        print(row)

    get_company_details()
