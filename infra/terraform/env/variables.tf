variable "subscription_id" {
  type = string
}

variable "location" {
  type    = string
  default = "swedencentral"
  # Poland Central: na subskrypcji trial zablokowane wszystkie małe rozmiary VM (NotAvailableForSubscription,
  # sprawdzone 2026-10-27 przez Microsoft.Compute/skus); Sweden Central ma je dostępne
}

variable "name" {
  type    = string
  default = "raglab"
}

variable "kubernetes_version" {
  type        = string
  default     = null # null = domyślna wersja AKS w regionie
  description = "Wersja Kubernetesa (np. 1.36); null = domyślna."
}

variable "node_vm_size" {
  type        = string
  default     = "Standard_B2as_v2"
  description = "1 węzeł 2 vCPU / 8 GB (API trzyma w RAM torch + model wektorów); najtańszy 8 GB w Sweden Central."
}

variable "node_count" {
  type = number
  # 2 węzły = 4 vCPU (cały limit triala). Na jednym 2 vCPU dodatki AKS rezerwują ~1,7 CPU (ingress nginx 2×500m,
  # coredns, webhook workload identity, CSI…) i pody aplikacji (~0,7 CPU) dostają `Insufficient cpu` — zmierzone 2026-10-27.
  default = 2
}

variable "api_admin_ips" {
  type        = list(string)
  default     = []
  description = "CIDR-y z dostępem do API serwera Kubernetesa (pusto = bez ograniczenia; CI dodaje swój adres)."
}

variable "tags" {
  type    = map(string)
  default = {}
}

variable "web_location" {
  type        = string
  # plan Free jest tylko w westeurope, centralus, eastus2, westus2, eastasia; West Europe odrzuca nowych klientów triala
  # (RequestDisallowedByAzure: region not accepting new customers, 2026-10-27), pozostałe cztery przyjmują.
  # Treść i tak idzie z globalnego CDN SWA — region dotyczy tylko zasobu zarządzającego.
  default     = "centralus"
  description = "Region zasobu Static Web App."
}
