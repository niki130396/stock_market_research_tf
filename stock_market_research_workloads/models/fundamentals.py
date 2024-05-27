from typing import List

from sqlalchemy import (
    Integer,
    BigInteger,
    String,
    ForeignKey,
    Text,
    Date,
    func,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    mapped_column,
    relationship,
    Mapped,
)

from stock_market_research_workloads.utils.mixins import MapFieldsFromJsonValidationSchemaMixin


class Base(DeclarativeBase):
    pass


class CompanyMetaData(Base, MapFieldsFromJsonValidationSchemaMixin):
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


class RetrievedStatementsLog(Base):
    __tablename__ = "retrieved_statements_log"

    id = mapped_column(Integer, primary_key=True)
    symbol: Mapped[str] = mapped_column(ForeignKey("company_meta_data.symbol"))
    statement_type = mapped_column(ForeignKey("statement_type_definition.id"))
    retrieval_date = mapped_column(Date, default=func.current_date())


class StatementTypeDefinition(Base):
    __tablename__ = "statement_type_definition"

    id = mapped_column(Integer, primary_key=True)
    statement_type = mapped_column(String(30))
    financial_statement_attributes: Mapped[List["FinancialStatementAttribute"]] = relationship(back_populates="statement_type")


class FinancialStatementAttribute(Base):
    __tablename__ = "financial_statement_attribute"

    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(256))
    friendly_name = mapped_column(String(256))
    description = mapped_column(String(256), nullable=True)
    statement_type_id: Mapped[int] = mapped_column(ForeignKey("statement_type_definition.id"))
    statement_type: Mapped["StatementTypeDefinition"] = relationship(back_populates="financial_statement_attributes")


class FinancialStatementFact(Base):
    __tablename__ = "financial_statement_fact"

    id = mapped_column(Integer, primary_key=True)
    company_symbol: Mapped[str] = mapped_column(ForeignKey("company_meta_data.symbol"))
    financial_statement_attribute: Mapped[int] = mapped_column(ForeignKey("financial_statement_attribute.id"))
    fiscal_year = mapped_column(String(10))
    fiscal_period = mapped_column(String(20))
    value = mapped_column(BigInteger)
