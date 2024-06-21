from sqlalchemy import (
    BigInteger,
    String,
    Text,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    mapped_column,
)


class Base(DeclarativeBase):
    pass


class CompanyMetaData(Base):
    __tablename__ = "company_meta_data"

    symbol = mapped_column(String(6), primary_key=True)
    name = mapped_column(String(128))
    description = mapped_column(Text, nullable=True)
    market_cap = mapped_column(BigInteger, nullable=True)
    currency = mapped_column(String(128), nullable=True)
    country = mapped_column(String(128), nullable=True)
    ipo_date = mapped_column(String(10), nullable=True)
    volume = mapped_column(String(128), nullable=True)
    sector = mapped_column(String(128), nullable=True)
    industry = mapped_column(String(128), nullable=True)
    full_time_employees_count = mapped_column(String(128), nullable=True)
