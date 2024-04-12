import asyncio

from src.utils.sql_helpers import connect_to_cloud_sql
from src.definitions import (
    FINANCIAL_MODELLING_PREP_API,
    STOCK_MARKET_CLOUD_STORAGE_BUCKET,
    COMPANY_PROFILE_ENDPOINT,
)
from src.utils.google_storage import read_file_from_storage_bucket
from src.utils.requests import get_item_async
from src.utils.validation import (
    COMPANY_METADATA_RESPONSE_SCHEMA_VALIDATOR,
    validate_json_objects,
)


def get_company_details():
    all_symbols = read_file_from_storage_bucket(STOCK_MARKET_CLOUD_STORAGE_BUCKET, "company_symbols.csv")
    not_available_symbols = all_symbols[(all_symbols["is_available"] == False) & (all_symbols["attempted"] == False)]["symbols"].tolist()

    ENDPOINT = FINANCIAL_MODELLING_PREP_API + COMPANY_PROFILE_ENDPOINT

    fetched_items = asyncio.run(get_item_async(ENDPOINT, not_available_symbols))
    validated_items = validate_json_objects(fetched_items, COMPANY_METADATA_RESPONSE_SCHEMA_VALIDATOR)
    return validated_items


if __name__ == "__main__":

    connection = connect_to_cloud_sql().raw_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM information_schema.tables")
    for row in cursor.fetchall():
        print(row)

    get_company_details()
