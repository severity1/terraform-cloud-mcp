# Use Python 3.12 slim image as base
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install uv for faster dependency management
RUN pip install --no-cache-dir uv

# Copy dependency files and README (needed for hatchling build)
COPY pyproject.toml uv.lock README.md LICENSE ./

# Copy the source code
COPY terraform_cloud_mcp/ ./terraform_cloud_mcp/

# Install dependencies and the package using uv
RUN uv sync --frozen --no-dev

# Set environment variables with defaults
ENV TFC_ADDRESS="https://app.terraform.io"
ENV ENABLE_DELETE_TOOLS="false"
ENV READ_ONLY_TOOLS="false"

# Expose that this container expects these environment variables
ENV TFC_TOKEN=""

# Set the entrypoint to run with uv
ENTRYPOINT ["uv", "run", "terraform-cloud-mcp"]
