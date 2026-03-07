locals {
  enabled_apis = toset([
    "artifactregistry.googleapis.com",
    "cloudscheduler.googleapis.com",
    "cloudtrace.googleapis.com",
    "containerregistry.googleapis.com",
    "generativelanguage.googleapis.com",
    "logging.googleapis.com",
    "parametermanager.googleapis.com",
    "pubsub.googleapis.com",
    "run.googleapis.com",
    "secretmanager.googleapis.com",
    "storage-api.googleapis.com",
    "storage-component.googleapis.com",
  ])
}

resource "google_project_service" "apis" {
  for_each = local.enabled_apis

  service            = each.value
  disable_on_destroy = false
}
