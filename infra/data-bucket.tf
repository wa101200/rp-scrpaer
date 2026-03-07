resource "google_storage_bucket" "data" {
  name     = var.data_bucket_name
  location = upper(var.region)

  storage_class               = "STANDARD"
  public_access_prevention    = "enforced"
  uniform_bucket_level_access = true

  soft_delete_policy {
    retention_duration_seconds = 604800
  }
}
