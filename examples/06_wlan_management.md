# ruckus.wlans.update - WLAN Management and Configuration

## Purpose

Update existing WLAN configuration including name, SSID, security settings, VLAN assignment, and operational parameters. Essential for maintaining wireless networks, implementing security updates, adjusting capacity, and responding to changing business requirements.

## When to Use

- Changing WLAN passwords (security rotation)
- Updating SSID broadcast names
- Modifying VLAN assignments
- Adjusting security settings
- Renaming WLANs for clarity
- Updating descriptions
- Implementing security policy changes
- Reconfiguring guest networks

## Use Case

**Scenario**: Security policy requires monthly password rotation for guest Wi-Fi. Network team needs to update guest WLAN passphrase and SSID name to reflect current month, then verify changes are applied.

**User Prompt**: "Update Guest-WiFi password to 'January2025!' and change SSID to 'CompanyGuest-Jan2025'"

## Request

### Update Password and SSID

```bash
curl -s \
  -H "Content-Type: application/json" \
  -X POST "http://localhost:8082/v1/tools/call" \
  -d '{
    "context": {
      "subject": "security@company.com",
      "correlation_id": "guest-wifi-january-update"
    },
    "tool": "ruckus.wlans.update",
    "args": {
      "zone_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
      "wlan_id": "f1e2d3c4-b5a6-7890-cdef-123456789abc",
      "ssid": "CompanyGuest-Jan2025",
      "description": "Guest network - January 2025 credentials"
    }
  }' | jq
```

### Update VLAN Assignment

```bash
curl -s \
  -H "Content-Type: application/json" \
  -X POST "http://localhost:8082/v1/tools/call" \
  -d '{
    "tool": "ruckus.wlans.update",
    "args": {
      "zone_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
      "wlan_id": "f1e2d3c4-b5a6-7890-cdef-123456789abc",
      "vlan_id": 150
    }
  }' | jq
```

### Rename WLAN

```bash
curl -s \
  -H "Content-Type: application/json" \
  -X POST "http://localhost:8082/v1/tools/call" \
  -d '{
    "tool": "ruckus.wlans.update",
    "args": {
      "zone_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
      "wlan_id": "f1e2d3c4-b5a6-7890-cdef-123456789abc",
      "name": "Guest-WiFi-2025",
      "description": "Updated guest network for 2025"
    }
  }' | jq
```

### Arguments

- **zone_id** (required): Zone UUID containing the WLAN
  - Get from `ruckus.zones.list`
- **wlan_id** (required): WLAN UUID to update
  - Get from `ruckus.wlans.list`
- **name** (optional): New WLAN internal name
  - Alphanumeric, hyphens allowed
  - Not broadcasted to users
- **ssid** (optional): New broadcasted SSID
  - What users see
  - Max 32 characters
  - Takes effect immediately
- **description** (optional): Updated description
  - Max 255 characters
  - For documentation

**Note**: Only provide fields you want to change. Omitted fields remain unchanged.

## Expected Response

### Success

```json
{
  "status": "ok",
  "data": {
    "result": "{\n  \"success\": true,\n  \"message\": \"WLAN updated successfully\"\n}"
  },
  "meta": {
    "tool": "ruckus.wlans.update"
  }
}
```

### Error - WLAN Not Found

```json
{
  "status": "error",
  "error": {
    "code": "api_error",
    "message": "WLAN not found"
  },
  "meta": {
    "tool": "ruckus.wlans.update"
  }
}
```

### Error - SSID Duplicate

```json
{
  "status": "error",
  "error": {
    "code": "api_error",
    "message": "SSID already exists in zone"
  }
}
```

## Pre-Update Checks

### Get Current Configuration

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

### List All WLANs in Zone

```bash
curl -s -H "Content-Type: application/json" -X POST \
  "http://localhost:8082/v1/tools/call" \
  -d '{
    "tool": "ruckus.wlans.list",
    "args": {
      "zone_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
    }
  }' | jq
```

## Post-Update Verification

### Verify Changes Applied

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

### Check Connected Clients

```bash
curl -s -H "Content-Type: application/json" -X POST \
  "http://localhost:8082/v1/tools/call" \
  -d '{
    "tool": "ruckus.clients.query",
    "args": {
      "filters": {
        "type": "SSID",
        "value": "CompanyGuest-Jan2025"
      }
    }
  }' | jq
```

