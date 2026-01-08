# Client Tracking

List, query, and manage connected wireless clients.

## Tools

| Tool | Description |
|------|-------------|
| `ruckus.clients.list` | List all connected clients |
| `ruckus.clients.get` | Get client details |
| `ruckus.clients.query` | Search clients with filters |
| `ruckus.clients.disconnect` | Disconnect a client |

---

## List All Clients

### curl

```bash
curl -s -X POST http://localhost:8082/v1/tools/call \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{"tool": "ruckus.clients.list", "args": {}}'
```

### With Pagination

```bash
curl -s -X POST http://localhost:8082/v1/tools/call \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{"tool": "ruckus.clients.list", "args": {"index": 0, "list_size": 100}}'
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
    "total": 583,
    "returned": 100,
    "has_more": true
  },
  "clients": [
    {
      "mac": "AA:BB:CC:DD:EE:FF",
      "ip": "192.168.10.45",
      "hostname": "Johns-iPhone",
      "user": "john.doe",
      "os": "iOS",
      "ssid": "CompanyCorp",
      "ap_name": "HQ-A-Floor2-AP05",
      "signal": -62,
      "connected": "2h 15m"
    },
    {
      "mac": "11:22:33:44:55:66",
      "ip": "192.168.100.50",
      "hostname": "LAPTOP-GUEST-05",
      "ssid": "CompanyGuest",
      "ap_name": "Lobby-AP-03",
      "signal": -72
    }
  ]
}
```

---

## Get Client Details

### curl

```bash
curl -s -X POST http://localhost:8082/v1/tools/call \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{"tool": "ruckus.clients.get", "args": {"client_mac": "AA:BB:CC:DD:EE:FF"}}'
```

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `client_mac` | string | **Yes** | Client MAC address |

### Response

```json
{
  "client": {
    "mac": "AA:BB:CC:DD:EE:FF",
    "ip": "192.168.10.45",
    "ipv6": "fe80::1",
    "hostname": "Johns-iPhone",
    "user": "john.doe",
    "os": "iOS",
    "device": "iPhone 15"
  },
  "connection": {
    "ssid": "CompanyCorp",
    "ap_name": "HQ-A-Floor2-AP05",
    "ap_mac": "AA:BB:CC:DD:EE:05",
    "zone": "HQ-Building-A",
    "radio": "5GHz",
    "channel": 36,
    "rssi": -62,
    "snr": 35
  },
  "session": {
    "auth_method": "WPA3-Personal",
    "vlan": 10,
    "connected_since": "2026-01-08T08:15:00Z",
    "traffic_up": 104857600,
    "traffic_down": 524288000
  }
}
```

---

## Query Clients

Search and filter connected clients.

### Search by Hostname

```bash
curl -s -X POST http://localhost:8082/v1/tools/call \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{"tool": "ruckus.clients.query", "args": {"full_text_search": "iPhone"}}'
```

### Filter by SSID

```bash
curl -s -X POST http://localhost:8082/v1/tools/call \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{"tool": "ruckus.clients.query", "args": {"filters": {"ssid": "CompanyGuest"}}}'
```

### Filter by AP

```bash
curl -s -X POST http://localhost:8082/v1/tools/call \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{"tool": "ruckus.clients.query", "args": {"filters": {"apMac": "AA:BB:CC:DD:EE:05"}}}'
```

### Filter by Zone

```bash
curl -s -X POST http://localhost:8082/v1/tools/call \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{"tool": "ruckus.clients.query", "args": {"filters": {"zoneName": "HQ-Building-A"}}}'
```

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `filters` | object | No | Filter criteria |
| `full_text_search` | string | No | Search hostname/MAC/user |
| `index` | integer | No | Pagination start |
| `list_size` | integer | No | Items per page |

### Common Filter Fields

| Field | Description |
|-------|-------------|
| `ssid` | Filter by SSID name |
| `apMac` | Filter by AP MAC |
| `zoneName` | Filter by zone name |
| `osType` | Filter by OS (iOS, Android, Windows) |
| `ipAddress` | Filter by IP address |

---

## Disconnect Client

Force disconnect a client from the network.

### curl

```bash
curl -s -X POST http://localhost:8082/v1/tools/call \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{"tool": "ruckus.clients.disconnect", "args": {"client_mac": "AA:BB:CC:DD:EE:FF"}}'
```

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `client_mac` | string | **Yes** | Client MAC address |

### Response

```json
{
  "status": "success",
  "message": "Client disconnected"
}
```

**Note**: Client may reconnect automatically if credentials are saved.

---

## Signal Quality Guide

| RSSI (dBm) | Quality | User Experience |
|------------|---------|-----------------|
| -30 to -50 | Excellent | Optimal streaming/video |
| -50 to -65 | Good | Normal browsing |
| -65 to -75 | Fair | May see slowdowns |
| -75 to -85 | Poor | Intermittent connectivity |
| Below -85 | Unusable | Frequent disconnects |

---

## Common Use Cases

### Find Guest Clients

```bash
curl -s -X POST http://localhost:8082/v1/tools/call \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{"tool": "ruckus.clients.query", "args": {"filters": {"ssid": "CompanyGuest"}, "list_size": 200}}'
```

### Find Clients with Poor Signal

List all clients, then filter in your application for RSSI < -75.

### Troubleshoot User Issue

1. Search by hostname or username
2. Check RSSI/SNR for signal quality
3. Verify AP and zone
4. Check session duration (frequent reconnects = issue)

### Audit Connected Devices

```bash
# Get all clients with pagination
curl -s -X POST http://localhost:8082/v1/tools/call \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{"tool": "ruckus.clients.list", "args": {"list_size": 500}}'
```
