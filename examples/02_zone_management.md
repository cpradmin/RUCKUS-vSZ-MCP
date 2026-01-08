# Zone Management

Manage wireless zones - organizational units grouping APs and WLANs.

## Tools

| Tool | Description |
|------|-------------|
| `ruckus.zones.list` | List all zones |
| `ruckus.zones.get` | Get zone details |
| `ruckus.zones.create` | Create new zone |
| `ruckus.zones.update` | Update zone config |
| `ruckus.zones.delete` | Delete zone |
| `ruckus.zones.get_aps` | List APs in zone |
| `ruckus.zones.get_wlans` | List WLANs in zone |
| `ruckus.zones.list_domains` | List domains |

---

## List All Zones

### curl

```bash
curl -s -X POST http://localhost:8082/v1/tools/call \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{"tool": "ruckus.zones.list", "args": {}}'
```

### With Pagination

```bash
curl -s -X POST http://localhost:8082/v1/tools/call \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{"tool": "ruckus.zones.list", "args": {"index": 0, "list_size": 10}}'
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
    "total": 13,
    "has_more": false
  },
  "zones": [
    {
      "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
      "name": "HQ-Building-A",
      "description": "Headquarters main building",
      "ap_count": 120,
      "client_count": 450
    },
    {
      "id": "b2c3d4e5-f6a7-8901-bcde-f23456789012",
      "name": "Branch-NYC",
      "description": "New York office",
      "ap_count": 45
    }
  ]
}
```

---

## Get Zone Details

### curl

```bash
curl -s -X POST http://localhost:8082/v1/tools/call \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{"tool": "ruckus.zones.get", "args": {"zone_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890"}}'
```

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `zone_id` | string | **Yes** | Zone UUID |

### Response

```json
{
  "zone": {
    "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "name": "HQ-Building-A",
    "description": "Headquarters main building",
    "country_code": "US",
    "timezone": "America/New_York"
  },
  "stats": {
    "ap_count": 120,
    "client_count": 450,
    "wlan_count": 5
  },
  "settings": {
    "ap_firmware": "6.1.2.0.398",
    "login_session_timeout": 1440
  }
}
```

---

## Create Zone

### curl

```bash
curl -s -X POST http://localhost:8082/v1/tools/call \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{
    "tool": "ruckus.zones.create",
    "args": {
      "name": "Branch-Miami",
      "description": "Miami office - opened Jan 2026"
    }
  }'
```

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `name` | string | **Yes** | Zone name |
| `description` | string | No | Zone description |
| `domain_id` | string | No | Parent domain UUID |

### Response

```json
{
  "status": "success",
  "message": "Zone created",
  "id": "d4e5f6a7-b8c9-0123-def4-567890123456"
}
```

---

## Update Zone

### curl

```bash
curl -s -X POST http://localhost:8082/v1/tools/call \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{
    "tool": "ruckus.zones.update",
    "args": {
      "zone_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
      "description": "HQ Building A - Floors 1-5"
    }
  }'
```

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `zone_id` | string | **Yes** | Zone UUID |
| `name` | string | No | New name |
| `description` | string | No | New description |

---

## Delete Zone

### curl

```bash
curl -s -X POST http://localhost:8082/v1/tools/call \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{"tool": "ruckus.zones.delete", "args": {"zone_id": "d4e5f6a7-b8c9-0123-def4-567890123456"}}'
```

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `zone_id` | string | **Yes** | Zone UUID |

**Warning**: Deletes all APs and WLANs in the zone.

---

## Get APs in Zone

### curl

```bash
curl -s -X POST http://localhost:8082/v1/tools/call \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{
    "tool": "ruckus.zones.get_aps",
    "args": {
      "zone_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
      "list_size": 50
    }
  }'
```

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `zone_id` | string | **Yes** | Zone UUID |
| `index` | integer | No | Pagination start |
| `list_size` | integer | No | Items per page |

### Response

```json
{
  "summary": {
    "total": 120,
    "online": 118,
    "offline": 2,
    "has_more": true
  },
  "aps": [
    {
      "name": "HQ-A-Floor1-AP01",
      "mac": "AA:BB:CC:DD:EE:01",
      "status": "Online",
      "ip": "10.1.1.101",
      "model": "R750",
      "clients": 12
    }
  ]
}
```

---

## Get WLANs in Zone

### curl

```bash
curl -s -X POST http://localhost:8082/v1/tools/call \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{"tool": "ruckus.zones.get_wlans", "args": {"zone_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890"}}'
```

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `zone_id` | string | **Yes** | Zone UUID |

### Response

```json
{
  "summary": {
    "total": 5
  },
  "wlans": [
    {
      "id": "wlan-uuid-1",
      "name": "Corporate-WiFi",
      "ssid": "CompanyCorp",
      "security": "WPA3",
      "vlan": 10,
      "enabled": true
    },
    {
      "id": "wlan-uuid-2",
      "name": "Guest-WiFi",
      "ssid": "CompanyGuest",
      "security": "WPA2",
      "vlan": 100,
      "enabled": true
    }
  ]
}
```

---

## List Domains

### curl

```bash
curl -s -X POST http://localhost:8082/v1/tools/call \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{"tool": "ruckus.zones.list_domains", "args": {}}'
```

### Parameters

None required.
