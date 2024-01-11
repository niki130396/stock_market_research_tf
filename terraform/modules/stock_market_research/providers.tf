terraform {
  required_providers {
    google = {
      version = "= 5.6.0"
      source = "hashicorp/google"
    }
  }
  required_version = ">= 1.3.7"

  backend "gcs" {
    bucket = "stock-market-research-tf-state-stock-market-research"
    prefix = "terraform/europe-north1/stock_market_research/terraform.tfstate"
  }
}

provider "google" {
  project = var.gcp_project_full
  region = var.gcp_region
}
