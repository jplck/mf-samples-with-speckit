ARG VARIANT=bookworm
ARG VERSION=3.12
FROM --platform=amd64 mcr.microsoft.com/devcontainers/python:${VERSION}-${VARIANT}

RUN export DEBIAN_FRONTEND=noninteractive \
    && curl -fsSL https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor -o /usr/share/keyrings/microsoft-prod.gpg \
    && curl https://packages.microsoft.com/config/debian/12/prod.list | sudo tee /etc/apt/sources.list.d/mssql-release.list\
    && apt-get update \
    && apt-get install -y xdg-utils unixodbc \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/*

RUN curl https://sh.rustup.rs -sSf | sh -s -- -y

# Install uv - fast Python package installer and resolver
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

# Install Azure Developer CLI (azd)
RUN curl -fsSL https://aka.ms/install-azd.sh | bash

# Add cargo, uv, and azd to PATH for all users
ENV PATH="/root/.cargo/bin:/root/.azd/bin:${PATH}"