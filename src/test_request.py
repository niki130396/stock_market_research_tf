import os
import asyncio

from src.utils.requests import financial_modeling_prep_async_request
from src.definitions import (
    FINANCIAL_MODELLING_PREP_API,
    COMPANY_PROFILE_ENDPOINT,
)

if __name__ == "__main__":
    api_token = os.environ["FINANCIAL_MODELING_PREP_API_TOKEN"]
    ENDPOINT = FINANCIAL_MODELLING_PREP_API + COMPANY_PROFILE_ENDPOINT

    fetched_items, attempted_items = asyncio.run(financial_modeling_prep_async_request(
        ENDPOINT,
        ["ACLS", "ACMB"],
        apikey=api_token
    ))
