
variable "gcp_project_full" {
  type = string
  default = "stock-market-research-410417"
}

variable "gcp_region" {
  type = string
  default = "europe-north1"
}

variable "stock_market_research_db_user_password" {
  type = string
}

variable "financial_modeling_prep_api_token" {
  type      = string
  sensitive = true
}
