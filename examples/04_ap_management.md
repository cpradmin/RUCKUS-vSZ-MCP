# AP Management

Monitor, troubleshoot, and manage access points.

## Tools

| Tool | Description |
|------|-------------|
| `ruckus.aps.list` | List all APs |
| `ruckus.aps.get` | Get AP details |
| `ruckus.aps.query` | Search APs with filters |
| `ruckus.aps.update` | Update AP config |
| `ruckus.aps.delete` | Remove AP from management |
| `ruckus.aps.reboot` | Reboot AP |
| `ruckus.aps.get_operational_info` | Get AP operational data |
| `ruckus.aps.get_clients` | Get clients on AP |
| `ruckus.aps.get_lldp_neighbors` | Get LLDP neighbors (switches, phones) |

---

## List All APs

### curl

```bash
curl -s -X POST http://localhost:8082/v1/tools/call \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{"tool": "ruckus.aps.list", "args": {}}'
```

### With Pagination

```bash
curl -s -X POST http://localhost:8082/v1/tools/call \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{"tool": "ruckus.aps.list", "args": {"index": 0, "list_size": 50}}'
```

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `index` | integer | No | Pagination start (default: 0) |
| `list_size` | integer | No | Items per page (default: 100) |

### Response

```json
{
  "summary": {
    "total": 917,
    "online": 890,
    "offline": 27,
    "flagged": 0,
    "has_more": true
  },
  "aps": [
    {
      "name": "HQ-A-Floor1-AP01",
      "mac": "AA:BB:CC:DD:EE:01",
      "status": "Online",
      "ip": "10.1.1.101",
      "model": "R750",
      "zone": "HQ-Building-A",
      "clients": 15,
      "firmware": "6.1.2.0.398"
    },
    {
      "name": "HQ-A-Floor1-AP02",
      "mac": "AA:BB:CC:DD:EE:02",
      "status": "Offline",
      "ip": "10.1.1.102",
      "model": "R750",
      "zone": "HQ-Building-A",
      "clients": 0
    }
  ]
}
```

---

## Get AP Details

### curl

```bash
curl -s -X POST http://localhost:8082/v1/tools/call \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{"tool": "ruckus.aps.get", "args": {"ap_mac": "AA:BB:CC:DD:EE:01"}}'
```

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `ap_mac` | string | **Yes** | AP MAC address |

### Response

```json
{
  "ap": {
    "name": "HQ-A-Floor2-AP05",
    "mac": "AA:BB:CC:DD:EE:05",
    "status": "Online",
    "ip": "10.1.2.105",
    "model": "R750",
    "serial": "1234567890",
    "firmware": "6.1.2.0.398",
    "zone": "HQ-Building-A",
    "group": "Default",
    "location": "Building A, Floor 2, East Wing",
    "description": "Conference room cluster"
  },
  "radio": {
    "channel_2g": 6,
    "channel_5g": 36,
    "channel_6g": 1
  },
  "stats": {
    "clients": 23,
    "uptime": "45d 12h 30m",
    "last_seen": "2026-01-08T10:30:00Z"
  }
}
```

---

## Query APs

Search and filter access points.

### Find Offline APs

```bash
curl -s -X POST http://localhost:8082/v1/tools/call \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{
    "tool": "ruckus.aps.query",
    "args": {
      "filters": {"connectionState": "Disconnect"},
      "list_size": 50
    }
  }'
```

### Search by Name

```bash
curl -s -X POST http://localhost:8082/v1/tools/call \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{"tool": "ruckus.aps.query", "args": {"full_text_search": "Floor2"}}'
```

### Find APs in Zone

```bash
curl -s -X POST http://localhost:8082/v1/tools/call \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{"tool": "ruckus.aps.query", "args": {"filters": {"zoneName": "HQ-Building-A"}}}'
```

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `filters` | object | No | Filter criteria |
| `full_text_search` | string | No | Search by name/MAC/IP |
| `index` | integer | No | Pagination start |
| `list_size` | integer | No | Items per page |

---

## Update AP Configuration

### curl

```bash
curl -s -X POST http://localhost:8082/v1/tools/call \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{
    "tool": "ruckus.aps.update",
    "args": {
      "ap_mac": "AA:BB:CC:DD:EE:05",
      "name": "HQ-A-Floor2-ConfRoom",
      "location": "Building A, Floor 2, Conference Room 201",
      "description": "Main conference room - 50 person capacity"
    }
  }'
```

### With GPS Coordinates

```bash
curl -s -X POST http://localhost:8082/v1/tools/call \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{
    "tool": "ruckus.aps.update",
    "args": {
      "ap_mac": "AA:BB:CC:DD:EE:05",
      "latitude": 37.7749,
      "longitude": -122.4194
    }
  }'
```

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `ap_mac` | string | **Yes** | AP MAC address |
| `name` | string | No | New AP name |
| `description` | string | No | New description |
| `location` | string | No | Location text |
| `latitude` | number | No | GPS latitude |
| `longitude` | number | No | GPS longitude |

---

## Reboot AP

### curl

```bash
curl -s -X POST http://localhost:8082/v1/tools/call \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{"tool": "ruckus.aps.reboot", "args": {"ap_mac": "AA:BB:CC:DD:EE:05"}}'
```

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `ap_mac` | string | **Yes** | AP MAC address |

