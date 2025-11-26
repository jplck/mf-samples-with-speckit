#!/usr/bin/env sh
set -e

REGISTRY="${AZURE_CONTAINER_REGISTRY_ENDPOINT}"

if [ -z "$REGISTRY" ]; then
  echo "AZURE_CONTAINER_REGISTRY_ENDPOINT is not set. Did provisioning complete successfully?" >&2
  exit 1
fi

if [ "$#" -eq 0 ]; then
  echo "Usage: $0 <image-name>:<dockerfile-path> [<image-name>:<dockerfile-path> ...]" >&2
  echo "Example: $0 product-agent:./src/agents/product-agent other-agent:./src/agents/other-agent" >&2
  exit 1
fi

# Ensure .env exists at repo root so we can append image vars
SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
REPO_ROOT="$SCRIPT_DIR/.."
ENV_FILE="$REPO_ROOT/.env"

if [ ! -f "$ENV_FILE" ]; then
  echo "Creating .env at $ENV_FILE..."
  touch "$ENV_FILE"
fi

for spec in "$@"; do
  IMAGE_NAME="${spec%%:*}"
  CONTEXT_PATH="${spec#*:}"

  if [ -z "$IMAGE_NAME" ] || [ -z "$CONTEXT_PATH" ]; then
    echo "Invalid spec '$spec'. Expected <image-name>:<dockerfile-path>." >&2
    exit 1
  fi

  IMAGE_TAG="$REGISTRY/$IMAGE_NAME:latest"

  echo "Queuing ACR build for $IMAGE_TAG from context $CONTEXT_PATH..."
  az acr build \
    --registry "${REGISTRY%%.*}" \
    --image "$IMAGE_TAG" \
    "$CONTEXT_PATH"
  
  # Persist image URL into .env using a conventional variable name
  # e.g., product-agent -> PRODUCT_AGENT_IMAGE
  IMAGE_VAR_NAME=$(echo "${IMAGE_NAME}_IMAGE" | tr '[:lower:]-' '[:upper:]_')

  # Remove any existing line for this var, then append the new value
  if grep -q "^${IMAGE_VAR_NAME}=" "$ENV_FILE" 2>/dev/null; then
    sed -i "s|^${IMAGE_VAR_NAME}=.*|${IMAGE_VAR_NAME}=${IMAGE_TAG}|" "$ENV_FILE"
  else
    echo "${IMAGE_VAR_NAME}=${IMAGE_TAG}" >> "$ENV_FILE"
  fi
done

echo "ACR builds queued/completed. Deploying hosted agents..."

cd "$REPO_ROOT/src"

if command -v python3 >/dev/null 2>&1; then
  PYTHON_BIN=python3
else
  PYTHON_BIN=python
fi

"$PYTHON_BIN" deploy_agents.py
