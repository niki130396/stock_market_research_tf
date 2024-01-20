

#resource "google_sql_database_instance" "stock_market_research_db" {
#  name                = "stock-market-research-db"
#  database_version    = "POSTGRES_15"
#  region              = "europe-west1"
#  deletion_protection = false
#
#  settings {
#    tier = "db-f1-micro"
#
#  ip_configuration {
#      ipv4_enabled = true
#      require_ssl  = false  # Disable SSL for public IP (Note: This is not recommended for production environments)
#    }
#  }
#}
