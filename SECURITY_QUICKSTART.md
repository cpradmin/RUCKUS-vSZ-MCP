# Security Quick Start

Deploy Ruckus vSZ MCP Server with enterprise security in 5 minutes.

## 1. Generate API Key

```bash
openssl rand -hex 32
# Example: a1b2c3d4e5f6789012345678901234567890abcdef12345678
```

## 2. Create Configuration

### config.yaml

```yaml
controllers:
  - id: "vsz-prod"
    name: "Production vSZ"
    url: "https://vsz.example.com:8443"
    username_env: "VSZ_PROD_USERNAME"
    password_env: "VSZ_PROD_PASSWORD"
    verify_ssl: false
    api_version: "v11_0"

security:
  api_key_env: "VSZ_API_KEY"
  allowed_ips_env: "VSZ_ALLOWED_IPS"  # Optional
  rate_limit_per_minute: 60
  public_endpoints:
    - "/healthz"
    - "/health"
    - "/mcp/info"

server:
  host: "0.0.0.0"
  port: 8082
```

### deploy/.env

```bash
# Controller credentials
VSZ_PROD_USERNAME=admin
VSZ_PROD_PASSWORD=your_password

# Security
VSZ_API_KEY=your-generated-api-key-here

# Optional: IP whitelist (comma-separated CIDRs)
# VSZ_ALLOWED_IPS=10.0.0.0/8,192.168.0.0/16
```

## 3. Deploy

```bash
cd deploy
docker-compose up -d
```

## 4. Test Security

```bash
# Health check (public - no auth)
curl http://localhost:8082/healthz
# {"status":"ok","version":"1.1.0","controllers":1}

# Without token (should fail)
curl http://localhost:8082/v1/controllers
# {"error":"Unauthorized","detail":"Invalid or missing Bearer token"}

# With token (should work)
curl -H "Authorization: Bearer your-api-key" http://localhost:8082/v1/controllers
# {"controllers":[...],"total":1}

# MCP info (public)
curl http://localhost:8082/mcp/info
# {"name":"ruckus-vsz-mcp-server","version":"1.1.0",...}
```

## OpenWebUI Configuration

1. **Admin Settings** → **Tools** → **Add MCP Server**
2. Configure:
   - **Type**: MCP (Streamable HTTP)
   - **URL**: `http://your-server:8082/mcp`
   - **Auth Header**: `Authorization`
   - **Auth Value**: `Bearer your-api-key`
3. **Save**

## Security Features

| Feature | Description |
|---------|-------------|
| **Bearer Token** | Required for all protected endpoints |
| **IP Whitelist** | Optional CIDR-based access control |
| **Rate Limiting** | Per-IP request limits (default: 60/min) |
| **Public Endpoints** | `/healthz`, `/health`, `/mcp/info` bypass auth |

## Multi-Controller Setup

```yaml
# config.yaml
controllers:
  - id: "vsz-prod"
    name: "Production"
    url: "https://vsz-prod.example.com:8443"
    username_env: "VSZ_PROD_USERNAME"
    password_env: "VSZ_PROD_PASSWORD"

  - id: "vsz-dr"
    name: "Disaster Recovery"
    url: "https://vsz-dr.example.com:8443"
    username_env: "VSZ_DR_USERNAME"
    password_env: "VSZ_DR_PASSWORD"

default_controller: "vsz-prod"
```

```bash
# .env
VSZ_PROD_USERNAME=admin
VSZ_PROD_PASSWORD=prod_pass
VSZ_DR_USERNAME=admin
VSZ_DR_PASSWORD=dr_pass
VSZ_API_KEY=your-api-key
```

## Troubleshooting

| Error | Cause | Solution |
|-------|-------|----------|
| 401 Unauthorized | Missing/invalid token | Check `VSZ_API_KEY` in `.env` |
| 403 Access denied | IP not in whitelist | Add IP to `VSZ_ALLOWED_IPS` |
| 429 Too Many Requests | Rate limit exceeded | Increase `rate_limit_per_minute` |

## Best Practices

- ✅ Generate 32+ character API keys
- ✅ Use environment variables for credentials
- ✅ Enable IP whitelisting in production
- ✅ Use read-only vSZ account
- ✅ Place behind HTTPS reverse proxy
- ❌ Don't commit credentials to git
- ❌ Don't share API keys between services

---

**Version**: 1.1.0
