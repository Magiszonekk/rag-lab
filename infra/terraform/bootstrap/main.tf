# Jednorazowy bootstrap (uruchamia właściciel lokalnie, `az login`): wszystko, czego potrzebuje workflow
# w GitHub Actions, zanim sam będzie mógł działać — konto na stan Terraform, tożsamość z federacją OIDC
# (bez sekretów w repo) i budżet z alertem. Stan bootstrapu jest lokalny (mały, bez sekretów; zasoby
# bootstrapu żyją przez cały okres projektu, `env/` stawia się i usuwa wielokrotnie).

terraform {
  required_version = ">= 1.9"
  required_providers {
    azurerm = { source = "hashicorp/azurerm", version = "~> 5.11" }
    random  = { source = "hashicorp/random", version = "~> 3.9" }
  }
}

provider "azurerm" {
  features {}
  subscription_id = var.subscription_id
}

data "azurerm_client_config" "current" {}

resource "random_string" "suffix" {
  length  = 6
  upper   = false
  special = false
}

locals {
  tags = { project = "rag-lab", managed-by = "terraform", stack = "bootstrap" }
}

resource "azurerm_resource_group" "state" {
  name     = "rg-raglab-tfstate"
  location = var.location
  tags     = local.tags
}

# Stan Terraform środowiska (env/): blob z blokadą (lease), dostęp tylko przez Entra ID (bez kluczy konta)
resource "azurerm_storage_account" "state" {
  name                            = "raglabtf${random_string.suffix.result}"
  resource_group_name             = azurerm_resource_group.state.name
  location                        = azurerm_resource_group.state.location
  account_tier                    = "Standard"
  account_replication_type        = "LRS"
  min_tls_version                 = "TLS1_2"
  allow_nested_items_to_be_public = false
  shared_access_key_enabled       = false
  default_to_oauth_authentication = true
  tags                            = local.tags

  blob_properties {
    versioning_enabled = true # przywrócenie stanu po błędzie
    delete_retention_policy { days = 7 }
  }

  lifecycle {
    prevent_destroy = true # stan wszystkich uruchomień env/ — nie usuwać przypadkiem
  }
}

resource "azurerm_storage_container" "state" {
  name                  = "tfstate"
  storage_account_id    = azurerm_storage_account.state.id
  container_access_type = "private"

  lifecycle {
    prevent_destroy = true
  }
}

# Dwie tożsamości workflow (managed identity + federacja z GitHub OIDC, bez sekretów w repo):
# - plan: tylko odczyt, dla pull requestów (PR uruchamia kod z gałęzi — nie może dostać praw zapisu);
# - deploy: zapis (apply/destroy), tylko z chronionego environment, który wymaga zatwierdzenia właściciela.
resource "azurerm_user_assigned_identity" "github" {
  for_each            = toset(["plan", "deploy"])
  name                = "id-raglab-github-${each.key}"
  resource_group_name = azurerm_resource_group.state.name
  location            = azurerm_resource_group.state.location
  tags                = local.tags
}

# Prefiks claimu `sub` tokenu OIDC z GitHuba. Repozytoria z niezmiennym subjectem (domyślne dla nowych repo) wysyłają
# `repo:<owner>@<owner_id>/<repo>@<repo_id>` zamiast `repo:<owner>/<repo>` — sprawdź:
#   gh api repos/<owner>/<repo>/actions/oidc/customization/sub  → sub_claim_prefix
locals {
  oidc_sub_prefix = var.github_oidc_sub_prefix != "" ? var.github_oidc_sub_prefix : "repo:${var.github_repo}"
}

resource "azurerm_federated_identity_credential" "github" {
  for_each = {
    plan   = "${local.oidc_sub_prefix}:pull_request"
    deploy = "${local.oidc_sub_prefix}:environment:${var.github_environment}"
  }
  name                      = "github-${each.key}"
  user_assigned_identity_id = azurerm_user_assigned_identity.github[each.key].id
  issuer                    = "https://token.actions.githubusercontent.com"
  audience                  = ["api://AzureADTokenExchange"]
  subject                   = each.value
}

