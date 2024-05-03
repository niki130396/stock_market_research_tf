

resource "google_cloud_scheduler_job" "schedule_get_company_details_job" {
  name             = "schedule-get-company-details-job"
  schedule         = "0 8 * * *"
  attempt_deadline = "320s"
  region           = var.gcp_region

  retry_config {
    retry_count = 3
  }

  http_target {
    http_method = "POST"
    uri         = "https://${google_cloud_run_v2_job.get_company_details.location}-run.googleapis.com/apis/run.googleapis.com/v1/namespaces/${var.gcp_project_number}/jobs/${google_cloud_run_v2_job.get_company_details.name}:run"

    oauth_token {
      service_account_email = google_service_account.stock_market_research_user.email
    }
  }

  depends_on = [google_project_service.enabled_apis, google_cloud_run_v2_job.get_company_details]
}
