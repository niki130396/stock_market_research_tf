import pytest

from stock_market_research_workloads.utils.requests import financial_modeling_prep_async_request


@pytest.mark.asyncio
async def test_get_company_information_valid(patch_client_response_get_company_information):

    results, attempted = await financial_modeling_prep_async_request("some_endpoint.com", ["AAPL"])
    assert results and attempted


@pytest.mark.asyncio
async def test_get_company_information_free_plan_limited_stocks(patch_client_response_get_company_information_free_plan):

    results, attempted = await financial_modeling_prep_async_request("some_endpoint.com", ["AAPL"])
    assert not results and attempted
    assert "AAPL" in attempted


@pytest.mark.asyncio
async def test_get_company_information_limit_reach(patch_client_response_get_company_information_limit_reach):

    results, attempted = await financial_modeling_prep_async_request("some_endpoint.com", ["AAPL"])
    assert not results and not attempted
