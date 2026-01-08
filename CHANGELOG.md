# Changelog

All notable changes to the Ruckus vSZ MCP Server.

## [1.1.0] - 2026-01-08

### Major Release — Multi-Controller, Security & LLM Optimization

Complete overhaul adding enterprise features: multi-controller support, API security, and LLM-optimized responses.

### Added

#### Multi-Controller Support
- **YAML-based configuration** via `config.yaml`
- **Multiple vSZ controllers** with individual credentials
- **Controller selection** via `controller_id` parameter in tool calls
- **Controller manager** for connection pooling
- **`/v1/controllers` endpoint** to list available controllers

#### Security Features
- **Bearer token authentication** for protected endpoints
- **IP whitelisting** with CIDR support (e.g., `10.0.0.0/8`)
- **Rate limiting** per IP address (configurable requests/minute)
- **Security middleware** with comprehensive logging
- **Public endpoints** bypass auth: `/healthz`, `/health`, `/mcp/info`

#### LLM-Optimized Responses
- **Response formatters** — Structured, compact JSON for all tools
- **Null value removal** — Cleaner responses, fewer tokens
- **Summary patterns** — Every list includes counts and pagination info
- **Token efficiency** — 10-50x reduction in response size

#### New Files
- `config.yaml` — Multi-controller configuration
- `ruckus_vsz_server/security.py` — Security middleware
- `ruckus_vsz_server/controller_manager.py` — Multi-controller management
- `ruckus_vsz_server/response_formatters.py` — LLM-optimized formatters
- `SECURITY_QUICKSTART.md` — Security setup guide

### Changed

#### Configuration
- Configuration now uses `config.yaml` (required)
- Credentials via environment variable references (`username_env`, `password_env`)
- Security settings via `api_key_env`, `allowed_ips_env`

#### API Endpoints
- `POST /mcp` — Requires Bearer token (unless public)
- `GET /v1/controllers` — New endpoint for multi-controller
- `GET /mcp/info` — Enhanced with security and controller info

#### vSZ 6.x Compatibility
- Fixed `query/ap` to use `limit` in body (not `listSize`)
- Fixed `query/client` to use `limit` in body
- Fixed `alert/alarm/list` endpoint for alarms
- Fixed `/controller` list response extraction

#### Response Format
All responses now follow LLM-friendly patterns:

```json
// Before (raw API): ~5000 chars with nulls
{"deviceName":"AP-01","description":null,"status":"Online","alerts":0,
 "ip":"10.0.0.1","ipv6Address":null,"txRx":null,"noise24G":null,...}

// After (v1.1.0): ~200 chars, structured
{"summary":{"total":917,"online":882,"offline":35},
 "aps":[{"name":"AP-01","status":"Online","ip":"10.0.0.1","model":"R750"}]}
```

### Response Examples

**System Summary:**
```json
{"controller":{"name":"vSZ01","model":"vSZ-H","version":"6.1.2.0.487"},
 "totals":{"aps":917,"clients":593,"zones":13},"status":{"alerts":147}}
```

**AP List:**
```json
{"summary":{"total":917,"online":882,"offline":35,"has_more":true},
 "aps":[{"name":"AP-01","mac":"AA:BB:CC:DD:EE:FF","status":"Online",
         "ip":"10.0.0.1","model":"R750","zone":"HQ","clients":15}]}
```

**Client List:**
```json
{"summary":{"total":593,"returned":10,"has_more":true},
 "clients":[{"mac":"11:22:33:44:55:66","ip":"10.0.1.100",
             "hostname":"laptop","user":"jdoe","ssid":"Corp","signal":-65}]}
```

**Alarm List:**
```json
{"summary":{"total":147,"critical":0,"major":35,"minor":12},
 "alarms":[{"id":"123","type":"AP disconnected","severity":"Major"}]}
```

### Security Configuration

```yaml
# config.yaml
security:
  api_key_env: "VSZ_API_KEY"           # Bearer token from env var
  allowed_ips_env: "VSZ_ALLOWED_IPS"   # CIDR list from env var
  rate_limit_per_minute: 60
  public_endpoints:
    - "/healthz"
    - "/health"
    - "/mcp/info"
```

```bash
# .env
VSZ_API_KEY=your-32-char-hex-token
VSZ_ALLOWED_IPS=10.0.0.0/8,192.168.0.0/16
```

### Breaking Changes

- **Configuration required**: Must have `config.yaml` with at least one controller
- **Auth required**: Protected endpoints require `Authorization: Bearer <token>`
- **Response format changed**: All responses now use structured JSON format

### Compatibility

- Ruckus vSZ 6.x (tested with 6.1.2.0.487)
- Ruckus vSZ 7.x (API v11_0)
- OpenWebUI v0.6.31+
- MCP Protocol 2024-11-05

#### LLDP Discovery (Added in this release)
- **New tool: `ruckus.aps.get_lldp_neighbors`** — Discover LLDP neighbors (switches, phones) connected to APs
  - Fields: `ap_port`, `neighbor_name`, `neighbor_ip`, `neighbor_port_desc`, `link_speed`
  - Includes anti-hallucination note to prevent LLM from inventing data

#### Multi-MCP Server Support
- **Unique operation IDs** — All FastAPI endpoints now have `ruckus_` prefixed operationIds
  - Prevents conflicts when using multiple MCP servers in OpenWebUI
  - Example: `healthz_healthz_get` → `ruckus_healthz`

#### Additional vSZ 6.x Fixes
- **`zones.get_aps`** — Now uses `query/ap` with zone filter
- **`zones.list_domains`** — Returns friendly error for permission denied
- **`aps.get_operational_info`** — Fallback to `query/ap` when endpoint returns 404
- **`aps.get_clients`** — Uses `query/client` with AP filter
- **`clients.get`** — Fixed query format (`limit` instead of `listSize`)
- **`alarms.get`** — Queries alarm list and finds by ID when direct endpoint fails
- **`network.list_vlan_pools`** — Tries multiple endpoints with friendly error fallback
- **`network.list_qos_profiles`** — Tries multiple endpoints with friendly error fallback

---

## [1.0.0] - 2026-01-01

### Initial Release

- 46 MCP tools across 9 modules
- OpenWebUI MCP Streamable HTTP support
- Docker deployment
- Basic authentication via environment variables
