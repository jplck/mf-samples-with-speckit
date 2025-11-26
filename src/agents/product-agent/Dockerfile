FROM python:3.11-slim

WORKDIR /app

COPY . product_agent/
WORKDIR /app/product_agent

RUN if [ -f requirements.txt ]; then \
        pip install -r requirements.txt; \
    else \
        echo "No requirements.txt found"; \
    fi

EXPOSE 8088

CMD ["python", "container.py"]