from urllib.parse import urlencode
from typing import List

import aiohttp


async def get_company_information(endpoint: str, symbols: List[str], **kwargs):
    """
    Function for fetching items by doing async http requests.
    The function will append each of the items values to the endpoint parameter as a suffix and will make an
    async request.
    :param endpoint: e.g. https://financialmodelingprep.com/api/v3/profile
    :param symbols: e.g. ["AAPL", "MSFT", "TSLA", "GOOG"]
    """
    results = []
    attempted = []
    async with aiohttp.ClientSession() as session:
        encoded = urlencode(kwargs)
        for symbol in symbols:
            url = endpoint + f"/{symbol}?" + encoded
            async with session.get(url) as response:
                response_json = await response.json()
                if "Error Message" in response_json:
                    if response_json["Error Message"].startswith("Free plan is limited to US stocks only"):
                        attempted.append(symbol)
                    else:
                        # Means we've reached the free limit and we haven't even attempted getting the information
                        break
                else:
                    attempted.append(symbol)
                    results.extend(response_json)
    return results, attempted
