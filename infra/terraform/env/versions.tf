terraform {
  required_version = ">= 1.9"
  required_providers {
    azurerm = { source = "hashicorp/azurerm", version = "~> 5.11" }
    random  = { source = "hashicorp/random", version = "~> 3.9" }
  }
  # stan w Azure Storage (z bootstrap/); parametry przez -backend-config, logowanie przez Entra ID (OIDC w CI)
  backend "azurerm" {
    key              = "raglab-env.tfstate"
    use_azuread_auth = true
  }
}

provider "azurerm" {
  features {
    key_vault {
      purge_soft_delete_on_destroy = true # środowisko jest stawiane i usuwane wielokrotnie
    }
    resource_group {
      prevent_deletion_if_contains_resources = false # destroy usuwa też to, co AKS założył sam
    }
  }
  subscription_id = var.subscription_id
}
