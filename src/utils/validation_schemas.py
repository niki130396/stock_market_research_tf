from src.models.fundamentals import (
    CompanyMetaData,
)

COMPANY_METADATA_RESPONSE_SCHEMA_VALIDATOR = {
    "type": "object",
    "properties": {
        "symbol": {"type": "string", "database_table_related_field": CompanyMetaData.symbol},
        "volAvg": {"type": "number", "database_table_related_field": CompanyMetaData.volume},
        "mktCap": {"type": "number", "database_table_related_field": CompanyMetaData.market_cap},
        "companyName": {"type": "string", "database_table_related_field": CompanyMetaData.name},
        "currency": {"type": "string", "database_table_related_field": CompanyMetaData.currency},
        "industry": {"type": "string", "database_table_related_field": CompanyMetaData.industry},
        "description": {"type": "string", "database_table_related_field": CompanyMetaData.description},
        "sector": {"type": "string", "database_table_related_field": CompanyMetaData.sector},
        "country": {"type": "string", "database_table_related_field": CompanyMetaData.country},
        "fullTimeEmployees": {"type": "string", "database_table_related_field": CompanyMetaData.full_time_employees_count},
        "ipoDate": {"type": "string", "database_table_related_field": CompanyMetaData.ipo_date},
    },
    "required": ["symbol", "companyName", "industry", "sector", "country"]
}
