resource "google_artifact_registry_repository" "docker" {
  location      = "europe-north1"
  repository_id = "docker"
  format        = "DOCKER"
}
