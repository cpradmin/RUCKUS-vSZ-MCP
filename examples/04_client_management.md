# ruckus.clients.list - Client Management and Monitoring

## Purpose

Retrieve list of all currently connected wireless clients with connection details. Essential for monitoring network usage, tracking device connectivity, troubleshooting user issues, and capacity planning. Provides real-time visibility into who is connected to the wireless network.

## When to Use

- Monitoring network usage and active connections
- Identifying unauthorized devices
- Troubleshooting specific client connectivity
- Generating usage reports and analytics
- Tracking guest access
- Verifying SSID assignments
- Capacity planning and load analysis
- Security audits and compliance

## Use Case

**Scenario**: Security team needs to audit all connected wireless devices, identify guests versus employees, track high-bandwidth users, and verify no unauthorized devices are connected during business hours.

**User Prompt**: "Show me all connected wireless clients with their hostnames, IP addresses, and which SSID they're using"

## Request

### List All Connected Clients

```bash
curl -s \
  -H "Content-Type: application/json" \
  -X POST "http://localhost:8082/v1/tools/call" \
  -d '{
    "context": {
      "subject": "security@company.com",
      "correlation_id": "client-audit-2024"
    },
    "tool": "ruckus.clients.list",
    "args": {
      "list_size": 100
    }
  }' | jq
```

### With Pagination

```bash
curl -s \
  -H "Content-Type: application/json" \
  -X POST "http://localhost:8082/v1/tools/call" \
  -d '{
    "tool": "ruckus.clients.list",
    "args": {
      "index": 0,
      "list_size": 50
    }
  }' | jq
```

### Arguments

- **index** (optional): Starting index for pagination
  - Default: 0
  - Use for large deployments
- **list_size** (optional): Number of clients to return
  - Default: 100
  - Maximum: 1000
  - Recommended: 50-100 for performance

## Expected Response

### Success with Multiple Clients

```json
{
  "status": "ok",
  "data": {
    "result": "{\n  \"list\": [\n    {\n      \"mac\": \"AA:BB:CC:DD:EE:FF\",\n      \"hostname\": \"iPhone-John\",\n      \"username\": \"john.doe\",\n      \"ipAddress\": \"192.168.1.100\",\n      \"ssid\": \"Corporate-WiFi\",\n      \"apMac\": \"12:34:56:78:90:AB\",\n      \"apName\": \"Building-A-Floor-2-AP-01\",\n      \"zoneName\": \"Campus-Zone\",\n      \"status\": \"Authorized\",\n      \"connectionTime\": \"2024-12-28T09:15:00Z\",\n      \"sessionDuration\": \"2h 45m\",\n      \"rssi\": \"-65 dBm\",\n      \"snr\": \"35 dB\",\n      \"channel\": \"36\",\n      \"radioType\": \"5GHz\",\n      \"dataRate\": \"866 Mbps\",\n      \"traffic\": {\n        \"txBytes\": 1048576,\n        \"rxBytes\": 5242880,\n        \"txPackets\": 1024,\n        \"rxPackets\": 5120\n      },\n      \"vlan\": 10,\n      \"role\": \"Employee\",\n      \"osType\": \"iOS\"\n    },\n    {\n      \"mac\": \"11:22:33:44:55:66\",\n      \"hostname\": \"LAPTOP-GUEST-05\",\n      \"ipAddress\": \"192.168.100.50\",\n      \"ssid\": \"Guest-WiFi\",\n      \"apMac\": \"12:34:56:78:90:CD\",\n      \"apName\": \"Lobby-AP-03\",\n      \"zoneName\": \"Guest-Zone\",\n      \"status\": \"Authorized\",\n      \"connectionTime\": \"2024-12-28T10:30:00Z\",\n      \"sessionDuration\": \"1h 15m\",\n      \"rssi\": \"-72 dBm\",\n      \"channel\": \"6\",\n      \"radioType\": \"2.4GHz\",\n      \"dataRate\": \"144 Mbps\",\n      \"vlan\": 100\n    }\n  ],\n  \"totalCount\": 245,\n  \"hasMore\": true\n}"
  },
  "meta": {
    "tool": "ruckus.clients.list"
  }
}
```

### Response Fields

**Client Identity**
- **mac**: Client MAC address (unique ID)
- **hostname**: Device hostname
- **username**: Authenticated username (if applicable)
- **osType**: Operating system (iOS, Android, Windows, etc.)

**Network Info**
- **ipAddress**: Assigned IP address
- **ssid**: Connected SSID name
- **vlan**: VLAN assignment
- **status**: Authorized/Unauthorized

**Connection Details**
- **apMac**: Connected AP MAC
- **apName**: Connected AP name
- **zoneName**: Zone name
- **connectionTime**: When connection started
- **sessionDuration**: How long connected

**Signal Quality**
- **rssi**: Signal strength (dBm)
- **snr**: Signal-to-noise ratio (dB)
- **channel**: Wi-Fi channel
- **radioType**: 2.4GHz or 5GHz
- **dataRate**: Current data rate (Mbps)

**Traffic Statistics**
- **txBytes**: Transmitted bytes
- **rxBytes**: Received bytes
- **txPackets**: Transmitted packets
- **rxPackets**: Received packets

### No Clients Connected

```json
{
  "status": "ok",
  "data": {
    "result": "{\n  \"list\": [],\n  \"totalCount\": 0\n}"
  }
}
```

## Advanced Client Queries

### Query Clients by SSID

