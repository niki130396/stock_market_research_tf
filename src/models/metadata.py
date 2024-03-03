from sqlalchemy import (
    Integer,
    String,
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
    name = mapped_column(String(50))
    market_cap = mapped_column(Integer)
    country = mapped_column(String(50))
    ipo_year = mapped_column(String(6))
    volume = mapped_column(String(30))
    sector = mapped_column(String(30))
    industry = mapped_column(String(30))
