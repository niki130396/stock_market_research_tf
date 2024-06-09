
locals {
  stock_market_research_workload_labels = {
    "group" : "stock_market_research_workloads"
  }
  stock_market_research_dashboard_labels = {
    "group": "stock_market_research_dashboard"
  }
}

resource "google_cloud_run_v2_job" "get_company_details" {
  name = "get-company-details"
  location = "europe-north1"

  labels = local.stock_market_research_workload_labels

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


resource "google_cloud_run_v2_service" "stock_market_research_dashboard" {
  name = "stock-market-research-dashboard"
  location = var.gcp_region
  ingress = "INGRESS_TRAFFIC_ALL"

  labels = local.stock_market_research_dashboard_labels

  template {

    volumes {
      name = "cloudsql"
      cloud_sql_instance {
        instances = [google_sql_database_instance.stock_market_research_db.connection_name]
      }
    }

    containers {
      ports {
        container_port = 8050
      }
      image = "europe-north1-docker.pkg.dev/stock-market-research-410417/docker/stock_market_research_dashboard:fundamentals_tables-1.0.61"

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
      volume_mounts {
        name = "cloudsql"
        mount_path = "/cloudsql"
      }

      startup_probe {
        initial_delay_seconds = 0
        timeout_seconds = 1
        period_seconds = 3
        failure_threshold = 1
        tcp_socket {
          port = 8050
        }
      }
      liveness_probe {
        http_get {
          path = "/"
          port = 8050
        }
      }

    }
    service_account = google_service_account.stock_market_research_user.email
  }
}
