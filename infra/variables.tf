variable "project_id" {
  description = "GCP project ID"
  type        = string
}

variable "project_number" {
  description = "GCP project number"
  type        = string
}

variable "region" {
  description = "GCP region"
  type        = string
  default     = "europe-west1"
}

variable "hevy_export_image" {
  description = "Docker image for hevy-export Cloud Run job"
  type        = string
}

variable "data_bucket_name" {
  description = "GCS bucket name for data storage"
  type        = string
}

variable "turso_cache_url" {
  description = "Turso database cache URL"
  type        = string
  sensitive   = true
}
