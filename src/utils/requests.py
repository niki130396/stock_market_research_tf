from urllib.parse import urlencode
from typing import List

import aiohttp


async def get_item_async(endpoint: str, items: List[str], **kwargs):
    """
    Function for fetching items by doing async http requests.
    The function will append each of the items values to the endpoint parameter as a suffix and will make an
    async request.
    :param endpoint: e.g. https://financialmodelingprep.com/api/v3/profile
    :param items: e.g. ["AAPL", "MSFT", "TSLA", "GOOG"]
    """
    results = []

    async with aiohttp.ClientSession() as session:
        encoded = urlencode(kwargs)
        for item in items:
            url = endpoint + f"/{item}?" + encoded
            async with session.get(url) as response:
                operation = await response.json()
                print(operation)
                results.extend(operation)
    return results
