terraform {
  required_providers {
    google = {
      version = "= 5.6.0"
      source = "hashicorp/google"
    }
  }
  required_version = ">= 1.3.7"
}

provider "google" {
  project = var.gcp_project_full
  region = var.gcp_region
}
