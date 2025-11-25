param location string
param name string
param project_name string
param applicationInsightsName string

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


resource appInsights 'Microsoft.Insights/components@2020-02-02' existing = {
  name: applicationInsightsName
}

resource accounts_test2155_name_firstProject_appInsights_connection_3703 'Microsoft.CognitiveServices/accounts/projects/connections@2025-06-01' = {
  parent: aiProject
  name: 'appInsights-connection-3703'
  properties: {
    authType: 'ApiKey'
    credentials: {
      key: appInsights.properties.InstrumentationKey
    }
    category: 'AppInsights'
    target: appInsights.id
    useWorkspaceManagedIdentity: false
    isSharedToAll: false
    sharedUserList: []
    peRequirement: 'NotRequired'
    peStatus: 'NotApplicable'
    metadata: {
      ApiType: 'Azure'
      ResourceId: appInsights.id
    }
  }
}

output name string = aiFoundry.name
output projectEndpoint string = aiProject.properties.endpoints['AI Foundry API']
output apiKey string = aiFoundry.listKeys().key1 //Not secure. Only used for demo purposes.