### Response

```json
{
  "status": "success",
  "message": "Reboot command sent"
}
```

**Note**: AP will be offline for 2-5 minutes during reboot.

---

## Get Clients on AP

### curl

```bash
curl -s -X POST http://localhost:8082/v1/tools/call \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{"tool": "ruckus.aps.get_clients", "args": {"ap_mac": "AA:BB:CC:DD:EE:05"}}'
```

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `ap_mac` | string | **Yes** | AP MAC address |

### Response

```json
{
  "summary": {
    "total": 23,
    "returned": 23
  },
  "clients": [
    {
      "mac": "11:22:33:44:55:66",
      "ip": "192.168.10.45",
      "hostname": "Johns-iPhone",
      "ssid": "CompanyCorp",
      "signal": -62,
      "connected": "2h 15m"
    },
    {
      "mac": "22:33:44:55:66:77",
      "ip": "192.168.10.46",
      "hostname": "LAPTOP-SALES01",
      "ssid": "CompanyCorp",
      "signal": -55,
      "connected": "4h 30m"
    }
  ]
}
```

---

## Get Operational Info

### curl

```bash
curl -s -X POST http://localhost:8082/v1/tools/call \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{"tool": "ruckus.aps.get_operational_info", "args": {"ap_mac": "AA:BB:CC:DD:EE:05"}}'
```

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `ap_mac` | string | **Yes** | AP MAC address |

Returns detailed radio utilization, channel info, and interference levels.

---

## Delete AP

### curl

```bash
curl -s -X POST http://localhost:8082/v1/tools/call \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{"tool": "ruckus.aps.delete", "args": {"ap_mac": "AA:BB:CC:DD:EE:05"}}'
```

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `ap_mac` | string | **Yes** | AP MAC address |

**Warning**: Removes AP from management. AP will need to be re-provisioned.

---

## AP Status Reference

| Status | Meaning | Action |
|--------|---------|--------|
| Online | Normal operation | None |
| Offline | Not reachable | Check power/network |
| Flagged | Has warnings | Review alarms |
| Rebooting | Restarting | Wait 5 minutes |

## Signal Quality Guide

| RSSI (dBm) | Quality | Notes |
|------------|---------|-------|
| -30 to -50 | Excellent | Optimal |
| -50 to -65 | Good | Normal |
| -65 to -75 | Fair | May see slowdowns |
| -75 to -85 | Poor | Consider AP placement |
| Below -85 | Unusable | Client will disconnect |

---

## Get LLDP Neighbors

Discover network devices connected to or detected by an AP via LLDP protocol.
Shows switches, IP phones, and other network equipment.

### curl

```bash
curl -s -X POST http://localhost:8082/v1/tools/call \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{"tool": "ruckus.aps.get_lldp_neighbors", "args": {"ap_mac": "AA:BB:CC:DD:EE:FF"}}'
```

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `ap_mac` | string | **Yes** | AP MAC address |

### Response

```json
{
  "summary": {
    "total": 2,
    "returned": 2
  },
  "neighbors": [
    {
      "ap_port": "eth0",
      "neighbor_name": "HQ-Core-Switch-01",
      "neighbor_desc": "Alcatel-Lucent Enterprise OS6560-P48X4 8.10.102.R01 GA",
      "neighbor_chassis": "mac 78:24:59:91:C8:03",
      "neighbor_port": "local 1020",
      "neighbor_port_desc": "GigabitEthernet 1/1/2",
      "neighbor_ip": "10.1.1.254",
      "capabilities": "Bridge, on;Router, on",
      "uptime": "2 days, 08:36:26",
      "link_speed": "1000BaseTFD - Four-pair Category 5 UTP, full duplex mode"
    },
    {
      "ap_port": "eth4",
      "neighbor_name": "VoIP-Phone-Reception",
      "neighbor_desc": "Yealink SIP-T31P",
      "neighbor_chassis": "ip 10.1.10.50",
      "neighbor_port": "mac 44:DB:D2:57:6A:15",
      "neighbor_port_desc": "WAN PORT",
      "capabilities": "Bridge, on;Tel, on;MDI/PD",
      "uptime": "2 days, 08:34:17",
      "power_source": "PSE",
      "link_speed": "100BaseTXFD - 2 pair category 5 UTP, full duplex mode"
    }
  ]
}
```

### Field Reference

| Field | Description |
|-------|-------------|
| `ap_port` | AP's local Ethernet port (eth0 = uplink, eth1-4 = LAN ports) |
| `neighbor_name` | Hostname of the connected device (switch, phone, etc.) |
| `neighbor_desc` | Device description/model |
| `neighbor_chassis` | Chassis ID (usually MAC address) |
| `neighbor_port` | Port identifier on the neighbor device |
| `neighbor_port_desc` | Port description (e.g., "GigabitEthernet 1/1/2") |
| `neighbor_ip` | Management IP of the neighbor device |
| `capabilities` | Device capabilities (Bridge, Router, Tel, etc.) |
| `link_speed` | Negotiated link speed |

### Use Cases

- **Network Topology Discovery**: Identify which switch port each AP is connected to
- **VoIP Phone Tracking**: Find IP phones connected to AP Ethernet ports
- **Troubleshooting**: Verify AP is connected to correct switch/port
- **Documentation**: Auto-document physical connectivity
