
resource "google_bigquery_dataset" "stock_market_research_dataset" {
  dataset_id                 = "stock_market_research"
  friendly_name              = "Stock market research"
  description                = "A dataset which will hold all the stock market research tables"
  location                   = "EU"
  delete_contents_on_destroy = true

  access {
    role          = "WRITER"
    user_by_email = google_service_account.stock_market_research_user.email
  }
}
