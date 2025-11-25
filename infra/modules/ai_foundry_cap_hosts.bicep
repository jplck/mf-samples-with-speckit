param aiFoundryName string
param aiProjectName string
param cosmosDbName string
param searchName string
param storageName string
var threadConnections = [cosmosDbName]
var vectorConnections = [searchName]
var storageConnections = [storageName]

resource aiFoundry 'Microsoft.CognitiveServices/accounts@2025-06-01' existing = {
  name: aiFoundryName
}

resource aiProject 'Microsoft.CognitiveServices/accounts/projects@2025-06-01' existing = {
  name: aiProjectName
  parent: aiFoundry
}

resource projectCapabilityHost 'Microsoft.CognitiveServices/accounts/projects/capabilityHosts@2025-06-01' = {
  name: 'agents-capability-host'
  parent: aiProject
  properties: {
    capabilityHostKind: 'Agents'
    threadStorageConnections: threadConnections
    vectorStoreConnections: vectorConnections
    storageConnections: storageConnections
  }
}

output projectCapHost string = projectCapabilityHost.name
