# ruckus.zones.list - List All Zones

## Purpose

Retrieve complete list of wireless zones from Ruckus vSZ controller. Zones are organizational units that group access points and WLANs together. Essential for understanding wireless network structure and segmentation.

## When to Use

- Getting overview of wireless network organization
- Building automated network documentation
- Finding zone IDs for WLAN or AP operations
- Auditing zone structure and AP distribution
- Planning wireless network expansions
- Generating zone capacity reports

## Use Case

**Scenario**: Network team needs comprehensive inventory of all wireless zones for documentation, including zone names, descriptions, and AP counts to plan capacity expansion.

**User Prompt**: "List all wireless zones in the network with their details"

## Request

```bash
curl -s \
  -H "Content-Type: application/json" \
  -X POST "http://localhost:8082/v1/tools/call" \
  -d '{
    "context": {
      "subject": "wireless-admin@company.com",
      "correlation_id": "zone-inventory-2024"
    },
    "tool": "ruckus.zones.list",
    "args": {}
  }' | jq
```

### With Pagination

```bash
curl -s \
  -H "Content-Type: application/json" \
  -X POST "http://localhost:8082/v1/tools/call" \
  -d '{
    "tool": "ruckus.zones.list",
    "args": {
      "index": 0,
      "list_size": 10
    }
  }' | jq
```

### Arguments

- **index** (optional): Starting index for pagination
  - Default: 0
  - Use for paginating large zone lists
- **list_size** (optional): Number of zones to return
  - Default: 100
  - Maximum: 1000
  - Recommended: 50-100 for optimal performance

## Expected Response

### Success

```json
{
  "status": "ok",
  "data": {
    "result": "{\n  \"list\": [\n    {\n      \"id\": \"a1b2c3d4-e5f6-7890-abcd-ef1234567890\",\n      \"name\": \"Campus-Zone\",\n      \"description\": \"Main campus wireless zone\",\n      \"domainId\": \"8b7a6c5d-4e3f-2a1b-0c9d-8e7f6a5b4c3d\",\n      \"apCount\": 25,\n      \"wlanCount\": 5,\n      \"clientCount\": 340\n    },\n    {\n      \"id\": \"b2c3d4e5-f6a7-8901-bcde-f23456789012\",\n      \"name\": \"Guest-Zone\",\n      \"description\": \"Guest access zone\",\n      \"domainId\": \"8b7a6c5d-4e3f-2a1b-0c9d-8e7f6a5b4c3d\",\n      \"apCount\": 10,\n      \"wlanCount\": 2,\n      \"clientCount\": 85\n    }\n  ],\n  \"totalCount\": 2,\n  \"hasMore\": false\n}"
  },
  "meta": {
    "tool": "ruckus.zones.list"
  }
}
```

### Response Fields

- **id**: Zone UUID (required for other operations)
- **name**: Zone display name
- **description**: Zone purpose/description
- **domainId**: Parent domain UUID
- **apCount**: Number of APs in zone
- **wlanCount**: Number of WLANs configured
- **clientCount**: Currently connected clients
- **totalCount**: Total zones available
- **hasMore**: More results available (pagination)

### Empty Result

```json
{
  "status": "ok",
  "data": {
    "result": "{\n  \"list\": [],\n  \"totalCount\": 0\n}"
  },
  "meta": {
    "tool": "ruckus.zones.list"
  }
}
```

## Follow-up Actions

### Get Zone Details
```bash
curl -s -H "Content-Type: application/json" -X POST \
  "http://localhost:8082/v1/tools/call" \
  -d '{"tool": "ruckus.zones.get", "args": {"zone_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890"}}' | jq
```

### List APs in Zone
```bash
curl -s -H "Content-Type: application/json" -X POST \
  "http://localhost:8082/v1/tools/call" \
  -d '{"tool": "ruckus.zones.get_aps", "args": {"zone_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890"}}' | jq
```

### List WLANs in Zone
```bash
curl -s -H "Content-Type: application/json" -X POST \
  "http://localhost:8082/v1/tools/call" \
  -d '{"tool": "ruckus.zones.get_wlans", "args": {"zone_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890"}}' | jq
```

### Get Zone Statistics
```bash
curl -s -H "Content-Type: application/json" -X POST \
  "http://localhost:8082/v1/tools/call" \
  -d '{"tool": "ruckus.monitoring.get_zone_statistics", "args": {"zone_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890"}}' | jq
```

## Tips

- Note zone IDs for subsequent zone-specific operations
- Use pagination for deployments with many zones
- Empty zones (apCount=0) may indicate configuration issues
- High clientCount relative to apCount suggests capacity issues
- Zone names typically reflect building/floor/department structure

## Common Zone Patterns

### Campus Building
```
Name: "Building-A-Zone"
Description: "Building A wireless coverage"
AP Count: 15-30 per floor
```

### Guest Network
```
Name: "Guest-Zone"
Description: "Guest and visitor access"
AP Count: Lower density, public areas
```

### Department/VLAN
```
Name: "Finance-Zone"
Description: "Finance department secure zone"
AP Count: Office density, specific VLAN
```

## Related Examples

- [02 - Create Guest WLAN](02_create_guest_wlan.md)
- [03 - Monitor Access Points](03_monitor_access_points.md)
- [07 - Network Configuration](07_network_configuration.md)
