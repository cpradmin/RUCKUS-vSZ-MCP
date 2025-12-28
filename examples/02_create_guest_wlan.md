# ruckus.wlans.create - Create Guest WLAN

## Purpose

Create new wireless network (WLAN/SSID) with specified security settings. Supports Open, WPA2, WPA3 authentication types with various encryption methods. Essential for deploying guest networks, corporate SSIDs, or IoT wireless segments.

## When to Use

- Deploying guest wireless networks
- Creating event-specific temporary SSIDs
- Setting up BYOD or contractor networks
- Configuring IoT device networks
- Establishing secure corporate wireless
- Creating isolated wireless segments

## Use Case

**Scenario**: Company needs guest Wi-Fi for visitors and contractors with WPA2 security, isolated on VLAN 100, with simple passphrase that changes monthly.

**User Prompt**: "Create guest WLAN 'CompanyGuest' with WPA2-PSK security using password 'Welcome2024' on VLAN 100"

## Request

### WPA2-PSK Guest Network

```bash
curl -s \
  -H "Content-Type: application/json" \
  -X POST "http://localhost:8082/v1/tools/call" \
  -d '{
    "context": {
      "subject": "wireless-admin@company.com",
      "correlation_id": "guest-wifi-deployment-2024"
    },
    "tool": "ruckus.wlans.create",
    "args": {
      "zone_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
      "name": "Guest-WiFi",
      "ssid": "CompanyGuest",
      "authentication_type": "WPA2",
      "encryption_method": "AES",
      "passphrase": "Welcome2024",
      "vlan_id": 100,
      "description": "Guest and visitor wireless network"
    }
  }' | jq
```

### Open Network (No Security)

```bash
curl -s \
  -H "Content-Type: application/json" \
  -X POST "http://localhost:8082/v1/tools/call" \
  -d '{
    "tool": "ruckus.wlans.create",
    "args": {
      "zone_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
      "name": "Open-Guest",
      "ssid": "FreeWiFi",
      "authentication_type": "Open",
      "description": "Open public Wi-Fi"
    }
  }' | jq
```

### WPA3-Personal (Most Secure)

```bash
curl -s \
  -H "Content-Type: application/json" \
  -X POST "http://localhost:8082/v1/tools/call" \
  -d '{
    "tool": "ruckus.wlans.create",
    "args": {
      "zone_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
      "name": "Corporate-Secure",
      "ssid": "CompanyCorp",
      "authentication_type": "WPA3",
      "encryption_method": "AES",
      "passphrase": "SecurePass2024!",
      "vlan_id": 10,
      "description": "Corporate WPA3 network"
    }
  }' | jq
```

### Arguments

- **zone_id** (required): Target zone UUID
  - Get from `ruckus.zones.list`
- **name** (required): WLAN identifier name
  - Internal name, not broadcasted
  - Format: alphanumeric, hyphens
- **ssid** (required): Broadcasted SSID name
  - What users see when scanning
  - Max 32 characters
  - Avoid special characters
- **authentication_type** (optional): Security type
  - `Open`: No password (default)
  - `WPA2`: WPA2-Personal/PSK
  - `WPA3`: WPA3-Personal (most secure)
  - `WPA23Mixed`: WPA2/WPA3 transition mode
- **encryption_method** (optional): Encryption algorithm
  - `AES`: Advanced Encryption (recommended)
  - `TKIP`: Legacy devices only
  - `Auto`: Automatic selection
- **passphrase** (optional): Wi-Fi password
  - Required for WPA2/WPA3
  - 8-63 characters
  - Complex passwords recommended
- **vlan_id** (optional): VLAN assignment
  - Isolates traffic to specific VLAN
  - Recommended for guest networks
- **description** (optional): Purpose description
  - Max 255 characters

## Expected Response

### Success

```json
{
  "status": "ok",
  "data": {
    "result": "{\n  \"id\": \"f1e2d3c4-b5a6-7890-cdef-123456789abc\",\n  \"name\": \"Guest-WiFi\",\n  \"ssid\": \"CompanyGuest\",\n  \"zoneId\": \"a1b2c3d4-e5f6-7890-abcd-ef1234567890\",\n  \"status\": \"Disabled\",\n  \"authServiceOrProfile\": {\n    \"authType\": \"Open\"\n  }\n}"
  },
  "meta": {
    "tool": "ruckus.wlans.create"
  }
}
```

