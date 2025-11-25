# Agent Framework Applications

This project demonstrates building AI agent applications using multiple frameworks:
- **Azure AI Agent Service** - Azure's native agent SDK
- **LangChain/LangGraph** - Popular open-source agent framework
- **AutoGen** - Microsoft's multi-agent conversation framework

## Prerequisites

- Python 3.12+
- `uv` package manager
- Azure subscription with AI Foundry project

## Setup

1. **Install dependencies:**
   ```bash
   uv sync
   ```

2. **Configure environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your Azure credentials
   ```

3. **Run an example:**
   ```bash
   # Azure AI Agent Service example
   uv run python src/agents/azure_agent_example.py
   
   # LangChain example
   uv run python src/agents/langchain_agent_example.py
   
   # AutoGen example
   uv run python src/agents/autogen_agent_example.py
   ```

## Project Structure

```
src/
├── agents/           # Agent implementations
│   ├── azure_agent_example.py
│   ├── langchain_agent_example.py
│   └── autogen_agent_example.py
├── tools/            # Custom tools for agents
│   └── custom_tools.py
└── config/           # Configuration utilities
    └── settings.py
```

## Features

- Multiple agent frameworks in one project
- Shared configuration and utilities
- Custom tool implementations
- Azure integration examples

## Development

Run tests:
```bash
uv run pytest
```

Format code:
```bash
uv run black .
uv run ruff check --fix .
```

Type checking:
```bash
uv run mypy src/
```

## Resources

- [Azure AI Agent Service Documentation](https://learn.microsoft.com/azure/ai-studio/agents/)
- [LangChain Documentation](https://python.langchain.com/)
- [AutoGen Documentation](https://microsoft.github.io/autogen/)
