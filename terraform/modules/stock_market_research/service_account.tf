
resource "google_service_account" "stock_market_research_user" {
  account_id = "stock-market-research-user"
  display_name = "Stock market research user"
}


resource "google_service_account" "new_user" {
  account_id = "new-user"
  display_name = "Stock market research user"
}
