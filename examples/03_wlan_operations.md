# WLAN Operations

Create, update, and manage wireless networks (SSIDs).

## Tools

| Tool | Description |
|------|-------------|
| `ruckus.wlans.list` | List WLANs in zone |
| `ruckus.wlans.get` | Get WLAN details |
| `ruckus.wlans.create` | Create new WLAN |
| `ruckus.wlans.update` | Update WLAN config |
| `ruckus.wlans.delete` | Delete WLAN |
| `ruckus.wlans.enable` | Enable WLAN |
| `ruckus.wlans.disable` | Disable WLAN |

---

## List WLANs

### curl

```bash
curl -s -X POST http://localhost:8082/v1/tools/call \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{"tool": "ruckus.wlans.list", "args": {"zone_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890"}}'
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
    "total": 4,
    "has_more": false
  },
  "wlans": [
    {
      "id": "wlan-1-uuid",
      "name": "Corporate-WiFi",
      "ssid": "CompanyCorp",
      "zone": "HQ-Building-A",
      "security": "WPA3",
      "vlan": 10,
      "enabled": true
    },
    {
      "id": "wlan-2-uuid",
      "name": "Guest-WiFi",
      "ssid": "CompanyGuest",
      "zone": "HQ-Building-A",
      "security": "WPA2",
      "vlan": 100,
      "enabled": true
    }
  ]
}
```

---

## Get WLAN Details

### curl

```bash
curl -s -X POST http://localhost:8082/v1/tools/call \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{
    "tool": "ruckus.wlans.get",
    "args": {
      "zone_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
      "wlan_id": "wlan-2-uuid"
    }
  }'
```

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `zone_id` | string | **Yes** | Zone UUID |
| `wlan_id` | string | **Yes** | WLAN UUID |

### Response

```json
{
  "wlan": {
    "id": "wlan-2-uuid",
    "name": "Guest-WiFi",
    "ssid": "CompanyGuest",
    "zone_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "enabled": true
  },
  "security": {
    "auth_type": "WPA2",
    "encryption": "AES",
    "wpa_version": "WPA2"
  },
  "network": {
    "vlan": 100,
    "hide_ssid": false
  }
}
```

---

## Create WLAN

### WPA2 Guest Network

```bash
curl -s -X POST http://localhost:8082/v1/tools/call \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{
    "tool": "ruckus.wlans.create",
    "args": {
      "zone_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
      "name": "Guest-WiFi",
      "ssid": "CompanyGuest",
      "authentication_type": "WPA2",
      "encryption_method": "AES",
      "passphrase": "Welcome2026!",
      "vlan_id": 100,
      "description": "Guest and visitor network"
    }
  }'
```

### WPA3 Corporate Network

```bash
curl -s -X POST http://localhost:8082/v1/tools/call \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{
    "tool": "ruckus.wlans.create",
    "args": {
      "zone_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
      "name": "Corporate-Secure",
      "ssid": "CompanyCorp",
      "authentication_type": "WPA3",
      "encryption_method": "AES",
      "passphrase": "SecurePass2026!Complex",
      "vlan_id": 10
    }
  }'
```

### Open Network (Captive Portal)

```bash
curl -s -X POST http://localhost:8082/v1/tools/call \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{
    "tool": "ruckus.wlans.create",
    "args": {
      "zone_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
      "name": "Conference-WiFi",
      "ssid": "CompanyEvent",
      "authentication_type": "Open",
      "vlan_id": 200,
      "description": "Temporary event network"
    }
  }'
```

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `zone_id` | string | **Yes** | Zone UUID |
| `name` | string | **Yes** | Internal WLAN name |
| `ssid` | string | **Yes** | Broadcast SSID |
| `authentication_type` | string | No | Open, WPA2, WPA3 (default: Open) |
| `encryption_method` | string | No | AES, TKIP |
| `passphrase` | string | No | WPA password (8-63 chars) |
| `vlan_id` | integer | No | VLAN assignment |
| `description` | string | No | WLAN description |

### Response

```json
{
  "status": "success",
  "message": "WLAN created",
  "id": "new-wlan-uuid"
}
```

---

## Update WLAN

### curl

```bash
curl -s -X POST http://localhost:8082/v1/tools/call \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{
    "tool": "ruckus.wlans.update",
    "args": {
      "zone_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
      "wlan_id": "wlan-2-uuid",
      "ssid": "CompanyGuest-Feb2026",
      "description": "Guest network - February 2026"
    }
  }'
```

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `zone_id` | string | **Yes** | Zone UUID |
| `wlan_id` | string | **Yes** | WLAN UUID |
| `name` | string | No | New internal name |
| `ssid` | string | No | New broadcast SSID |
| `description` | string | No | New description |

### Response

```json
{
  "status": "success",
  "message": "WLAN updated"
}
```

---

## Enable WLAN

### curl

```bash
curl -s -X POST http://localhost:8082/v1/tools/call \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{
    "tool": "ruckus.wlans.enable",
    "args": {
      "zone_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
      "wlan_id": "wlan-2-uuid"
    }
  }'
```

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `zone_id` | string | **Yes** | Zone UUID |
| `wlan_id` | string | **Yes** | WLAN UUID |

---

## Disable WLAN

### curl

```bash
curl -s -X POST http://localhost:8082/v1/tools/call \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{
    "tool": "ruckus.wlans.disable",
    "args": {
      "zone_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
      "wlan_id": "wlan-2-uuid"
    }
  }'
```

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `zone_id` | string | **Yes** | Zone UUID |
| `wlan_id` | string | **Yes** | WLAN UUID |

---

## Delete WLAN

### curl

```bash
curl -s -X POST http://localhost:8082/v1/tools/call \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{
    "tool": "ruckus.wlans.delete",
    "args": {
      "zone_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
      "wlan_id": "wlan-2-uuid"
    }
  }'
```

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `zone_id` | string | **Yes** | Zone UUID |
| `wlan_id` | string | **Yes** | WLAN UUID |

**Warning**: Disconnects all clients on this SSID immediately.

---

## Security Recommendations

| Network Type | Auth | VLAN | Notes |
|--------------|------|------|-------|
| Corporate | WPA3 | 10-19 | Employee devices |
| Guest | WPA2 | 100-199 | Isolated, rate-limited |
| IoT | WPA2 | 50-59 | Device-specific |
| Event | Open | 200+ | Temporary, captive portal |