```bash
curl -s -H "Content-Type: application/json" -X POST \
  "http://localhost:8082/v1/tools/call" \
  -d '{
    "tool": "ruckus.clients.query",
    "args": {
      "filters": {
        "type": "SSID",
        "value": "Guest-WiFi"
      },
      "list_size": 100
    }
  }' | jq
```

### Query Clients by AP

```bash
curl -s -H "Content-Type: application/json" -X POST \
  "http://localhost:8082/v1/tools/call" \
  -d '{
    "tool": "ruckus.clients.query",
    "args": {
      "filters": {
        "type": "AP_MAC",
        "value": "12:34:56:78:90:AB"
      }
    }
  }' | jq
```

### Search by Hostname

```bash
curl -s -H "Content-Type: application/json" -X POST \
  "http://localhost:8082/v1/tools/call" \
  -d '{
    "tool": "ruckus.clients.query",
    "args": {
      "full_text_search": "iPhone"
    }
  }' | jq
```

### Get Specific Client Details

```bash
curl -s -H "Content-Type: application/json" -X POST \
  "http://localhost:8082/v1/tools/call" \
  -d '{
    "tool": "ruckus.clients.get",
    "args": {
      "client_mac": "AA:BB:CC:DD:EE:FF"
    }
  }' | jq
```

## Client Management Actions

### Disconnect Client

```bash
curl -s -H "Content-Type: application/json" -X POST \
  "http://localhost:8082/v1/tools/call" \
  -d '{
    "tool": "ruckus.clients.disconnect",
    "args": {
      "client_mac": "AA:BB:CC:DD:EE:FF"
    }
  }' | jq
```

### Get Active Client Count

```bash
curl -s -H "Content-Type: application/json" -X POST \
  "http://localhost:8082/v1/tools/call" \
  -d '{"tool": "ruckus.monitoring.get_active_client_count"}' | jq
```

### Expected Count Response

```json
{
  "status": "ok",
  "data": {
    "result": "{\n  \"total\": 245,\n  \"bySSID\": [\n    {\"ssid\": \"Corporate-WiFi\", \"count\": 180},\n    {\"ssid\": \"Guest-WiFi\", \"count\": 65}\n  ],\n  \"byZone\": [\n    {\"zoneName\": \"Campus-Zone\", \"count\": 200},\n    {\"zoneName\": \"Guest-Zone\", \"count\": 45}\n  ]\n}"
  }
}
```

## Client Monitoring Workflows

### Daily Active User Audit
1. List all clients
2. Group by SSID
3. Identify guest vs employee
4. Check for unauthorized devices
5. Generate daily report

### Troubleshoot User Connection
1. Get client by MAC
2. Check signal strength (RSSI/SNR)
3. Verify AP connection
4. Review session history
5. Check for alarms

### Capacity Planning
1. Get client count by zone
2. Analyze peak usage times
3. Identify overloaded APs
4. Plan AP additions

### Security Incident Response
1. List all guests
2. Check for suspicious traffic
3. Identify unauthorized MACs
4. Disconnect if needed
5. Block repeat offenders

## Signal Quality Interpretation

### RSSI (Received Signal Strength Indicator)
- **-30 to -50 dBm**: Excellent
- **-50 to -60 dBm**: Good
- **-60 to -70 dBm**: Fair
- **-70 to -80 dBm**: Weak
- **Below -80 dBm**: Poor (disconnect likely)

### SNR (Signal-to-Noise Ratio)
- **40+ dB**: Excellent
- **25-40 dB**: Good
- **15-25 dB**: Fair
- **10-15 dB**: Poor
- **Below 10 dB**: Unusable

### Data Rates
- **800+ Mbps**: Excellent (Wi-Fi 6, 5GHz)
- **400-800 Mbps**: Good (Wi-Fi 5, 5GHz)
- **100-400 Mbps**: Fair
- **Below 100 Mbps**: Poor/congestion

## Client Statistics Analysis

### Traffic Patterns
```bash
# Sort by data usage
# Identify top consumers
# Check for anomalies
# Plan bandwidth allocation
```

### Connection Duration
```bash
# Average session length
# Frequent reconnections (indicates issues)
# Long-lived sessions (good coverage)
```

### Device Distribution
```bash
# Count by OS type
# Identify legacy devices
# Plan for compatibility
```

## Tips

- **Monitor RSSI/SNR**: Poor signal indicates coverage gaps
- **Track guest counts**: Plan capacity for events
- **Identify high-bandwidth users**: QoS policy adjustments
- **Check session duration**: Frequent reconnects = issues
- **Document unauthorized MACs**: Blacklist if needed
- **Monitor by SSID**: Validate VLAN assignments
- **Review peak times**: Plan maintenance windows
- **Use pagination**: Better performance on large networks

## Common Client Issues

### Client Can't Connect
1. Check if MAC is blocked
2. Verify SSID is enabled
3. Review authentication settings
4. Check VLAN configuration

### Poor Performance
1. Check RSSI/SNR
2. Verify data rate
3. Look for channel congestion
4. Consider AP placement

### Frequent Disconnects
1. Review signal strength
2. Check for roaming issues
3. Verify AP capacity
4. Look for interference

### High Bandwidth Usage
1. Identify client MAC
2. Check traffic patterns
3. Apply QoS if needed
4. Investigate for abuse

## Related Examples

- [03 - Monitor Access Points](03_monitor_access_points.md)
- [02 - Create Guest WLAN](02_create_guest_wlan.md)
- [05 - Alarm Management](05_alarm_management.md)
