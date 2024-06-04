resource "google_artifact_registry_repository_iam_member" "docker_writer" {
  for_each = toset([
    "serviceAccount:${google_service_account.stock_market_research_user.email}",
  ])
  project = google_artifact_registry_repository.docker.project
  location = google_artifact_registry_repository.docker.location
  repository = google_artifact_registry_repository.docker.name
  role = "roles/artifactregistry.writer"
  member = each.value

  depends_on = [google_artifact_registry_repository.docker]
}


resource "google_project_iam_member" "cloud_sql_instance_user" {
  for_each = toset([
    "serviceAccount:${google_service_account.stock_market_research_user.email}",
  ])
  member  = each.value
  project = var.gcp_project_full
  role    = "roles/cloudsql.instanceUser"
}

resource "google_project_iam_member" "cloud_sql_client" {
  for_each = toset([
    "serviceAccount:${google_service_account.stock_market_research_user.email}",
  ])
  member  = each.value
  project = var.gcp_project_full
  role    = "roles/cloudsql.client"
}

resource "google_project_iam_member" "cloud_storage_object_user" {
  for_each = toset([
    "serviceAccount:${google_service_account.stock_market_research_user.email}"
  ])
  member   = each.value
  project  = var.gcp_project_full
  role     = "roles/storage.objectUser"
}

resource "google_project_iam_member" "cloud_run_job_invoker" {
  for_each = toset([
    "serviceAccount:${google_service_account.stock_market_research_user.email}"
  ])
  member  = each.value
  project = var.gcp_project_full
  role    = "roles/run.invoker"
}

resource "google_cloud_run_service_iam_binding" "stock_market_research_dashboard" {
  members = [
    "allUsers"
  ]
  role    = "roles/run.invoker"
  service = google_cloud_run_v2_service.stock_market_research_dashboard.name
  location = var.gcp_region
}