### Error - SSID Already Exists

```json
{
  "status": "error",
  "error": {
    "code": "api_error",
    "message": "WLAN with this SSID already exists in zone"
  },
  "meta": {
    "tool": "ruckus.wlans.create"
  }
}
```

### Error - Invalid Passphrase

```json
{
  "status": "error",
  "error": {
    "code": "api_error",
    "message": "Passphrase must be 8-63 characters"
  },
  "meta": {
    "tool": "ruckus.wlans.create"
  }
}
```

## Post-Creation Actions

### Enable the WLAN

```bash
curl -s -H "Content-Type: application/json" -X POST \
  "http://localhost:8082/v1/tools/call" \
  -d '{
    "tool": "ruckus.wlans.enable",
    "args": {
      "zone_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
      "wlan_id": "f1e2d3c4-b5a6-7890-cdef-123456789abc"
    }
  }' | jq
```

### Verify WLAN Configuration

```bash
curl -s -H "Content-Type: application/json" -X POST \
  "http://localhost:8082/v1/tools/call" \
  -d '{
    "tool": "ruckus.wlans.get",
    "args": {
      "zone_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
      "wlan_id": "f1e2d3c4-b5a6-7890-cdef-123456789abc"
    }
  }' | jq
```

### Monitor WLAN Usage

```bash
curl -s -H "Content-Type: application/json" -X POST \
  "http://localhost:8082/v1/tools/call" \
  -d '{
    "tool": "ruckus.monitoring.get_wlan_statistics",
    "args": {
      "zone_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
      "wlan_id": "f1e2d3c4-b5a6-7890-cdef-123456789abc"
    }
  }' | jq
```

## WLAN Deployment Workflow

1. **Plan WLAN**
   - Choose SSID name
   - Select security type
   - Assign VLAN
   - Define access policies

2. **Create WLAN** (this tool)
   - Specify all parameters
   - WLAN created but disabled

3. **Enable WLAN**
   - Use `ruckus.wlans.enable`
   - Broadcasts SSID

4. **Test Connectivity**
   - Connect test device
   - Verify VLAN assignment
   - Check internet access

5. **Monitor**
   - Track client count
   - Monitor performance
   - Review alarms

## Security Recommendations

### Guest Networks
- Use WPA2 minimum (WPA3 preferred)
- Isolate on dedicated VLAN (100-199)
- Enable client isolation
- Set bandwidth limits
- Use captive portal if needed

### Corporate Networks
- Use WPA3 or WPA2-Enterprise
- Assign to corporate VLAN
- Integrate with RADIUS
- Enable 802.1X authentication
- Strong, complex passphrases

### IoT Networks
- Use WPA2-PSK
- Dedicated VLAN (separate from corporate)
- Restrict internet access if possible
- Monitor unusual traffic patterns

## Common WLAN Patterns

### Guest/Visitor
```json
{
  "name": "Guest-WiFi",
  "ssid": "CompanyGuest",
  "authentication_type": "WPA2",
  "vlan_id": 100
}
```

### Corporate
```json
{
  "name": "Corporate-Wireless",
  "ssid": "CompanyCorp",
  "authentication_type": "WPA3",
  "vlan_id": 10
}
```

### IoT Devices
```json
{
  "name": "IoT-Network",
  "ssid": "Company-IoT",
  "authentication_type": "WPA2",
  "vlan_id": 50
}
```

### Temporary Event
```json
{
  "name": "Conference-2024",
  "ssid": "CompanyEvent",
  "authentication_type": "Open",
  "description": "Temporary network for annual conference"
}
```

## Tips

- **Always disable WLAN first**: Created WLANs are disabled by default
- **Test before production**: Enable on single AP first
- **Use descriptive names**: Include purpose in WLAN name
- **Document passphrases**: Store securely for help desk
- **Plan VLAN strategy**: Consistent VLAN numbering across zones
- **Monitor after deployment**: Watch for connection issues
- **Regular passphrase rotation**: Change guest passwords monthly
- **Verify SSID visibility**: Some devices may not see certain SSIDs

## Related Examples

- [01 - List Zones](01_list_zones.md)
- [06 - WLAN Management](06_wlan_management.md)
- [07 - Network Configuration](07_network_configuration.md)
