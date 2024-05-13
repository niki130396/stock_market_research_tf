from os import environ
import asyncio

from sqlalchemy.orm import Session

from src.utils.sql_helpers import connect_to_cloud_sql
from src.definitions import (
    FINANCIAL_MODELLING_PREP_API,
    STOCK_MARKET_CLOUD_STORAGE_BUCKET,
    COMPANY_PROFILE_ENDPOINT,
    REQUEST_ATTEMPTS_BEFORE_FAIL,
)
from src.utils.google_storage import read_file_from_storage_bucket, write_dataframe_as_csv_to_storage_bucket
from src.utils.requests import financial_modeling_prep_async_request
from src.utils.validation import (
    COMPANY_METADATA_RESPONSE_SCHEMA_VALIDATOR,
    validate_json_objects,
)
from src.models.fundamentals import CompanyMetaData


if __name__ == "__main__":

    engine = connect_to_cloud_sql()

    all_symbols = read_file_from_storage_bucket(STOCK_MARKET_CLOUD_STORAGE_BUCKET, "company_symbols.csv")
    not_available_symbols = all_symbols[(all_symbols["is_available"] == False) & (all_symbols["attempted"] == False)]["symbol"].tolist()[:REQUEST_ATTEMPTS_BEFORE_FAIL]

    fetched_items, attempted_items = asyncio.run(financial_modeling_prep_async_request(
        COMPANY_PROFILE_ENDPOINT,
        not_available_symbols,
        apikey=environ["FINANCIAL_MODELING_PREP_API_TOKEN"]
    ))
    newly_available_symbols = [item["symbol"] for item in fetched_items]

    validated_items = validate_json_objects(fetched_items, COMPANY_METADATA_RESPONSE_SCHEMA_VALIDATOR)

    all_symbols.loc[all_symbols["symbol"].isin(newly_available_symbols), "is_available"] = True
    all_symbols.loc[all_symbols["symbol"].isin(attempted_items), "attempted"] = True

    write_dataframe_as_csv_to_storage_bucket(STOCK_MARKET_CLOUD_STORAGE_BUCKET, "company_symbols.csv", all_symbols)

    with Session(engine) as session:
        company_profiles = []
        for company_profile_json in validated_items:
            company_profile_obj = CompanyMetaData.map_fields(
                COMPANY_METADATA_RESPONSE_SCHEMA_VALIDATOR, company_profile_json
            )
            company_profiles.append(company_profile_obj)
        session.add_all(company_profiles)
        session.commit()
