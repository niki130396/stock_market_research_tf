locals {
  enabled_apis = [
    "sqladmin.googleapis.com",
    "artifactregistry.googleapis.com",
    "run.googleapis.com",
    "cloudscheduler.googleapis.com",
    "documentai.googleapis.com",
  ]
}

resource "google_project_service" "enabled_apis" {
  for_each = toset(local.enabled_apis)
  service = each.value
  disable_dependent_services = true
}