## WLAN Update Workflows

### Password Rotation (Monthly)

1. **Schedule maintenance window**
   - Notify users of password change
   - Choose low-usage time

2. **Backup current config**
   - Document current password
   - Save WLAN configuration

3. **Update WLAN**
   ```bash
   # Update passphrase via encryption endpoint
   # Note: Password changes require encryption update
   ```

4. **Verify and communicate**
   - Test connectivity
   - Update help desk docs
   - Notify users of new password

### SSID Rename

1. **Plan transition**
   - Choose new SSID name
   - Decide on transition method

2. **Update SSID**
   ```bash
   ruckus.wlans.update → Change ssid field
   ```

3. **Monitor adoption**
   - Watch client counts
   - Verify reconnections

### VLAN Migration

1. **Verify new VLAN exists**
   - Check switch configuration
   - Test connectivity

2. **Update WLAN VLAN**
   ```bash
   ruckus.wlans.update → Change vlan_id
   ```

3. **Test and validate**
   - Connect test device
   - Verify correct VLAN
   - Check internet access
   - Test inter-VLAN routing

## WLAN Control Operations

### Disable WLAN

```bash
curl -s -H "Content-Type: application/json" -X POST \
  "http://localhost:8082/v1/tools/call" \
  -d '{
    "tool": "ruckus.wlans.disable",
    "args": {
      "zone_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
      "wlan_id": "f1e2d3c4-b5a6-7890-cdef-123456789abc"
    }
  }' | jq
```

### Enable WLAN

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

### Delete WLAN

```bash
curl -s -H "Content-Type: application/json" -X POST \
  "http://localhost:8082/v1/tools/call" \
  -d '{
    "tool": "ruckus.wlans.delete",
    "args": {
      "zone_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
      "wlan_id": "f1e2d3c4-b5a6-7890-cdef-123456789abc"
    }
  }' | jq
```

## Common Update Scenarios

### Guest Network Password Rotation
```json
{
  "ssid": "CompanyGuest-Jan2025",
  "description": "Guest network - January 2025"
}
```

### Corporate SSID Rebrand
```json
{
  "name": "Corporate-Wireless-New",
  "ssid": "CompanyCorp-Secure",
  "description": "Corporate wireless - rebranded"
}
```

### VLAN Segregation
```json
{
  "vlan_id": 200,
  "description": "Moved to isolated guest VLAN 200"
}
```

### Event-Specific Update
```json
{
  "ssid": "Conference-2025",
  "description": "Annual conference - temporary network"
}
```

## Best Practices

### Password Updates
- **Schedule off-hours**: Minimize user disruption
- **Complexity requirements**: 12+ chars, mixed case, numbers, symbols
- **Rotation frequency**: Monthly for guest, quarterly for corporate
- **Communication**: Notify users 24h in advance
- **Documentation**: Update help desk immediately

### SSID Changes
- **Test first**: Single AP test before full deployment
- **User notification**: Advance warning for corporate SSIDs
- **Help desk prep**: Provide connection instructions
- **Monitor adoption**: Track client reconnections

### VLAN Changes
- **Network validation**: Verify VLAN exists on switches
- **Test device**: Confirm connectivity before production
- **Routing check**: Verify inter-VLAN rules
- **Firewall updates**: Adjust policies if needed

## Tips

- **One change at a time**: Easier troubleshooting
- **Test after updates**: Verify with real device
- **Document changes**: Maintain change log
- **Backup configs**: Before major changes
- **Monitor post-change**: Watch for issues
- **Plan rollback**: Know how to revert
- **Communicate clearly**: Users, help desk, management
- **Off-peak updates**: Less impact

## Troubleshooting Updates

### Clients Not Reconnecting
- SSID visibility issues
- Check WLAN enabled status
- Verify AP association
- Review client device logs

### Authentication Failures After Update
- Incorrect new password
- Client cached old credentials
- RADIUS sync delays
- Certificate issues

### No Internet After VLAN Change
- Check VLAN trunking
- Verify DHCP on new VLAN
- Test default gateway
- Review firewall rules

## Related Examples

- [02 - Create Guest WLAN](02_create_guest_wlan.md)
- [07 - Network Configuration](07_network_configuration.md)
- [01 - List Zones](01_list_zones.md)