# ruckus.aps.get - Monitor Access Point Status

## Purpose

Retrieve detailed status and configuration of specific access point by MAC address. Essential for troubleshooting, monitoring AP health, and verifying deployment. Provides comprehensive information including connection status, firmware, model, location, and operational metrics.

## When to Use

- Troubleshooting AP connectivity issues
- Verifying AP deployment and configuration
- Monitoring AP health and performance
- Validating firmware versions
- Confirming GPS/location settings
- Investigating client connectivity problems
- Pre-maintenance AP inspection

## Use Case

**Scenario**: Help desk receives reports of poor Wi-Fi in Building A, 2nd floor. Network engineer needs complete status of AP 12:34:56:78:90:AB including connected clients, signal strength, and any alarms.

**User Prompt**: "Show me complete status and details of access point 12:34:56:78:90:AB"

## Request

### Get AP Details

```bash
curl -s \
  -H "Content-Type: application/json" \
  -X POST "http://localhost:8082/v1/tools/call" \
  -d '{
    "context": {
      "subject": "network-ops@company.com",
      "correlation_id": "ap-troubleshooting-2024"
    },
    "tool": "ruckus.aps.get",
    "args": {
      "ap_mac": "12:34:56:78:90:AB"
    }
  }' | jq
```

### Arguments

- **ap_mac** (required): AP MAC address
  - Format: "12:34:56:78:90:AB" or "12-34-56-78-90-AB"
  - Case insensitive
  - Must be exact match
  - Get from `ruckus.aps.list` or physical label

## Expected Response

### Success - Online AP

```json
{
  "status": "ok",
  "data": {
    "result": "{\n  \"mac\": \"12:34:56:78:90:AB\",\n  \"name\": \"Building-A-Floor-2-AP-01\",\n  \"model\": \"R750\",\n  \"serial\": \"521900001234\",\n  \"status\": \"Online\",\n  \"zoneName\": \"Campus-Zone\",\n  \"zoneId\": \"a1b2c3d4-e5f6-7890-abcd-ef1234567890\",\n  \"location\": \"Building A, 2nd Floor, Main Corridor\",\n  \"latitude\": 37.7749,\n  \"longitude\": -122.4194,\n  \"ipAddress\": \"10.0.1.50\",\n  \"ipType\": \"Static\",\n  \"gateway\": \"10.0.1.1\",\n  \"firmwareVersion\": \"6.1.2.0.398\",\n  \"uptime\": \"15d 7h 23m\",\n  \"connectionState\": \"Connect\",\n  \"registrationState\": \"Approved\",\n  \"provisionMethod\": \"Controller\",\n  \"connectedClients\": 15,\n  \"radio24\": {\n    \"channel\": 6,\n    \"channelWidth\": \"20MHz\",\n    \"txPower\": \"17dBm\"\n  },\n  \"radio5\": {\n    \"channel\": 36,\n    \"channelWidth\": \"80MHz\",\n    \"txPower\": \"20dBm\"\n  }\n}"
  },
  "meta": {
    "tool": "ruckus.aps.get"
  }
}
```

### Response Fields

**Identity**
- **mac**: AP MAC address (unique identifier)
- **name**: Friendly AP name
- **model**: AP model (R750, R650, etc.)
- **serial**: Serial number

**Status**
- **status**: Online/Offline/Rebooting/Flagged
- **connectionState**: Connect/Disconnect
- **registrationState**: Approved/Pending
- **uptime**: Time since last reboot

**Network Configuration**
- **ipAddress**: Current IP address
- **ipType**: Static/DHCP
- **gateway**: Default gateway
- **zoneName**: Assigned zone name
- **zoneId**: Zone UUID

**Location**
- **location**: Text description
- **latitude**: GPS latitude
- **longitude**: GPS longitude

**Radio Settings**
- **radio24**: 2.4GHz radio config (channel, power, width)
- **radio5**: 5GHz radio config

**Performance**
- **connectedClients**: Current client count
- **firmwareVersion**: Running firmware

### Offline AP

```json
{
  "status": "ok",
  "data": {
    "result": "{\n  \"mac\": \"12:34:56:78:90:AB\",\n  \"name\": \"Building-A-Floor-2-AP-01\",\n  \"status\": \"Offline\",\n  \"lastSeen\": \"2024-12-28T08:15:00Z\",\n  \"disconnectReason\": \"Lost connectivity\"\n}"
  }
}
```

### Error - AP Not Found

```json
{
  "status": "error",
  "error": {
    "code": "api_error",
    "message": "Access point not found"
  },
  "meta": {
    "tool": "ruckus.aps.get"
  }
}
```

## Related AP Operations

### List All APs

```bash
curl -s -H "Content-Type: application/json" -X POST \
  "http://localhost:8082/v1/tools/call" \
  -d '{"tool": "ruckus.aps.list", "args": {"list_size": 50}}' | jq
```

