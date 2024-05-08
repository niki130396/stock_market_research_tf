import os
import requests
from urllib.parse import urlencode


if __name__ == "__main__":
    api_token = os.environ["FINANCIAL_MODELING_PREP_API_TOKEN"]

    response = requests.get(f"https://financialmodelingprep.com/api/v3/profile/ACCMF?{urlencode({'apikey': api_token})}")
    print(response.json())
    print(response.text)
