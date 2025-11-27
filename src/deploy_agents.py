import os
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import ImageBasedHostedAgentDefinition, ProtocolVersionRecord, AgentProtocol
from azure.identity import DefaultAzureCredential

from dotenv import load_dotenv

load_dotenv()

def get_env(name: str, required: bool = True, default: str | None = None) -> str:
  value = os.getenv(name, default)
  if required and not value:
      raise RuntimeError(f"Missing required environment variable: {name}")
  return value


def main() -> None:
  # These come from azd / Bicep outputs and the container images we built
  project_endpoint = get_env("AZURE_AI_PROJECT_ENDPOINT", required=True)
  model_deployment_name = get_env("AZURE_AI_MODEL_DEPLOYMENT_NAME", required=True, default="o4-mini")
  aoai_endpoint = get_env("AZURE_OPENAI_ENDPOINT", required=True)
  openai_api_version = get_env("OPENAI_API_VERSION", required=True, default="2024-05-01-preview")

  credential = DefaultAzureCredential()

  client = AIProjectClient(
      endpoint=project_endpoint,
      credential=credential,
  )

  # Shared container protocol versions for hosted agents
  protocols = [ProtocolVersionRecord(protocol=AgentProtocol.RESPONSES, version="v1")]

  # Automatically discover all *_IMAGE variables in the environment
  # and create/update a hosted agent for each.
  for key, value in os.environ.items():
      if not key.endswith("_IMAGE"):
          continue

      image_tag = value
      if not image_tag:
          continue

      # Derive agent name from variable name, e.g.
      # PRODUCT_AGENT_IMAGE -> product-agent
      base_name = key[:-len("_IMAGE")]  # strip suffix
      # Replace _ with - and lowercase
      agent_name = base_name.lower().replace("_", "-")

      agent = client.agents.create_version(
          agent_name=agent_name,
          description=f"Hosted agent for {agent_name}",
          definition=ImageBasedHostedAgentDefinition(
              container_protocol_versions=protocols,
              cpu="1",
              memory="2Gi",
              image=image_tag,
              environment_variables={
                  "AZURE_AI_PROJECT_ENDPOINT": project_endpoint,
                  "AZURE_AI_MODEL_DEPLOYMENT_NAME": model_deployment_name,
                  "AZURE_OPENAI_CHAT_DEPLOYMENT_NAME": model_deployment_name,
                  "AZURE_OPENAI_ENDPOINT": aoai_endpoint,
                  "OPENAI_API_VERSION": openai_api_version,
              },
          ),
      )
      print(f"Agent '{agent_name}' created: {agent.id}")


if __name__ == "__main__":
  main()