### Get AP Statistics

```bash
curl -s -H "Content-Type: application/json" -X POST \
  "http://localhost:8082/v1/tools/call" \
  -d '{"tool": "ruckus.monitoring.get_ap_statistics", "args": {"ap_mac": "12:34:56:78:90:AB"}}' | jq
```

### Get Connected Clients

```bash
curl -s -H "Content-Type: application/json" -X POST \
  "http://localhost:8082/v1/tools/call" \
  -d '{"tool": "ruckus.aps.get_clients", "args": {"ap_mac": "12:34:56:78:90:AB"}}' | jq
```

### Get Operational Info

```bash
curl -s -H "Content-Type: application/json" -X POST \
  "http://localhost:8082/v1/tools/call" \
  -d '{"tool": "ruckus.aps.get_operational_info", "args": {"ap_mac": "12:34:56:78:90:AB"}}' | jq
```

### Reboot AP

```bash
curl -s -H "Content-Type: application/json" -X POST \
  "http://localhost:8082/v1/tools/call" \
  -d '{"tool": "ruckus.aps.reboot", "args": {"ap_mac": "12:34:56:78:90:AB"}}' | jq
```

### Update AP Configuration

```bash
curl -s -H "Content-Type: application/json" -X POST \
  "http://localhost:8082/v1/tools/call" \
  -d '{
    "tool": "ruckus.aps.update",
    "args": {
      "ap_mac": "12:34:56:78:90:AB",
      "name": "Building-A-Floor-2-AP-01-Updated",
      "description": "Main corridor AP - North side",
      "location": "Building A, 2nd Floor, Main Corridor, North"
    }
  }' | jq
```

## Troubleshooting Workflow

### 1. Check Basic Status
```bash
# Get AP details
ruckus.aps.get → Check status, uptime, IP

# If offline, check last seen time
# If online but issues, proceed to step 2
```

### 2. Check Client Connectivity
```bash
# Get connected clients
ruckus.aps.get_clients → Verify client count

# Check client distribution
# Compare to expected load
```

### 3. Review Statistics
```bash
# Get performance metrics
ruckus.monitoring.get_ap_statistics → Check throughput, errors

# Review radio utilization
# Check for interference
```

### 4. Check for Alarms
```bash
# Get AP alarms
ruckus.alarms.list → Filter by AP MAC

# Review alarm history
# Identify patterns
```

### 5. Remediation Actions
```bash
# If needed, reboot AP
ruckus.aps.reboot

# Or update configuration
ruckus.aps.update

# Then verify resolution
ruckus.aps.get → Confirm status
```

## Status Indicators

### Connection States
- **Online**: AP connected and operational
- **Offline**: AP not reachable
- **Rebooting**: AP in restart process
- **Flagged**: AP has warnings/alerts
- **Heartbeat Lost**: Intermittent connectivity

### Registration States
- **Approved**: Fully authorized
- **Pending**: Awaiting approval
- **Rejected**: Authorization denied

### IP Types
- **Static**: Manually configured IP
- **DHCP**: Dynamic IP assignment
- **Zero Config**: Auto-discovery

## AP Model Reference

Common Ruckus AP models:
- **R750**: High-density indoor, Wi-Fi 6
- **R650**: Standard indoor, Wi-Fi 6
- **R550**: Entry indoor, Wi-Fi 5
- **T750**: Outdoor, Wi-Fi 6
- **H550**: Hospitality, Wi-Fi 6

## Tips

- **Save MAC address format**: Some systems use colons, others hyphens
- **Check uptime regularly**: Frequent reboots indicate issues
- **Monitor client count**: High counts suggest capacity needs
- **Verify firmware versions**: Keep consistent across deployment
- **Use GPS coordinates**: Helps with RF planning and coverage maps
- **Document locations**: Detailed descriptions aid troubleshooting
- **Note serial numbers**: Required for RMA/support cases
- **Check both radios**: 2.4GHz and 5GHz operate independently

## Common Issues and Checks

### AP Shows Offline
1. Check physical power/PoE
2. Verify network connectivity
3. Check switch port status
4. Review last disconnect reason

### High Client Count
1. Check for client issues
2. Review load distribution
3. Consider adding APs
4. Verify WLAN settings

### Firmware Mismatch
1. Note current version
2. Check zone firmware policy
3. Schedule upgrade if needed
4. Monitor post-upgrade

### Poor Performance
1. Review statistics
2. Check channel utilization
3. Look for interference
4. Verify radio power settings

## Related Examples

- [04 - Client Management](04_client_management.md)
- [05 - Alarm Management](05_alarm_management.md)
- [08 - Bulk AP Operations](08_bulk_ap_operations.md)
