variable "subscription_id" {
  type        = string
  description = "Subskrypcja Azure (az account show --query id -o tsv)."
}

variable "location" {
  type    = string
  default = "swedencentral"
  # Poland Central: na subskrypcji trial zablokowane wszystkie małe rozmiary VM (NotAvailableForSubscription,
  # sprawdzone 2026-10-27 przez Microsoft.Compute/skus); Sweden Central ma je dostępne
}

variable "github_repo" {
  type        = string
  default     = "Magiszonekk/rag-lab"
  description = "owner/repo, którego workflow dostaje dostęp przez OIDC."
}

variable "github_environment" {
  type        = string
  default     = "azure"
  description = "Environment GitHuba z wymaganym zatwierdzeniem — tylko z niego apply/destroy."
}

variable "budget_usd" {
  type    = number
  default = 150
}

variable "alert_email" {
  type        = string
  description = "Adres alertów budżetu (podawany przy apply, nie w repo)."
}

variable "github_oidc_sub_prefix" {
  type        = string
  default     = "repo:Magiszonekk@97131056/rag-lab@1431095257"
  description = "Prefiks claimu sub z GitHuba (niezmienny subject z ID właściciela i repo); pusty = repo:<github_repo>."
}
