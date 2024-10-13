module "gh_oidc" {
  source      = "terraform-google-modules/github-actions-runners/google//modules/gh-oidc"
  project_id  = var.gcp_project_full
  pool_id     = "gh-terraform-pool"
  provider_id = "gh-terraform-provider"
  sa_mapping = {
    "terraform-service-account" = {
      sa_name   = google_service_account.secondary_terraform.id
      attribute = "attribute.repository/niki130396/stock_market_research_tf"
    }
  }
}

output "workload_identity_provider" {
  value = module.gh_oidc.provider_name
}

output "workload_identity_pool" {
  value = module.gh_oidc.pool_name
}
