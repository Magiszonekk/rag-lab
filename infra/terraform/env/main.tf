# Środowisko RAG Lab na Azure (koncept D17, M4): AKS + ACR + Key Vault + tożsamość podów (workload identity).
# Stawiane i usuwane przez workflow `azure` (plan na PR → zatwierdzenie → apply → ewaluacja → destroy).
# Modele NIE są na Azure: pod LiteLLM łączy się z bramką modeli właściciela (decyzja 2026-10-27).

data "azurerm_client_config" "current" {}

resource "random_string" "suffix" {
  length  = 6
  upper   = false
  special = false
}

locals {
  suffix = random_string.suffix.result
  tags   = merge({ project = "rag-lab", managed-by = "terraform", stack = "env" }, var.tags)
}

resource "azurerm_resource_group" "main" {
  name     = "rg-${var.name}"
  location = var.location
  tags     = local.tags
}

# --- rejestr obrazów -------------------------------------------------------------------------------------------
resource "azurerm_container_registry" "main" {
  name                = "${var.name}acr${local.suffix}"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  sku                 = "Basic"
  admin_enabled       = false # pull przez tożsamość kubeleta (AcrPull), push przez OIDC workflow
  tags                = local.tags
}

# --- Kubernetes ------------------------------------------------------------------------------------------------
resource "azurerm_kubernetes_cluster" "main" {
  name                = "aks-${var.name}"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  dns_prefix          = "${var.name}-${local.suffix}"
  kubernetes_version  = var.kubernetes_version
  node_resource_group = "rg-${var.name}-nodes"
  sku_tier            = "Free" # plan sterowania bez opłaty (bez SLA) — środowisko demonstracyjne
  tags                = local.tags

  # dostęp do API klastra tylko przez Entra ID + Azure RBAC; lokalne konto admina wyłączone
  local_account_disabled            = true
  role_based_access_control_enabled = true
  azure_active_directory_role_based_access_control {
    azure_rbac_enabled = true
    tenant_id          = data.azurerm_client_config.current.tenant_id
  }

  # workload identity: pod dostaje token Entra ID bez sekretów (Key Vault przez sterownik CSI)
  oidc_issuer_enabled       = true
  workload_identity_enabled = true
  key_vault_secrets_provider {
    secret_rotation_enabled = true
  }

  # wbudowany kontroler ingress (nginx zarządzany przez AKS) — publiczne API z TLS
  web_app_routing {
    dns_zone_ids = []
  }

  automatic_upgrade_channel    = "patch"
  node_os_upgrade_channel      = "NodeImage"
  image_cleaner_enabled        = true
  image_cleaner_interval_hours = 48

  dynamic "api_server_access_profile" {
    for_each = length(var.api_admin_ips) > 0 ? [1] : []
    content {
      authorized_ip_ranges = var.api_admin_ips
    }
  }

  default_node_pool {
    name                         = "system"
    vm_size                      = var.node_vm_size
    node_count                   = var.node_count
    os_sku                       = "AzureLinux"
    os_disk_size_gb              = 64
    only_critical_addons_enabled = false # system i aplikacja na tych samych węzłach
    temporary_name_for_rotation  = "tmpsystem"
    upgrade_settings {
      # przy 2 węzłach (4 vCPU = limit triala) zapasowy węzeł na czas aktualizacji się nie zmieści — aktualizacja
      # węzłów padnie na limicie; środowisko żyje 1–2 h (deploy → test → destroy), więc to świadomy kompromis
      max_surge = "1"
    }
  }

  # węzły z default_node_pool (bez automatycznego doboru węzłów — Node Auto Provisioning)
  node_provisioning_profile {
    mode               = "Manual"
    default_node_pools = "Auto"
  }

  network_profile {
    network_plugin      = "azure"
    network_plugin_mode = "overlay"
    network_data_plane  = "cilium" # egzekwuje NetworkPolicy z chartu
    network_policy      = "cilium"
    load_balancer_sku   = "standard"
    outbound_type       = "loadBalancer"
  }

  identity {
    type = "SystemAssigned"
  }

  lifecycle {
    ignore_changes = [default_node_pool[0].upgrade_settings, kubernetes_version]
  }
}

resource "azurerm_role_assignment" "kubelet_acr" {
  scope                            = azurerm_container_registry.main.id
  role_definition_name             = "AcrPull"
  principal_id                     = azurerm_kubernetes_cluster.main.kubelet_identity[0].object_id
  skip_service_principal_aad_check = true
}

