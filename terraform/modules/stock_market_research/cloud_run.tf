
locals {
  stock_market_research_labels = {
    "group" : "stock_market_research"
  }
}

resource "google_cloud_run_v2_job" "get_company_details" {
  name = "get-company-details"
  location = "europe-north1"

  labels = local.stock_market_research_labels

  template {
    template {
      containers {
        image   = "europe-north1-docker.pkg.dev/stock-market-research-410417/docker/stock_market_research_workloads:latest"
        command = ["python", "stock_market_research_workloads/get_company_details.py"]

        env {
          name  = "STOCK_MARKET_RESEARCH_DB_USER_PASSWORD"
          value = var.stock_market_research_db_user_password
        }
        env {
          name = "STOCK_MARKET_RESEARCH_DB_USERNAME"
          value = google_sql_user.stock_market_research_db_user.name
        }
        env {
          name = "STOCK_MARKET_RESEARCH_DB_HOST"
          value = google_sql_database_instance.stock_market_research_db.connection_name
        }
        env {
          name = "FINANCIAL_MODELING_PREP_API_TOKEN"
          value = var.financial_modeling_prep_api_token
        }
        volume_mounts {
          name = "cloudsql"
          mount_path = "/cloudsql"
        }
      }

      service_account = google_service_account.stock_market_research_user.email

      volumes {
        name = "cloudsql"
        cloud_sql_instance {
          instances = [google_sql_database_instance.stock_market_research_db.connection_name]
        }
      }
    }
  }

  depends_on = [google_project_service.enabled_apis, google_artifact_registry_repository_iam_member.docker_writer]
}


resource "google_cloud_run_v2_job" "test_request" {
  name = "test-request"
  location = var.gcp_region

  labels = local.stock_market_research_labels

  template {
    template {
      containers {
        image   = "europe-north1-docker.pkg.dev/stock-market-research-410417/docker/stock_market_research:latest"
        command = ["python", "src/test_request.py"]

        env {
          name  = "STOCK_MARKET_RESEARCH_DB_USER_PASSWORD"
          value = var.stock_market_research_db_user_password
        }
        env {
          name = "STOCK_MARKET_RESEARCH_DB_USERNAME"
          value = google_sql_user.stock_market_research_db_user.name
        }
        env {
          name = "STOCK_MARKET_RESEARCH_DB_HOST"
          value = google_sql_database_instance.stock_market_research_db.connection_name
        }
        env {
          name = "FINANCIAL_MODELING_PREP_API_TOKEN"
          value = var.financial_modeling_prep_api_token
        }
      }

      service_account = google_service_account.stock_market_research_user.email
    }
  }
}
