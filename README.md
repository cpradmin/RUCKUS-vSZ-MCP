# Ruckus vSZ MCP Server

[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![MCP](https://img.shields.io/badge/MCP-2024--11--05-green.svg)](https://modelcontextprotocol.io/)
[![OpenWebUI](https://img.shields.io/badge/OpenWebUI-v0.6.31%2B-brightgreen.svg)](https://docs.openwebui.com/)

**Model Context Protocol server for Ruckus Virtual SmartZone** — Manage your wireless network through AI.

## Features

- **47 MCP Tools** — Complete vSZ API coverage
- **Multi-Controller** — Manage multiple vSZ instances
- **Security** — Bearer token auth, IP whitelist, rate limiting
- **LLM-Optimized** — Compact JSON responses for efficient token usage
- **OpenWebUI Ready** — MCP Streamable HTTP support

## Quick Start

```bash
# Clone and configure
git clone https://github.com/0xEkho/RUCKUS-vSZ-MCP.git
cd RUCKUS-vSZ-MCP/deploy
cp .env.example .env
# Edit .env with your credentials

# Start
docker-compose up -d

# Verify
curl http://localhost:8082/healthz
```

## Configuration

### 1. Create `config.yaml`

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
  host: "0.0.0.0"
  port: 8082
```

### 2. Create `.env`

```bash
# Controller credentials
VSZ_PROD_USERNAME=admin
VSZ_PROD_PASSWORD=your_password

# API key (generate: openssl rand -hex 32)
VSZ_API_KEY=your_api_key_here
```

### 3. Start Server

```bash
docker-compose up -d
```

## OpenWebUI Integration

1. **Admin Settings** → **Tools** → **Add MCP Server**
2. **URL**: `http://your-server:8082/mcp`
3. **Auth**: Bearer token from `VSZ_API_KEY`
4. Start chatting: *"Show me all offline access points"*

## API Endpoints

| Endpoint | Auth | Description |
|----------|------|-------------|
| `GET /healthz` | No | Health check |
| `GET /mcp/info` | No | Server capabilities |
| `POST /mcp` | Yes | MCP JSON-RPC endpoint |
| `GET /v1/controllers` | Yes | List controllers |

## Tools by Module

### System (5 tools)
- `ruckus.system.get_info` — Controller info
- `ruckus.system.get_summary` — Network overview (APs, clients, zones, alerts)
- `ruckus.system.get_inventory` — Per-zone statistics
- `ruckus.system.get_licenses` — License info
- `ruckus.system.get_cluster_status` — Cluster nodes

### Access Points (9 tools)
- `ruckus.aps.list` — List APs with status
- `ruckus.aps.get` — AP details
- `ruckus.aps.update` — Update AP config
- `ruckus.aps.delete` — Remove AP
- `ruckus.aps.reboot` — Reboot AP
- `ruckus.aps.get_operational_info` — Runtime info
- `ruckus.aps.get_clients` — AP's connected clients
- `ruckus.aps.get_lldp_neighbors` — LLDP neighbors (switches, phones)
- `ruckus.aps.query` — Search APs

### Clients (4 tools)
- `ruckus.clients.list` — Connected clients
- `ruckus.clients.get` — Client details
- `ruckus.clients.disconnect` — Disconnect client
- `ruckus.clients.query` — Search clients

### Zones (8 tools)
- `ruckus.zones.list` — List zones
- `ruckus.zones.get` — Zone details
- `ruckus.zones.create` — Create zone
- `ruckus.zones.update` — Update zone
- `ruckus.zones.delete` — Delete zone
- `ruckus.zones.get_aps` — Zone's APs
- `ruckus.zones.get_wlans` — Zone's WLANs
- `ruckus.zones.list_domains` — List domains

### WLANs (7 tools)
- `ruckus.wlans.list` — List WLANs
- `ruckus.wlans.get` — WLAN details
- `ruckus.wlans.create` — Create WLAN
- `ruckus.wlans.update` — Update WLAN
- `ruckus.wlans.delete` — Delete WLAN
- `ruckus.wlans.enable` — Enable WLAN
- `ruckus.wlans.disable` — Disable WLAN

### Alarms (4 tools)
- `ruckus.alarms.list` — List alarms
- `ruckus.alarms.get` — Alarm details
- `ruckus.alarms.acknowledge` — Acknowledge alarm
- `ruckus.alarms.get_summary` — Alarm counts

### Monitoring (4 tools)
- `ruckus.monitoring.get_ap_statistics`
- `ruckus.monitoring.get_wlan_statistics`
- `ruckus.monitoring.get_zone_statistics`
- `ruckus.monitoring.get_active_client_count`

### Authentication (3 tools)
- `ruckus.authentication.list_radius_profiles`
- `ruckus.authentication.get_radius_profile`
- `ruckus.authentication.create_radius_profile`

### Network (3 tools)
- `ruckus.network.list_vlan_pools`
- `ruckus.network.create_vlan_pool`
- `ruckus.network.list_qos_profiles`

## Response Format

All responses are LLM-optimized JSON:

```json
// System Summary
{"controller":{"name":"vSZ01","model":"vSZ-H","version":"6.1.2.0.487"},
 "totals":{"aps":917,"clients":593,"zones":13},"status":{"alerts":147}}

// AP List
{"summary":{"total":917,"online":882,"offline":35,"has_more":true},
 "aps":[{"name":"AP-01","mac":"AA:BB:CC:DD:EE:FF","status":"Online",
         "ip":"10.0.0.1","model":"R750","zone":"HQ","clients":15}]}

// Alarm List  
{"summary":{"total":147,"critical":0,"major":35,"minor":12},
 "alarms":[{"id":"123","type":"AP disconnected","severity":"Major"}]}
```

## Security

See [SECURITY_QUICKSTART.md](SECURITY_QUICKSTART.md) for:
- API key generation
- IP whitelisting
- Rate limiting configuration

## Documentation

- [SECURITY_QUICKSTART.md](SECURITY_QUICKSTART.md) — Security setup
- [OPEN_WEBUI_QUICKSTART.md](OPEN_WEBUI_QUICKSTART.md) — OpenWebUI integration

## Requirements

- Python 3.11+ or Docker
- Ruckus vSZ 6.x or 7.x (API v11_0)
- Network access to vSZ (port 8443)

## License

MIT License — see [LICENSE](LICENSE)
