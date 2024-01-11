
resource "google_bigquery_table" "company_meta_data" {
  dataset_id          = google_bigquery_dataset.stock_market_research_dataset.dataset_id
  table_id            = "company_meta_data"
  friendly_name       = "Company Meta Data"
  description         = "Holds data that describes a company - ticker symbol, market cap, country origin, sector, industry"
  deletion_protection = false

  schema = <<EOF
[
  {
    "name": "symbol",
    "type": "STRING",
    "mode": "REQUIRED",
    "description": "Also known as ticker - e.g. AAPL for Apple"
  },
  {
    "name": "name",
    "type": "STRING",
    "mode": "NULLABLE",
    "description": "Company name"
  },
  {
    "name": "market_cap",
    "type": "INTEGER",
    "mode": "NULLABLE",
    "description": "The perceived value of the business by the market"
  },
  {
    "name": "country",
    "type": "STRING",
    "mode": "NULLABLE",
    "description": "Country of origin"
  },
  {
    "name": "ipo_year",
    "type": "STRING",
    "mode": "NULLABLE",
    "description": "Year when the company stock became publicly offered"
  },
  {
    "name": "volume",
    "type": "STRING",
    "mode": "NULLABLE",
    "description": "Stock trading volumes for a given point in time"
  },
  {
    "name": "sector",
    "type": "STRING",
    "mode": "NULLABLE",
    "description": "Market sector in which the company operates"
  },
  {
    "name": "industry",
    "type": "STRING",
    "mode": "NULLABLE",
    "description": "Market industry in which the company operates"
  }
]
EOF
}


resource "google_bigquery_table" "financial_statement_fact" {
  dataset_id          = google_bigquery_dataset.stock_market_research_dataset.dataset_id
  table_id            = "financial_statement_fact"
  friendly_name       = "Financial statement fact"
  description         = "Each row in this table represents a single fact from a given financial statement for a given period"
  deletion_protection = false

  schema = <<EOF
[
  {
    "name": "fact_id",
    "type": "INTEGER",
    "mode": "REQUIRED",
    "description": "Primary key of the table"
  },
  {
    "name": "company",
    "type": "STRING",
    "mode": "REQUIRED",
    "description": "Foreign key which is in the form of a ticker"
  },
  {
    "name": "financial_statement_line",
    "type": "INTEGER",
    "mode": "REQUIRED",
    "description": "Foreign key - represents a category of a financial statement"
  },
  {
    "name": "fiscal_period",
    "type": "DATE",
    "mode": "NULLABLE",
    "description": "Which month and year the fact is from"
  },
  {
    "name": "currency",
    "type": "STRING",
    "mode": "NULLABLE",
    "description": "Currency the value is denominated in"
  },
  {
    "name": "value",
    "type": "INTEGER",
    "mode": "REQUIRED",
    "description": "The actual value of the fact being observed"
  }
]
EOF
}


resource "google_bigquery_table" "financial_statement_category" {
  dataset_id          = google_bigquery_dataset.stock_market_research_dataset.dataset_id
  table_id            = "financial_statement_category"
  friendly_name       = "Financial statement category"
  description         = "Each row in this table represents a category of a financial statement - Revenue, Cost of goods sold etc..."
  deletion_protection = false

  schema = <<EOF
[
  {
    "name": "category_id",
    "type": "INTEGER",
    "mode": "REQUIRED",
    "description": "Primary key of the table"
  },
  {
    "name": "name",
    "type": "STRING",
    "mode": "REQUIRED",
    "description": "The name of the category - Revenue, Cost of goods sold etc..."
  },
  {
    "name": "description",
    "type": "STRING",
    "mode": "NULLABLE",
    "description": "A description of the category"
  },
  {
    "name": "statement_type",
    "type": "INTEGER",
    "mode": "REQUIRED",
    "description": "Foreign key - the statement type this category belongs to - Balance sheet, Income statement, Cash flow statement"
  }
]
EOF
}


resource "google_bigquery_table" "financial_statement_type" {
  dataset_id          = google_bigquery_dataset.stock_market_research_dataset.dataset_id
  table_id            = "financial_statement_type"
  friendly_name       = "Financial statement type"
  description         = "Each row in this table represents a statement type - Balance sheet, Income statement, Cash flow statement"
  deletion_protection = false

  schema = <<EOF
[
  {
    "name": "statement_type_id",
    "type": "INTEGER",
    "mode": "REQUIRED",
    "description": "Primary key of the table"
  },
  {
    "name": "statement_type_name",
    "type": "STRING",
    "mode": "REQUIRED",
    "description": "The name of the statement type"
  }
]
EOF
}
