#resource "google_artifact_registry_repository" "docker" {
#  location      = "europe-north1"
#  repository_id = "docker"
#  format        = "DOCKER"
#
#  cleanup_policy_dry_run = false
#  cleanup_policies {
#    id     = "keep-minimum-versions"
#    action = "KEEP"
#    most_recent_versions {
#      keep_count = 5
#    }
#  }
#  depends_on = [google_project_service.enabled_apis]
#}


resource "google_artifact_registry_repository" "docker" {
  location      = var.gcp_region
  repository_id = "docker"
  format        = "DOCKER"

  cleanup_policy_dry_run = false
  cleanup_policies {
    id     = "keep-minimum-versions"
    action = "KEEP"
    most_recent_versions {
      keep_count = 5
    }
  }
  depends_on = [google_project_service.enabled_apis]
}
