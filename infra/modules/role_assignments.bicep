param aiFoundryName string
param aiProjectName string
param cosmosDbName string
param storageName string
param searchName string

// Built-in Azure role IDs
var cosmosDbDataContributorRoleId = '00000000-0000-0000-0000-000000000002' // Cosmos DB Built-in Data Contributor
var storageBlobDataContributorRoleId = 'ba92f5b4-2d11-453d-a403-e96b0029c9fe' // Storage Blob Data Contributor
var searchIndexDataContributorRoleId = '8ebe5a00-799e-43f5-93ac-243d3dce84a7' // Search Index Data Contributor
var searchServiceContributorRoleId = '7ca78c08-252a-4471-8644-bb5ff32d4ba0' // Search Service Contributor

resource aiFoundry 'Microsoft.CognitiveServices/accounts@2025-06-01' existing = {
  name: aiFoundryName
}

resource aiProject 'Microsoft.CognitiveServices/accounts/projects@2025-06-01' existing = {
  name: aiProjectName
  parent: aiFoundry
}

resource cosmosDb 'Microsoft.DocumentDB/databaseAccounts@2024-05-15' existing = {
  name: cosmosDbName
}

resource storage 'Microsoft.Storage/storageAccounts@2023-01-01' existing = {
  name: storageName
}

resource search 'Microsoft.Search/searchServices@2024-06-01-preview' existing = {
  name: searchName
}

// AI Foundry to Cosmos DB
resource cosmosRoleAssignmentFoundry 'Microsoft.DocumentDB/databaseAccounts/sqlRoleAssignments@2024-05-15' = {
  name: guid(aiFoundry.id, cosmosDb.id, cosmosDbDataContributorRoleId)
  parent: cosmosDb
  properties: {
    principalId: aiFoundry.identity.principalId
    roleDefinitionId: '/${subscription().id}/resourceGroups/${resourceGroup().name}/providers/Microsoft.DocumentDB/databaseAccounts/${cosmosDb.name}/sqlRoleDefinitions/${cosmosDbDataContributorRoleId}'
    scope: cosmosDb.id
  }
}

// AI Project to Cosmos DB
resource cosmosRoleAssignmentProject 'Microsoft.DocumentDB/databaseAccounts/sqlRoleAssignments@2024-05-15' = {
  name: guid(aiProject.id, cosmosDb.id, cosmosDbDataContributorRoleId)
  parent: cosmosDb
  properties: {
    principalId: aiProject.identity.principalId
    roleDefinitionId: '/${subscription().id}/resourceGroups/${resourceGroup().name}/providers/Microsoft.DocumentDB/databaseAccounts/${cosmosDb.name}/sqlRoleDefinitions/${cosmosDbDataContributorRoleId}'
    scope: cosmosDb.id
  }
}

// AI Foundry to Storage
resource storageRoleAssignmentFoundry 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(aiFoundry.id, storage.id, storageBlobDataContributorRoleId)
  scope: storage
  properties: {
    principalId: aiFoundry.identity.principalId
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', storageBlobDataContributorRoleId)
    principalType: 'ServicePrincipal'
  }
}

// AI Project to Storage
resource storageRoleAssignmentProject 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(aiProject.id, storage.id, storageBlobDataContributorRoleId)
  scope: storage
  properties: {
    principalId: aiProject.identity.principalId
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', storageBlobDataContributorRoleId)
    principalType: 'ServicePrincipal'
  }
}

// AI Foundry to Search - Index Data Contributor
resource searchIndexRoleAssignmentFoundry 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(aiFoundry.id, search.id, searchIndexDataContributorRoleId)
  scope: search
  properties: {
    principalId: aiFoundry.identity.principalId
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', searchIndexDataContributorRoleId)
    principalType: 'ServicePrincipal'
  }
}

// AI Project to Search - Index Data Contributor
resource searchIndexRoleAssignmentProject 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(aiProject.id, search.id, searchIndexDataContributorRoleId)
  scope: search
  properties: {
    principalId: aiProject.identity.principalId
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', searchIndexDataContributorRoleId)
    principalType: 'ServicePrincipal'
  }
}

// AI Foundry to Search - Service Contributor
resource searchServiceRoleAssignmentFoundry 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(aiFoundry.id, search.id, searchServiceContributorRoleId)
  scope: search
  properties: {
    principalId: aiFoundry.identity.principalId
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', searchServiceContributorRoleId)
    principalType: 'ServicePrincipal'
  }
}

// AI Project to Search - Service Contributor
resource searchServiceRoleAssignmentProject 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(aiProject.id, search.id, searchServiceContributorRoleId)
  scope: search
  properties: {
    principalId: aiProject.identity.principalId
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', searchServiceContributorRoleId)
    principalType: 'ServicePrincipal'
  }
}

output cosmosDbRoleAssigned bool = true
output storageRoleAssigned bool = true
output searchRoleAssigned bool = true
