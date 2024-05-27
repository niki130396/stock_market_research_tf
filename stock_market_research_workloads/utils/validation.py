from typing import List

from jsonschema import (
    validate,
    ValidationError,
)

from stock_market_research_workloads.models.fundamentals import (
    CompanyMetaData,
)

COMPANY_METADATA_RESPONSE_SCHEMA_VALIDATOR = {
    "type": "object",
    "properties": {
        "symbol": {
            "type": "string",
            "database_table_related_field": CompanyMetaData.symbol
        },
        "volAvg": {
            "type": "number",
            "database_table_related_field": CompanyMetaData.volume
        },
        "mktCap": {
            "type": ["number", "null"],
            "database_table_related_field": CompanyMetaData.market_cap
        },
        "companyName": {
            "type": "string",
            "database_table_related_field": CompanyMetaData.name
        },
        "currency": {
            "type": ["string", "null"],
            "database_table_related_field": CompanyMetaData.currency
        },
        "industry": {
            "type": "string",
            "database_table_related_field": CompanyMetaData.industry
        },
        "description": {
            "type": ["string", "null"],
            "database_table_related_field": CompanyMetaData.description
        },
        "sector": {
            "type": "string",
            "database_table_related_field": CompanyMetaData.sector
        },
        "country": {
            "type": ["string", "null"],
            "database_table_related_field": CompanyMetaData.country
        },
        "fullTimeEmployees": {
            "type": ["string", "null"],
            "database_table_related_field": CompanyMetaData.full_time_employees_count
        },
        "ipoDate": {
            "type": ["string", "null"],
            "database_table_related_field": CompanyMetaData.ipo_date
        },
    },
    "required": ["symbol", "companyName", "industry", "sector", "country"]
}


def validate_json_objects(objects: List[dict], validation_schema):
    output = []

    for obj in objects:
        try:
            validate(obj, validation_schema)
            output.append(obj)
        except ValidationError as exception:
            print(exception)
            continue
    return output
