param aiFoundryName string
param aiProjectName string
param storageName string
param searchName string
param cosmosDbName string
param applicationInsightsName string

resource aiFoundry 'Microsoft.CognitiveServices/accounts@2025-06-01' existing = {
  name: aiFoundryName
}

resource aiProject 'Microsoft.CognitiveServices/accounts/projects@2025-06-01' existing = {
  name: aiProjectName
  parent: aiFoundry
}

resource storage 'Microsoft.Storage/storageAccounts@2023-01-01' existing = {
  name: storageName
}

resource search 'Microsoft.Search/searchServices@2024-06-01-preview' existing = {
  name: searchName
}

resource cosmosDb 'Microsoft.DocumentDB/databaseAccounts@2024-05-15' existing = {
  name: cosmosDbName
}

resource appInsights 'Microsoft.Insights/components@2020-02-02' existing = {
  name: applicationInsightsName
}

resource cosmosDbConnection 'Microsoft.CognitiveServices/accounts/projects/connections@2025-06-01' = {
  name: cosmosDbName
  parent: aiProject
  properties: {
    category: 'CosmosDB'
    target: cosmosDb.properties.documentEndpoint
    authType: 'AAD'
    metadata: {
      ApiType: 'Azure'
      ResourceId: cosmosDb.id
      location: cosmosDb.location
    }
  }
}

resource appInsightsConnection 'Microsoft.CognitiveServices/accounts/projects/connections@2025-06-01' = {
  name: 'appInsights-connection'
  parent: aiProject
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

resource storageConnection 'Microsoft.CognitiveServices/accounts/projects/connections@2025-06-01' = {
  name: storageName
  parent: aiProject
  properties: {
    category: 'AzureStorageAccount'
    target: storage.properties.primaryEndpoints.blob
    authType: 'AAD'
    metadata: {
      ApiType: 'Azure'
      ResourceId: storage.id
      location: storage.location
    }
  }
}

resource searchConnection 'Microsoft.CognitiveServices/accounts/projects/connections@2025-06-01' = {
  name: searchName
  parent: aiProject
  properties: {
    category: 'CognitiveSearch'
    target: 'https://${search.name}.search.windows.net'
    authType: 'AAD'
    metadata: {
      ApiType: 'Azure'
      ResourceId: search.id
      location: search.location
    }
  }
}

output storageConnectionName string = storageConnection.name
output searchConnectionName string = searchConnection.name
output cosmosDbConnectionName string = cosmosDbConnection.name
output appInsightsConnectionName string = appInsightsConnection.name