# kto uruchamia Terraform (workflow przez OIDC albo właściciel), ten administruje klastrem i pushuje obrazy
resource "azurerm_role_assignment" "deployer_aks" {
  scope                = azurerm_kubernetes_cluster.main.id
  role_definition_name = "Azure Kubernetes Service RBAC Cluster Admin"
  principal_id         = data.azurerm_client_config.current.object_id
}

resource "azurerm_role_assignment" "deployer_acr" {
  scope                = azurerm_container_registry.main.id
  role_definition_name = "AcrPush"
  principal_id         = data.azurerm_client_config.current.object_id
}

# --- sekrety -------------------------------------------------------------------------------------------------
resource "azurerm_key_vault" "main" {
  name                       = "kv-${var.name}-${local.suffix}"
  resource_group_name        = azurerm_resource_group.main.name
  location                   = azurerm_resource_group.main.location
  tenant_id                  = data.azurerm_client_config.current.tenant_id
  sku_name                   = "standard"
  rbac_authorization_enabled = true
  soft_delete_retention_days = 7
  purge_protection_enabled   = false # destroy ma usuwać całkowicie (środowisko na żądanie)
  tags                       = local.tags
}

resource "azurerm_role_assignment" "deployer_kv" {
  scope                = azurerm_key_vault.main.id
  role_definition_name = "Key Vault Secrets Officer"
  principal_id         = data.azurerm_client_config.current.object_id
}

# hasła generowane tutaj; klucze modeli (LLM_API_KEY itp.) wpisuje workflow z sekretów environmentu GitHuba
resource "random_password" "postgres" {
  length  = 32
  special = false
}

resource "random_password" "litellm_master" {
  length  = 40
  special = false
}

resource "random_password" "demo_key" {
  length  = 40
  special = false
}

resource "azurerm_key_vault_secret" "generated" {
  for_each = {
    POSTGRES-PASSWORD  = random_password.postgres.result
    LITELLM-MASTER-KEY = "sk-${random_password.litellm_master.result}"
    LLM-DEMO-API-KEY   = "sk-${random_password.demo_key.result}" # klucz wirtualny LiteLLM (zakładany po wdrożeniu)
  }
  name         = each.key
  value        = each.value
  key_vault_id = azurerm_key_vault.main.id
  depends_on   = [azurerm_role_assignment.deployer_kv]
}

# --- tożsamość podów (workload identity → Key Vault) ------------------------------------------------------------
resource "azurerm_user_assigned_identity" "workload" {
  name                = "id-${var.name}-workload"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  tags                = local.tags
}

resource "azurerm_federated_identity_credential" "workload" {
  name                      = "raglab-sa"
  user_assigned_identity_id = azurerm_user_assigned_identity.workload.id
  issuer                    = azurerm_kubernetes_cluster.main.oidc_issuer_url
  audience                  = ["api://AzureADTokenExchange"]
  subject                   = "system:serviceaccount:raglab:raglab"
}

resource "azurerm_role_assignment" "workload_kv" {
  scope                = azurerm_key_vault.main.id
  role_definition_name = "Key Vault Secrets User"
  principal_id         = azurerm_user_assigned_identity.workload.principal_id
  principal_type       = "ServicePrincipal"
}

# --- frontend demo: Azure Static Web Apps (plan Free) -----------------------------------------------------------
# Statyczny build `web/` (Vite) wdrażany przez workflow tokenem wdrożeniowym (`api_key`); VITE_API_URL = https://api_host.
# SWA Free jest tylko w kilku regionach (West Europe najbliżej), niezależnie od regionu klastra.
resource "azurerm_static_web_app" "web" {
  name                = "swa-${var.name}-${local.suffix}"
  resource_group_name = azurerm_resource_group.main.name
  location            = var.web_location
  sku_tier            = "Free"
  sku_size            = "Free"
  tags                = local.tags
}

locals {
  # publiczny adres API: etykieta DNS na IP load balancera kontrolera ingress (ustawia ją workflow w
  # NginxIngressController) → <etykieta>.<region>.cloudapp.azure.com; certyfikat Let's Encrypt przez cert-manager
  api_dns_label = "${var.name}-${local.suffix}"
  api_host      = "${local.api_dns_label}.${var.location}.cloudapp.azure.com"
}
