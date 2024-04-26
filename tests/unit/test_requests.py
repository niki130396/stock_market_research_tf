import pytest

from src.utils.requests import get_company_information


@pytest.mark.asyncio
async def test_get_company_information_valid(patch_client_response_get_company_information):

    results, attempted = await get_company_information("some_endpoint.com", ["AAPL"])
    assert results and attempted


@pytest.mark.asyncio
async def test_get_company_information_free_plan_limited_stocks(patch_client_response_get_company_information_free_plan):

    results, attempted = await get_company_information("some_endpoint.com", ["AAPL"])
    assert not results and attempted
    assert "AAPL" in attempted


@pytest.mark.asyncio
async def test_get_company_information_limit_reach(patch_client_response_get_company_information_limit_reach):

    results, attempted = await get_company_information("some_endpoint.com", ["AAPL"])
    assert not results and not attempted
