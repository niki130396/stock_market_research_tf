
resource "google_service_account" "stock_market_research_user" {
  account_id = "stock-market-research-user"
  display_name = "Stock market research user"
}


resource "google_service_account" "secondary_terraform" {
  account_id = "secondary-terraform"
}
