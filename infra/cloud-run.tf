locals {
  default_compute_sa = "${var.project_number}-compute@developer.gserviceaccount.com"
}

resource "google_cloud_run_v2_job" "hevy_export" {
  name     = "hevy-export"
  location = var.region
  client   = "cloud-console"

  template {
    task_count = 1

    template {
      timeout     = "600s"
      max_retries = 1

      execution_environment = "EXECUTION_ENVIRONMENT_GEN2"
      service_account       = local.default_compute_sa

      containers {
        name    = "rp-to-hevy-cli-1"
        image   = var.hevy_export_image
        command = ["sh"]
        args    = ["-c", "python -m rp_to_hevy_cli hevy export --type all -o gs://${google_storage_bucket.data.name}/exports/hevy/$(date +%Y%m%d-%H%M%S)/"]


        resources {
          limits = {
            cpu    = "1000m"
            memory = "512Mi"
          }
        }

        env {
          name  = "HEVY_API_BASE_URL"
          value = "https://api.hevyapp.com"
        }

        env {
          name = "HEVY_API_KEY"
          value_source {
            secret_key_ref {
              secret  = google_secret_manager_secret.hevy_api_key.secret_id
              version = "latest"
            }
          }
        }
      }
    }
  }

  depends_on = [google_project_service.apis["run.googleapis.com"]]
}

resource "google_cloud_run_v2_job" "port_rp_workout_to_hevy" {
  name                = "port-rp-workout-to-hevy"
  location            = var.region
  client              = "cloud-console"
  deletion_protection = false

  template {
    task_count = 1

    template {
      timeout     = "600s"
      max_retries = 1

      execution_environment = "EXECUTION_ENVIRONMENT_GEN2"
      service_account       = local.default_compute_sa

      containers {
        name    = "rp-to-hevy-cli-1"
        image   = var.hevy_export_image
        command = ["sh"]
        args = [
          "-c",
          "python -m rp_to_hevy_cli port-rp-workout-to-hevy --matches /app/data/embeddings/llm-matches.yaml --cache-url '${var.turso_cache_url}' --start-date 2026-03-06 --yes"
        ]

        resources {
          limits = {
            cpu    = "1000m"
            memory = "512Mi"
          }
        }

        env {
          name  = "HEVY_API_BASE_URL"
          value = "https://api.hevyapp.com"
        }

        env {
          name  = "RP_APP_BASE_URL"
          value = "https://training.rpstrength.com/api"
        }

        env {
          name  = "TITLE_API_BASE_URL"
          value = "https://openrouter.ai/api/v1"
        }

        env {
          name  = "TITLE_API_MODEL"
          value = "google/gemini-3-flash-preview"
        }

        env {
          name = "HEVY_API_KEY"
          value_source {
            secret_key_ref {
              secret  = google_secret_manager_secret.hevy_api_key.secret_id
              version = "latest"
            }
          }
        }

        env {
          name = "RP_BEARER_TOKEN"
          value_source {
            secret_key_ref {
              secret  = google_secret_manager_secret.rp_bearer_token.secret_id
              version = "latest"
            }
          }
        }

        env {
          name = "OPENROUTER_API_KEY"
          value_source {
            secret_key_ref {
              secret  = google_secret_manager_secret.openrouter_api_key.secret_id
              version = "latest"
            }
          }
        }

        env {
          name = "TITLE_API_KEY"
          value_source {
            secret_key_ref {
              secret  = google_secret_manager_secret.openrouter_api_key.secret_id
              version = "latest"
            }
          }
        }

        env {
          name = "TURSO_AUTH_TOKEN"
          value_source {
            secret_key_ref {
              secret  = google_secret_manager_secret.turso_auth_token.secret_id
              version = "latest"
            }
          }
        }
      }
    }
  }

  depends_on = [google_project_service.apis["run.googleapis.com"]]
}

resource "google_cloud_scheduler_job" "hevy_export_cron" {
  name     = "hevy-export-cron"
  region   = var.region
  schedule = "0 0 * * *"

  time_zone        = "Europe/Paris"
  attempt_deadline = "180s"

  retry_config {
    min_backoff_duration = "5s"
    max_backoff_duration = "3600s"
    max_doublings        = 5
    max_retry_duration   = "0s"
  }

  http_target {
    http_method = "POST"
    uri         = "https://${var.region}-run.googleapis.com/apis/run.googleapis.com/v1/namespaces/${var.project_id}/jobs/${google_cloud_run_v2_job.hevy_export.name}:run"

    oauth_token {
      service_account_email = local.default_compute_sa
      scope                 = "https://www.googleapis.com/auth/cloud-platform"
    }
  }

  depends_on = [google_project_service.apis["cloudscheduler.googleapis.com"]]
}
