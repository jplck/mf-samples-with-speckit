param location string
param name string
param project_name string

resource aiFoundry 'Microsoft.CognitiveServices/accounts@2025-04-01-preview' = {
  name: name
  location: location
  identity: {
    type: 'SystemAssigned'
  }
  sku: {
    name: 'S0'
  }
  kind: 'AIServices'
  properties: {
    allowProjectManagement: true 
    customSubDomainName: name
    disableLocalAuth: false //disable if you want to use only managed identities for API access
    publicNetworkAccess: 'Enabled'
  }
}

resource aiProject 'Microsoft.CognitiveServices/accounts/projects@2025-04-01-preview' = {
  name: project_name
  parent: aiFoundry
  location: location
  identity: {
    type: 'SystemAssigned'
  }
  properties: {}
}

output name string = aiFoundry.name
output projectEndpoint string = aiProject.properties.endpoints['AI Foundry API']
output apiKey string = aiFoundry.listKeys().key1 //Not secure. Only used for demo purposes.
