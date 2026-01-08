# Ruckus vSZ MCP Server - Deployment Guide

This directory contains Docker deployment configurations for the Ruckus vSZ MCP Server.

## Quick Start

### 1. Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit with your Ruckus vSZ credentials
nano .env
```

### 2. Start the Server

```bash
# Build and start
docker-compose up -d

# View logs
docker-compose logs -f

# Check status
docker-compose ps
```

### 3. Verify Health

```bash
curl http://localhost:8082/healthz
```

Expected response:
```json
{
  "status": "ok",
  "version": "1.0.0"
}
```

## Environment Variables

### Required

- `RUCKUS_VSZ_URL` - Ruckus vSZ controller URL (e.g., `https://vsz.example.com:8443`)
- `RUCKUS_VSZ_USERNAME` - Admin username
- `RUCKUS_VSZ_PASSWORD` - Admin password

### Optional

- `RUCKUS_VSZ_VERIFY_SSL` - SSL certificate verification (default: `true`)
- `RUCKUS_VSZ_TIMEOUT` - API request timeout in seconds (default: `30`)
- `RUCKUS_VSZ_API_VERSION` - API version (default: `v11_0`)
- `LOG_LEVEL` - Logging level (default: `INFO`)

## Docker Commands

### Build Image

```bash
docker build -t ruckus-vsz-mcp-server -f Dockerfile ..
```

### Run Container

```bash
docker run -d \
  --name ruckus-vsz-mcp \
  -p 8082:8082 \
  -e RUCKUS_VSZ_URL="https://vsz.example.com:8443" \
  -e RUCKUS_VSZ_USERNAME="admin" \
  -e RUCKUS_VSZ_PASSWORD="your_password" \
  ruckus-vsz-mcp-server
```

### View Logs

```bash
docker logs -f ruckus-vsz-mcp
```

### Stop and Remove

```bash
docker stop ruckus-vsz-mcp
docker rm ruckus-vsz-mcp
```

## Docker Compose Commands

### Start Services

```bash
docker-compose up -d
```

### Stop Services

```bash
docker-compose down
```

### Rebuild

```bash
docker-compose up -d --build
```

### View Logs

```bash
# All logs
docker-compose logs -f

# Last 100 lines
docker-compose logs --tail=100
```

## Troubleshooting

### Connection Issues

1. Verify Ruckus vSZ is accessible:
   ```bash
   curl -k https://your-vsz.example.com:8443
   ```

2. Check container logs:
   ```bash
   docker-compose logs ruckus-vsz-mcp
   ```

3. Verify environment variables:
   ```bash
   docker-compose config
   ```

### SSL Certificate Issues

If using self-signed certificates:

```bash
# In .env file
RUCKUS_VSZ_VERIFY_SSL=false
```

### Authentication Issues

1. Verify credentials are correct
2. Check user has API access permissions
3. Ensure API version matches your vSZ version

### Port Conflicts

If port 8082 is already in use:

```yaml
# In docker-compose.yml, change:
ports:
  - "8082:8082"  # Use 8082 instead
```

## Health Checks

### Container Health

```bash
docker inspect --format='{{.State.Health.Status}}' ruckus-vsz-mcp
```

### API Health

```bash
curl http://localhost:8082/healthz
```

### MCP Metadata

```bash
curl http://localhost:8082/mcp/metadata
```

## Security Best Practices

1. **Use Environment Files**: Store credentials in `.env` file, not in docker-compose.yml
2. **Enable SSL Verification**: Always use `RUCKUS_VSZ_VERIFY_SSL=true` in production
3. **Secure Networks**: Run on private networks, not exposed to public internet
4. **Regular Updates**: Keep Docker images updated
5. **Audit Logs**: Monitor container logs for security events

## Production Deployment

### Use Docker Secrets (Docker Swarm)

```yaml
version: '3.8'

services:
  ruckus-vsz-mcp:
    image: ruckus-vsz-mcp-server
    secrets:
      - vsz_username
      - vsz_password
    environment:
      RUCKUS_VSZ_URL: https://vsz.example.com:8443
      RUCKUS_VSZ_USERNAME_FILE: /run/secrets/vsz_username
      RUCKUS_VSZ_PASSWORD_FILE: /run/secrets/vsz_password

secrets:
  vsz_username:
    external: true
  vsz_password:
    external: true
```

### Kubernetes Deployment

See `kubernetes/` directory for Kubernetes manifests (if available).

### Reverse Proxy

Example nginx configuration:

```nginx
server {
    listen 443 ssl;
    server_name mcp.example.com;

    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    location / {
        proxy_pass http://localhost:8082;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## Performance Tuning

### Increase Request Timeout

```bash
# In .env
RUCKUS_VSZ_TIMEOUT=60
```

### Adjust Log Level

```bash
# For production
LOG_LEVEL=WARNING

# For debugging
LOG_LEVEL=DEBUG
```

## Monitoring

### Prometheus Metrics

Future enhancement - metrics endpoint at `/metrics`

### Logging

Logs are sent to stdout/stderr and captured by Docker:

```bash
# Follow logs
docker-compose logs -f

# Export logs
docker-compose logs > ruckus-vsz-mcp.log
```

## Support

For issues and questions:
- GitHub Issues: https://github.com/0xEkho/RUCKUS-vSZ-MCP/issues
- Documentation: https://github.com/0xEkho/RUCKUS-vSZ-MCP