# plan: odczyt zasobów, stanu (bez blokady: -lock=false), sekretów generowanych przez Terraform i danych AKS
resource "azurerm_role_assignment" "plan" {
  for_each = {
    "Reader"                                     = "/subscriptions/${var.subscription_id}"
    "Key Vault Secrets User"                     = "/subscriptions/${var.subscription_id}"
    "Azure Kubernetes Service Cluster User Role" = "/subscriptions/${var.subscription_id}"
    "Storage Blob Data Reader"                   = azurerm_storage_account.state.id
  }
  scope                = each.value
  role_definition_name = each.key
  principal_id         = azurerm_user_assigned_identity.github["plan"].principal_id
  principal_type       = "ServicePrincipal"
}

# Contributor wystarczy na zasoby; środowisko nadaje role (AcrPull, Key Vault) własnym tożsamościom, więc
# workflow potrzebuje też "Role Based Access Control Administrator" — ograniczonego warunkiem do tych ról.
resource "azurerm_role_assignment" "github_contributor" {
  scope                = "/subscriptions/${var.subscription_id}"
  role_definition_name = "Contributor"
  principal_id         = azurerm_user_assigned_identity.github["deploy"].principal_id
  principal_type       = "ServicePrincipal"
}

locals {
  # role, które workflow może nadawać (GUID-y wbudowanych ról Azure)
  delegable_roles = [
    "7f951dda-4ed3-4680-a7ca-43fe172d538d", # AcrPull (kubelet → ACR)
    "8311e382-0749-4cb8-b61a-304f252e45ec", # AcrPush (workflow → ACR)
    "4633458b-17de-408a-b874-0445c86b69e6", # Key Vault Secrets User (pod → Key Vault)
    "b86a8fe4-44ce-4948-aee5-eccb2c155cd7", # Key Vault Secrets Officer (workflow → Key Vault)
    "b1ff04bb-8a4e-4dc4-8eb5-8693973ce19b", # Azure Kubernetes Service RBAC Cluster Admin (workflow → AKS)
  ]
  delegable_condition = join(" OR ", [for r in local.delegable_roles : "@Request[Microsoft.Authorization/roleAssignments:RoleDefinitionId] ForAnyOfAnyValues:GuidEquals {${r}}"])
}

resource "azurerm_role_assignment" "github_rbac_admin" {
  scope                = "/subscriptions/${var.subscription_id}"
  role_definition_name = "Role Based Access Control Administrator"
  principal_id         = azurerm_user_assigned_identity.github["deploy"].principal_id
  principal_type       = "ServicePrincipal"
  condition_version    = "2.0"
  condition            = <<-EOT
    (
     (
      !(ActionMatches{'Microsoft.Authorization/roleAssignments/write'})
     )
     OR
     (
      ${local.delegable_condition}
     )
    )
    AND
    (
     (
      !(ActionMatches{'Microsoft.Authorization/roleAssignments/delete'})
     )
     OR
     (
      ${replace(local.delegable_condition, "@Request", "@Resource")}
     )
    )
  EOT
}

resource "azurerm_role_assignment" "github_state" {
  scope                = azurerm_storage_account.state.id
  role_definition_name = "Storage Blob Data Contributor"
  principal_id         = azurerm_user_assigned_identity.github["deploy"].principal_id
  principal_type       = "ServicePrincipal"
}

# właściciel też czyta/zapisuje stan (lokalny `terraform plan` w env/)
resource "azurerm_role_assignment" "owner_state" {
  scope                = azurerm_storage_account.state.id
  role_definition_name = "Storage Blob Data Contributor"
  principal_id         = data.azurerm_client_config.current.object_id
}

# Budżet subskrypcji z alertem mailowym (koncept D17: przed pierwszym apply). Trial i tak ma twardy limit
# wydatków; budżet ostrzega wcześniej — przy 50/80/100% kwoty i przy prognozie przekroczenia.
resource "azurerm_consumption_budget_subscription" "monthly" {
  name            = "raglab-monthly"
  subscription_id = "/subscriptions/${var.subscription_id}"
  amount          = var.budget_usd
  time_grain      = "Monthly"

  time_period {
    start_date = formatdate("YYYY-MM-01'T'00:00:00Z", timestamp())
  }

  dynamic "notification" {
    for_each = { "50" = "Actual", "80" = "Actual", "100" = "Actual", "90" = "Forecasted" }
    content {
      enabled        = true
      threshold      = tonumber(notification.key)
      operator       = "GreaterThanOrEqualTo"
      threshold_type = notification.value
      contact_emails = [var.alert_email]
    }
  }

  lifecycle {
    ignore_changes = [time_period] # start_date liczony raz, przy założeniu
  }
}
