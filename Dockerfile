FROM python:3.10

# 👇 Environment Variables
ENV UV_VERSION='0.11.29' \
    PATH="/root/.local/bin:$PATH"

WORKDIR /opt/app

# 👇 Installing uv
RUN apt-get update \
    && apt-get install -y curl \
    && curl -LsSf "https://astral.sh/uv/${UV_VERSION}/install.sh" | sh

# 👇 Adding Files
COPY . .

# 👇 Installing project dependencies
RUN uv sync --frozen --no-dev

# 🤘 Let's rock
CMD [ "uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--log-config", "resources/log-config.yml"]
