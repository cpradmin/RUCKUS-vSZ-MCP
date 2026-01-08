# OpenWebUI Quick Start

Connect Ruckus vSZ MCP Server to OpenWebUI in 5 minutes.

## Prerequisites

- Docker running
- OpenWebUI v0.6.31+
- Ruckus vSZ accessible on network

## 1. Deploy MCP Server

```bash
cd RUCKUS-vSZ-MCP/deploy

# Configure
cp .env.example .env
# Edit .env with your vSZ credentials and API key

# Start
docker-compose up -d

# Verify
curl http://localhost:8082/healthz
# {"status":"ok","version":"1.1.0","controllers":1}
```

## 2. Configure OpenWebUI

1. **Admin Settings** → **Tools** → **Add MCP Server**
2. Fill in:
   - **Type**: MCP (Streamable HTTP)
   - **Name**: Ruckus vSZ
   - **URL**: `http://your-server:8082/mcp`
   - **Auth Header**: `Authorization`
   - **Auth Value**: `Bearer your-api-key`
3. **Save**

## 3. Test

Ask your LLM:
> "Show me all access points"

The LLM will call `ruckus.aps.list` and return a structured response.

## Example Prompts

| Prompt | Tool Called |
|--------|-------------|
| "Show me system info" | `ruckus.system.get_info` |
| "How many clients are connected?" | `ruckus.system.get_summary` |
| "List all zones" | `ruckus.zones.list` |
| "Show offline APs" | `ruckus.aps.list` |
| "What alarms are active?" | `ruckus.alarms.list` |
| "Find client with MAC AA:BB:CC:DD:EE:FF" | `ruckus.clients.get` |

## Configuration Files

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
  rate_limit_per_minute: 60

server:
  port: 8082
```

### .env

```bash
VSZ_PROD_USERNAME=admin
VSZ_PROD_PASSWORD=your_password
VSZ_API_KEY=your-api-key-from-openssl-rand-hex-32
```

## Verify Connection

```bash
# Server info
curl http://localhost:8082/mcp/info

# Tool list (with auth)
curl -H "Authorization: Bearer your-api-key" \
  -X POST http://localhost:8082/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}'

# Test tool call
curl -H "Authorization: Bearer your-api-key" \
  -X POST http://localhost:8082/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"ruckus.system.get_summary"}}'
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Connection refused | Check Docker: `docker ps` |
| 401 Unauthorized | Verify API key in OpenWebUI matches `.env` |
| Tools not showing | Refresh OpenWebUI, check `/mcp/info` |
| vSZ connection failed | Check vSZ URL and credentials |
| LLM invents data | Add system prompt (see below) |

## Preventing LLM Hallucinations

If the LLM invents device names or IPs instead of using real data:

### Option 1: System Prompt

Add this to your model's system prompt in OpenWebUI:

```
When using MCP tools, always use the EXACT values from tool responses.
Never invent, fabricate, or modify device names, IPs, MAC addresses, or other data.
If data is missing, say "not available" instead of making up values.
```

### Option 2: Per-Chat Instructions

Start your conversation with:
> "Use only real data from the tools. Do not invent any names or values."

## Response Format

All responses are LLM-optimized JSON:

```json
// System Summary
{"controller":{"name":"vSZ01","version":"6.1.2.0.487"},
 "totals":{"aps":917,"clients":593,"zones":13}}

// AP List
{"summary":{"total":917,"online":882,"offline":35},
 "aps":[{"name":"AP-01","status":"Online","ip":"10.0.0.1"}]}
```

---

**Version**: 1.1.0
