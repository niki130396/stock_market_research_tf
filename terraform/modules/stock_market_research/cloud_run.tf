
locals {
  stock_market_research_labels = {
    "group" : "stock_market_research"
  }
}

resource "google_cloud_run_v2_job" "get_financial_statements" {
  name = "get-financial-statements"
  location = "europe-north1"

  labels = local.stock_market_research_labels

  template {
    template {
      containers {
        image = "europe-north1-docker.pkg.dev/stock-market-research-410417/docker/stock_market_research:latest"
      }
      service_account = google_service_account.stock_market_research_user.email
    }
  }

  depends_on = [google_project_service.enabled_apis, google_artifact_registry_repository_iam_member.docker_writer]
}
