
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


