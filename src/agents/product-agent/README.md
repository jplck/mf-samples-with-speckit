# Writer-Reviewer Hosted Agent Sample

This sample demonstrates the construction of a hosted agent workflow using the Agent Framework. It features two agents—a "Writer" and a "Reviewer"—integrated in a streamlined, one-way workflow to illustrate best practices for agent orchestration and interaction.

## Project Structure

| File               | Description                                                         |
| ------------------ | ------------------------------------------------------------------- |
| `workflow_core.py` | Builds the workflow, creates agents, and manages credentials.       |
| `interactive.py`   | Runs the workflow in local/interactive mode.                        |
| `container.py`     | Starts the workflow in container/server mode.                       |
| `.env`             | Stores environment configuration for Microsoft Foundry integration. |

## Prerequisites

- Python 3.10 or higher.
- A Microsoft Foundry Project and a model deployment.

## Setup and Installation

1. Creating virtual environments

   ```bash
    python -m venv .venv
   ```

2. Activate the virtual environment

   ```bash
   # PowerShell
   ./.venv/Scripts/Activate.ps1

   # Windows cmd
   .venv\Scripts\activate.bat

   # Unix/MacOS
   source .venv/bin/activate
   ```

3. Install dependencies

   ```bash
   pip install azure-ai-agentserver-agentframework
   ```

4. Create or update the `.env` file with your Microsoft Foundry configuration

   ```bash
   # Your Microsoft Foundry project endpoint
   AZURE_AI_PROJECT_ENDPOINT="your-foundry-project-endpoint"

   # Your model deployment name in Microsoft Foundry
   AZURE_AI_MODEL_DEPLOYMENT_NAME="your-model-deployment-name"
   ```

   **Important**: Never commit the `.env` file to version control. Add it to your `.gitignore` file.

## Local Testing

This sample authenticates using [DefaultAzureCredential](https://aka.ms/azsdk/python/identity/credential-chains#usage-guidance-for-defaultazurecredential). Ensure your development environment is configured to provide credentials via one of the supported sources, for example:

- Azure CLI (`az login`)
- Visual Studio Code account sign-in
- Visual Studio account sign-in
- Environment variables for a service principal (AZURE_TENANT_ID, AZURE_CLIENT_ID, AZURE_CLIENT_SECRET)

Confirm authentication locally (for example, az account show or az account get-access-token) before running the sample.

### Interactive Mode

Run the hosted agent directly for development and testing:

```bash
python interactive.py
```

### Container Mode

To run the agent in container mode:

1. Open the Visual Studio Code Command Palette and execute the `Microsoft Foundry: Open Container Agent Playground Locally` command.
2. Execute `container.py` to initialize the containerized hosted agent.
3. Submit a request to the agent through the playground interface. For example, you may enter a prompt such as: "Create a slogan for a new electric SUV that is affordable and fun to drive."
4. Review the agent's response in the playground interface.

> **Note**: Open the local playground before starting the container agent to ensure the visualization functions correctly.

## Deployment

To deploy the hosted agent:

1. Open the Visual Studio Code Command Palette and run the `Microsoft Foundry: Deploy Hosted Agent` command.
2. Configure the deployment settings by selecting your target workspace, specifying the container agent file (`container.py`), and defining any additional deployment parameters as needed.
3. Upon successful deployment, the hosted agent will appear in the `Hosted Agents (Preview)` section of the Microsoft Foundry extension tree view.
4. Select the deployed agent to access detailed information and test functionality using the integrated playground interface.

## MSI Configuration in the Azure Portal

This sample requires the Microsoft Foundry Project to authenticate using a Managed Identity when running remotely in Azure. Grant the project's managed identity the required permissions by assigning the built-in [Azure AI User](https://aka.ms/foundry-ext-project-role) role.

To configure the Managed Identity:

1. In the Azure Portal, open the Foundry Project.
2. Select "Access control (IAM)" from the left-hand menu.
3. Click "Add" and choose "Add role assignment".
4. In the role selection, search for and select "Azure AI User", then click "Next".
5. For "Assign access to", choose "Managed identity".
6. Click "Select members", locate the managed identity associated with your Foundry Project (you can search by the project name), then click "Select".
7. Click "Review + assign" to complete the assignment.
8. Allow a few minutes for the role assignment to propagate before running the application.

## Additional Resources

- [Microsoft Agents Framework](https://learn.microsoft.com/en-us/agent-framework/overview/agent-framework-overview)
- [Managed Identities for Azure Resources](https://learn.microsoft.com/en-us/entra/identity/managed-identities-azure-resources/)
