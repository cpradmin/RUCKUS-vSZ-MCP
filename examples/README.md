# Usage Examples

Practical examples for Ruckus vSZ MCP Server v1.1.0 with curl commands.

## API Endpoint

All tool calls use the same endpoint:

```
POST /v1/tools/call
```

## Authentication

When security is enabled, include the Bearer token:

```bash
-H "Authorization: Bearer YOUR_API_KEY"
```

## Base curl Command

```bash
curl -s -X POST http://localhost:8082/v1/tools/call \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{"tool": "TOOL_NAME", "args": {PARAMETERS}}'
```

## Quick Health Check

```bash
# Server health
curl -s http://localhost:8082/healthz

# Server info (47 tools available)
curl -s http://localhost:8082/mcp/info | jq

# System summary
curl -s -X POST http://localhost:8082/v1/tools/call \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{"tool": "ruckus.system.get_summary", "args": {}}' | jq
```

## Available Tools (47 total)

| Module | Tools | Description |
|--------|-------|-------------|
| system | 5 | Controller info, inventory, licenses, cluster |
| zones | 8 | Zone CRUD, list APs/WLANs in zone |
| wlans | 7 | WLAN CRUD, enable/disable |
| aps | 9 | AP management, reboot, query, LLDP neighbors |
| clients | 4 | Client list, disconnect, query |
| monitoring | 4 | Statistics for APs, WLANs, zones |
| alarms | 4 | Alarm list, acknowledge, summary |
| authentication | 3 | RADIUS profiles |
| network | 3 | VLAN pools, QoS profiles |

## Examples

1. **[System Overview](01_system_overview.md)** - Health check, inventory, licenses
2. **[Zone Management](02_zone_management.md)** - List, create, update zones
3. **[WLAN Operations](03_wlan_operations.md)** - Create, update, enable/disable SSIDs
4. **[AP Management](04_ap_management.md)** - Monitor, reboot, query APs
5. **[Client Tracking](05_client_tracking.md)** - List, query, disconnect clients
6. **[Alarm Monitoring](06_alarm_monitoring.md)** - Summary, list, acknowledge alarms

## Response Format

All responses follow this structure:

```json
{
  "status": "ok",
  "data": {
    "result": "{\"summary\":{...},\"items\":[...]}"
  },
  "meta": {
    "tool": "ruckus.tool.name",
    "controller": "vsz-prod"
  }
}
```

The `result` field contains LLM-optimized JSON:
- Compact (no whitespace)
- No null values
- Summary + items pattern

## Multi-Controller Mode

To target a specific controller:

```bash
curl -s -X POST http://localhost:8082/v1/tools/call \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{
    "tool": "ruckus.zones.list",
    "args": {},
    "controller_id": "vsz-dr"
  }'
```

## Error Handling

```json
{
  "status": "error",
  "error": {
    "code": "api_error",
    "message": "Zone not found"
  },
  "meta": {
    "tool": "ruckus.zones.get"
  }
}
```

Error codes:
- `api_error` - vSZ API returned error
- `unknown_tool` - Tool name incorrect
- `invalid_request` - Missing/invalid parameters
- `internal_error` - Server-side error

## Tips

- Use `jq` for formatted JSON output
- Use `-s` flag for silent curl (no progress bar)
- Pipe to `jq -r '.data.result | fromjson'` to parse nested JSON
