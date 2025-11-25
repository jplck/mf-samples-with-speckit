param environmentName string
param resourceGroupName string
param aiFoundryName string = '${environmentName}-aif'
param aiProjectName string = '${aiFoundryName}-proj'
param location string
param logAnalyticsName string = '${environmentName}-loganalytics'
param applicationInsightsName string = '${environmentName}-appinsights'

var deployments = {
  gpt41: {
    name: 'gpt-4.1'
    properties: {
      model: {
        format: 'OpenAI'
        name: 'gpt-4.1'
        version: '2025-04-14'
      }
      sku: {
        name: 'GlobalStandard'
        capacity: 20
      }
    }
  }
  gpto3mini: {
    name: 'o3-mini'
    properties: {
      model: {
        format: 'OpenAI'
        name: 'o3-mini'
        version: '2025-01-31'
      }
      sku: {
        name: 'GlobalStandard'
        capacity: 20
      }
    }
  }
}

targetScope = 'subscription'
resource resourceGroup 'Microsoft.Resources/resourceGroups@2021-04-01' = {
  name: !empty(resourceGroupName) ? resourceGroupName : '${environmentName}-rg'
  location: location
}

module foundry './modules/ai_foundry.bicep' = {
  name: 'ai_foundry'
  scope: resourceGroup
  dependsOn: [
    monitoring
  ]
  params: {
    location: location
    name: aiFoundryName
    project_name: aiProjectName
    applicationInsightsName: applicationInsightsName
  }
}

@batchSize(1)
module project_deployments 'modules/ai_project_deployment.bicep' = [for deployment in items(deployments): {
  name: 'project_deployment-${deployment.value.name}'
  params: {
    name: deployment.value.name
    properties: deployment.value.properties
    ai_services_name: foundry.outputs.name
  }
  scope: resourceGroup
}]

module monitoring './modules/monitoring/monitoring.bicep' = {
  name: 'monitoring'
  scope: resourceGroup
  params: {
    location: location
    logAnalyticsName: logAnalyticsName
    applicationInsightsName: applicationInsightsName
  }
}

output PROJECT_ENDPOINT string = foundry.outputs.projectEndpoint
output PROJECT_API_KEY string = foundry.outputs.apiKey
output APPLICATIONINSIGHTS_CONNECTION_STRING string = monitoring.outputs.applicationInsightsConnectionString
