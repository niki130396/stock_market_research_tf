
variable "gcp_project_full" {
  type = string
  default = "stock-market-research-410417"
}

variable "gcp_region" {
  type = string
  default = "europe-north1"
}

variable "gcs_terraform_bucket" {
  type = string
  default = "stock-market-research-tf-state-stock-market-research"
}
