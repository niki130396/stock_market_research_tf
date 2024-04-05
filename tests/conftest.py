import pytest
from sqlalchemy import create_engine

from src.models.fundamentals import Base


@pytest.fixture
def connection_engine():
    return create_engine("sqlite:///:memory:")


@pytest.fixture
def setup_teardown_tables(connection_engine):
    Base.metadata.create_all(connection_engine)

    yield

    Base.metadata.drop_all(connection_engine)
