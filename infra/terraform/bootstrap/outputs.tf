# wartości do ustawienia jako zmienne repo/environment w GitHubie (to identyfikatory, nie sekrety)
output "github_variables" {
  value = {
    AZURE_CLIENT_ID         = azurerm_user_assigned_identity.github["deploy"].client_id
    AZURE_PLAN_CLIENT_ID    = azurerm_user_assigned_identity.github["plan"].client_id
    AZURE_TENANT_ID         = data.azurerm_client_config.current.tenant_id
    AZURE_SUBSCRIPTION_ID   = var.subscription_id
    TFSTATE_RESOURCE_GROUP  = azurerm_resource_group.state.name
    TFSTATE_STORAGE_ACCOUNT = azurerm_storage_account.state.name
    TFSTATE_CONTAINER       = azurerm_storage_container.state.name
  }
}
