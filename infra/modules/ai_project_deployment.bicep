param name string
param properties object
param ai_services_name string

var defaults = {
  raiPolicyName: 'Microsoft.Default'
  versionUpgradeOption: 'OnceNewDefaultVersionAvailable'
  type: 'Azure.OpenAI'
  sku: {
    name: 'Standard'
    capacity: 20
  }
}

var properties_with_defaults = union(defaults, properties)

resource aiResource 'Microsoft.CognitiveServices/accounts@2025-06-01' existing = {
  name: ai_services_name
}

resource deployment 'Microsoft.CognitiveServices/accounts/deployments@2025-06-01' = {
  parent: aiResource
  name: name
  sku: properties_with_defaults.sku
  properties: {
    model: properties_with_defaults.model
    versionUpgradeOption: properties_with_defaults.versionUpgradeOption
  }
}