from os import environ
from typing import List

import aiohttp


async def get_item_async(endpoint: str, items: List[str]):
    """
    Function for fetching items by doing async http requests.
    The function will append each of the items values to the endpoint parameter as a suffix and will make an
    async request.
    :param endpoint: e.g. https://financialmodelingprep.com/api/v3/profile
    :param items: e.g. ["AAPL", "MSFT", "TSLA", "GOOG"]
    """
    results = []

    async with aiohttp.ClientSession() as session:
        headers = {"Authorization": f"Bearer {environ['FINANCIAL_MODELING_PREP_API_TOKEN']}"}
        for item in items:
            url = endpoint + f"/{item}"
            async with session.get(url, headers=headers) as response:
                operation = await response.json()
                print(operation)
                results.extend(operation)
    return results
