
resource "google_storage_bucket" "some_bucket" {
  location = var.gcp_region
  name     = "some-bucket-for-testing"
  project = var.gcp_project_full
}
