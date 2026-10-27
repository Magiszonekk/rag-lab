plugin "terraform" {
  enabled = true
  preset  = "recommended"
}

plugin "azurerm" {
  enabled = true
  version = "0.33.0"
  source  = "github.com/terraform-linters/tflint-ruleset-azurerm"
}

# env/ to środowisko na żądanie: deploy → ewaluacja → destroy. Ochrona przed usunięciem dotyczy tylko stanu
# w bootstrap/ (tam reguła działa); w env/ jest celowo wyłączona.
rule "azurerm_resources_missing_prevent_destroy" {
  enabled = false
}
