# Microsoft Azure AI Foundry Agent Service - Sample Repository

## Purpose

This repository serves as a comprehensive sample demonstrating the capabilities of **Microsoft Azure AI Foundry** for building intelligent agent applications. It showcases how to leverage Azure AI Foundry's Agent Service through different implementation approaches, providing developers with practical examples and best practices for agent-based application development.

## Overview

This project demonstrates two primary approaches to building AI agents with Microsoft Azure AI Foundry:

1. **Agent Framework Application** - Using the Microsoft Agent Framework with Azure AI Foundry Agent Service (non-self-hosted)
2. **LangChain Agent Application** - Using LangChain framework with Azure AI Foundry Agent Service (self-hosted agent model)

Both implementations highlight different architectural patterns and deployment models while leveraging the power of Azure AI Foundry's infrastructure and services.

## Project Goals

- **Demonstrate Azure AI Foundry capabilities** for agent development
- **Provide reference implementations** using popular agent frameworks
- **Showcase best practices** for agent orchestration and tool integration
- **Illustrate deployment patterns** for both managed and self-hosted agent models
- **Enable rapid prototyping** of enterprise-grade agent applications

## Baseline Applications

This repository includes the following baseline applications:

### 1. Agent Framework Application (Non-Self-Hosted)

**Technology Stack:**
- Microsoft Agent Framework SDK
- Azure AI Foundry Agent Service (Managed)
- Azure AI Project integration

**Key Features:**
- Utilizes Azure AI Foundry's fully managed Agent Service
- No infrastructure management required
- Built-in scalability and reliability
- Native Azure integration for authentication and monitoring
- Direct connection to Azure AI Foundry project endpoints

**Use Cases:**
- Enterprise applications requiring managed services
- Scenarios with predictable workloads
- Projects prioritizing operational simplicity
- Applications needing Azure security and compliance features

**Architecture:**
The Agent Framework application connects directly to Azure AI Foundry's managed Agent Service, leveraging cloud-hosted capabilities without requiring self-managed infrastructure. Agents are orchestrated through the Azure AI Foundry platform with built-in monitoring, logging, and security.

### 2. LangChain Agent Application (Self-Hosted Model)

**Technology Stack:**
- LangChain/LangGraph framework
- Azure AI Foundry Agent Service (Self-Hosted)
- Custom agent orchestration

**Key Features:**
- Self-hosted agent model deployment
- Full control over agent behavior and customization
- Integration with LangChain's extensive ecosystem
- Flexible tool integration and chain composition
- Hosted on Azure AI Foundry infrastructure with custom runtime

**Use Cases:**
- Applications requiring deep customization
- Complex multi-agent workflows
- Integration with existing LangChain applications
- Scenarios needing fine-grained control over model execution

**Architecture:**
The LangChain application deploys agent models to Azure AI Foundry's infrastructure in a self-hosted configuration, providing greater flexibility in agent design while still benefiting from Azure's scalability, security, and management capabilities.

## Azure AI Foundry Integration

Both applications leverage Azure AI Foundry services including:

- **Azure AI Project** - Centralized project management and resource organization
- **Agent Service** - Managed and self-hosted agent execution environments
- **Model Deployments** - Access to GPT-4 and other advanced language models
- **Connection Management** - Secure credential and endpoint management
- **Monitoring & Logging** - Application Insights and Log Analytics integration
- **Security** - Azure RBAC, managed identities, and network security

## Project Structure

```
agents/
├── src/
│   ├── agents/
│   │   ├── agent_framework_app/     # Agent Framework implementation
│   │   └── langchain_app/           # LangChain implementation
│   ├── config/                      # Shared configuration
│   └── tools/                       # Custom tools and utilities
├── infra/                           # Azure infrastructure as code (Bicep)
│   ├── main.bicep
│   └── modules/                     # Modular infrastructure components
├── azure.yaml                       # Azure Developer CLI configuration
├── requirements.txt                 # Python dependencies
└── README.md                        # Quick start guide
```

## Key Features

### Multi-Framework Support
Demonstrates how different agent frameworks can leverage Azure AI Foundry's capabilities, allowing developers to choose the best framework for their needs.

### Infrastructure as Code
Complete Bicep templates for provisioning Azure AI Foundry resources, ensuring reproducible and maintainable deployments.

### Tool Integration
Examples of custom tool development and integration with agents, showcasing how to extend agent capabilities with domain-specific functionality.

### Agent Orchestration
Patterns for multi-agent systems, including delegation, coordination, and specialized agent roles (e.g., HR Specialist, Technical Support).

### Azure Developer CLI Integration
Streamlined deployment and management using `azd` commands for a consistent developer experience.

## Target Audience

This sample repository is designed for:

- **Developers** exploring AI agent development with Azure
- **Solution Architects** evaluating Azure AI Foundry for agent applications
- **DevOps Engineers** learning to deploy and manage agent workloads
- **Data Scientists** building AI-powered automation solutions
- **Enterprise Teams** seeking reference implementations for production systems

## Getting Started

Refer to [README.md](./README.md) for detailed setup instructions, prerequisites, and quickstart guides.

## Technology Comparison

| Aspect | Agent Framework (Non-Self-Hosted) | LangChain (Self-Hosted) |
|--------|-----------------------------------|-------------------------|
| **Management** | Fully managed by Azure | Self-managed runtime |
| **Customization** | Standard Azure configurations | Full customization |
| **Deployment** | Automatic scaling | Manual scaling configuration |
| **Framework** | Microsoft Agent Framework | LangChain/LangGraph |
| **Best For** | Enterprise managed solutions | Custom, flexible implementations |
| **Operational Overhead** | Minimal | Moderate |

## Learning Outcomes

By exploring this repository, you will learn:

- How to set up and configure Azure AI Foundry projects
- Differences between managed and self-hosted agent models
- Best practices for agent orchestration and tool integration
- Infrastructure provisioning for AI agent applications
- Authentication and security patterns for Azure AI services
- Monitoring and debugging agent applications
- Deployment strategies using Azure Developer CLI

## Resources

- [Azure AI Foundry Documentation](https://learn.microsoft.com/azure/ai-studio/)
- [Microsoft Agent Framework](https://learn.microsoft.com/azure/ai-studio/agents/)
- [LangChain Documentation](https://python.langchain.com/)
- [Azure Developer CLI](https://learn.microsoft.com/azure/developer/azure-developer-cli/)

## License

This sample repository is provided for educational and demonstration purposes. Please refer to the LICENSE file for specific terms and conditions.

---

**Note**: This is a sample repository intended for learning and demonstration. For production deployments, ensure proper security reviews, compliance checks, and adherence to your organization's policies.
