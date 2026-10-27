output "resource_group" { value = azurerm_resource_group.main.name }
output "aks_name" { value = azurerm_kubernetes_cluster.main.name }
output "acr_login_server" { value = azurerm_container_registry.main.login_server }
output "acr_name" { value = azurerm_container_registry.main.name }
output "key_vault_name" { value = azurerm_key_vault.main.name }
output "workload_client_id" { value = azurerm_user_assigned_identity.workload.client_id }
output "tenant_id" { value = data.azurerm_client_config.current.tenant_id }
output "api_dns_label" { value = local.api_dns_label }
output "api_host" { value = local.api_host }
output "web_host" { value = azurerm_static_web_app.web.default_host_name }
output "web_deploy_token" {
  value     = azurerm_static_web_app.web.api_key
  sensitive = true
}
