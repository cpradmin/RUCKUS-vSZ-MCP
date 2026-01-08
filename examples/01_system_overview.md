# System Overview

Get controller status, inventory, and health information.

## Tools

| Tool | Description |
|------|-------------|
| `ruckus.system.get_info` | Controller version, model, uptime |
| `ruckus.system.get_summary` | AP/client/zone counts |
| `ruckus.system.get_inventory` | Zone-by-zone breakdown |
| `ruckus.system.get_licenses` | License status |
| `ruckus.system.get_cluster_status` | HA cluster info |

---

## Get System Summary

Quick overview of network status.

### curl

```bash
curl -s -X POST http://localhost:8082/v1/tools/call \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{"tool": "ruckus.system.get_summary", "args": {}}'
```

### Parameters

None required.

### Response

```json
{
  "status": "ok",
  "data": {
    "result": "{\"controller\":{\"name\":\"vSZ01\",\"model\":\"vSZ-H\",\"version\":\"6.1.2.0.487\"},\"totals\":{\"aps\":917,\"clients\":583,\"zones\":13},\"status\":{\"alerts\":147}}"
  },
  "meta": {
    "tool": "ruckus.system.get_summary",
    "controller": "vsz-prod"
  }
}
```

### Parsed Result

```json
{
  "controller": {
    "name": "vSZ01",
    "model": "vSZ-H",
    "version": "6.1.2.0.487"
  },
  "totals": {
    "aps": 917,
    "clients": 583,
    "zones": 13
  },
  "status": {
    "alerts": 147
  }
}
```

---

## Get System Info

Detailed controller information.

### curl

```bash
curl -s -X POST http://localhost:8082/v1/tools/call \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{"tool": "ruckus.system.get_info", "args": {}}'
```

### Parameters

None required.

### Response Fields

| Field | Description |
|-------|-------------|
| `controller.name` | Controller hostname |
| `controller.model` | vSZ model (vSZ-H, vSZ-E) |
| `controller.version` | Firmware version |
| `controller.serial` | Serial number |
| `controller.uptime` | Time since boot |
| `network.management_ip` | Management IP address |
| `network.control_ip` | Control plane IP |
| `network.cluster_ip` | Cluster VIP |

---

## Get System Inventory

Zone-by-zone AP and client breakdown.

### curl

```bash
curl -s -X POST http://localhost:8082/v1/tools/call \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{"tool": "ruckus.system.get_inventory", "args": {}}'
```

### Parameters

None required.

### Response

```json
{
  "summary": {
    "zones": 13,
    "total_aps": 917,
    "online_aps": 890,
    "offline_aps": 27,
    "total_clients": 583
  },
  "zones": [
    {
      "name": "HQ-Building-A",
      "aps": 120,
      "online": 118,
      "offline": 2,
      "clients": 450,
      "firmware": "6.1.2.0.398"
    }
  ]
}
```

---

## Get Licenses

Check license capacity and expiration.

### curl

```bash
curl -s -X POST http://localhost:8082/v1/tools/call \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{"tool": "ruckus.system.get_licenses", "args": {}}'
```

### Parameters

None required.

### Response

```json
{
  "license_count": 2,
  "licenses": [
    {
      "type": "AP_MANAGEMENT",
      "capacity": 1000,
      "used": 917,
      "expiry": "2026-12-31"
    }
  ]
}
```

---

## Get Cluster Status

HA cluster health and node status.

### curl

```bash
curl -s -X POST http://localhost:8082/v1/tools/call \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{"tool": "ruckus.system.get_cluster_status", "args": {}}'
```

### Parameters

None required.

### Response

```json
{
  "cluster_state": "In_Service",
  "node_count": 2,
  "nodes": [
    {
      "name": "vSZ-Node1",
      "role": "Leader",
      "state": "In_Service",
      "ip": "10.0.1.10",
      "version": "6.1.2.0.398"
    },
    {
      "name": "vSZ-Node2",
      "role": "Follower",
      "state": "In_Service",
      "ip": "10.0.1.11"
    }
  ]
}
```

---

## Parse Nested JSON

To extract the `result` field as JSON:

```bash
curl -s -X POST http://localhost:8082/v1/tools/call \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{"tool": "ruckus.system.get_summary", "args": {}}' \
  | jq -r '.data.result | fromjson'
```

Output:
```json
{
  "controller": {
    "name": "vSZ01",
    "model": "vSZ-H",
    "version": "6.1.2.0.487"
  },
  "totals": {
    "aps": 917,
    "clients": 583,
    "zones": 13
  },
  "status": {
    "alerts": 147
  }
}
```
