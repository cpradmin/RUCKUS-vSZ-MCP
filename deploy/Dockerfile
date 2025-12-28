FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY ruckus_vsz_server/ ./ruckus_vsz_server/
COPY pyproject.toml .

# Install package
RUN pip install --no-cache-dir -e .

# Create non-root user
RUN useradd -m -u 1000 ruckus && chown -R ruckus:ruckus /app
USER ruckus

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD python -c "import requests; requests.get('http://localhost:8082/healthz')"

EXPOSE 8082

# Run server
CMD ["ruckus-vsz-mcp-server"]
