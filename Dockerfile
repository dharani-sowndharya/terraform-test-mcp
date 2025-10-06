FROM python:3.13-slim

WORKDIR /app

# Install uv for faster Python package management
RUN pip install uv

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies using uv
RUN uv sync --frozen

# Copy application files
COPY main.py prompt_template.md validation.py enforcement.py ./

# Create non-root user for security
RUN addgroup --gid 1001 --system mcpuser && \
    adduser --uid 1001 --system --group mcpuser
RUN chown -R mcpuser:mcpuser /app

USER mcpuser

# Set environment variables
ENV PYTHONPATH=/app
ENV MCP_SERVER_NAME=terraform-test-mcp
ENV MCP_TRANSPORT=stdio

# Run the MCP server
CMD ["uv", "run", "python", "main.py"]