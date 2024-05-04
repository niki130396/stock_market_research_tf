from typing import List

from sqlalchemy import (
    Integer,
    String,
    ForeignKey,
    Text,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    mapped_column,
    relationship,
    Mapped,
)

from src.utils.mixins import MapFieldsFromJsonValidationSchemaMixin


class Base(DeclarativeBase):
    pass


class CompanyMetaData(Base, MapFieldsFromJsonValidationSchemaMixin):
    __tablename__ = "company_meta_data"

    symbol = mapped_column(String(6), primary_key=True)
    name = mapped_column(String(50))
    description = mapped_column(Text)
    market_cap = mapped_column(Integer)
    currency = mapped_column(String(10))
    country = mapped_column(String(50))
    ipo_date = mapped_column(String(10))
    volume = mapped_column(String(30))
    sector = mapped_column(String(30))
    industry = mapped_column(String(30))
    full_time_employees_count = mapped_column(String(50))
    statements_flag = mapped_column(
        Integer,
        default=0,
        description="""A flag set to represent whether we have collected all 3 statements for a given company.
        A value of 7 would indicate that we have all 3 statements from the last run. A value of 3 indicates we only have
        2 statements, and a value of 1 indicates we have one statement only.
        """

    )


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
    value = mapped_column(Integer)
