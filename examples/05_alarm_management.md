# ruckus.alarms.get_summary - Alarm Monitoring and Management

## Purpose

Retrieve alarm summary with counts by severity level and acknowledgment status. Essential for proactive network monitoring, identifying critical issues, tracking incident response, and maintaining network health. Provides at-a-glance view of network alerts.

## When to Use

- Daily network health checks
- Incident response and prioritization
- SLA compliance monitoring
- Root cause analysis preparation
- Maintenance planning
- Automated alerting workflows
- Performance trend analysis
- Executive status reporting

## Use Case

**Scenario**: Network Operations Center (NOC) team needs morning dashboard showing all active alarms by severity, prioritize critical issues for immediate attention, and generate daily incident report for management.

**User Prompt**: "Show me alarm summary with critical issues that need immediate attention"

## Request

### Get Alarm Summary

```bash
curl -s \
  -H "Content-Type: application/json" \
  -X POST "http://localhost:8082/v1/tools/call" \
  -d '{
    "context": {
      "subject": "noc@company.com",
      "correlation_id": "morning-alarm-check-2024"
    },
    "tool": "ruckus.alarms.get_summary",
    "args": {}
  }' | jq
```

### Arguments

- None required
- Returns complete summary of all active alarms

## Expected Response

### Summary with Multiple Alarms

```json
{
  "status": "ok",
  "data": {
    "result": "{\n  \"total\": 15,\n  \"bySeverity\": {\n    \"Critical\": 2,\n    \"Major\": 5,\n    \"Minor\": 6,\n    \"Warning\": 2\n  },\n  \"byStatus\": {\n    \"acknowledged\": 8,\n    \"unacknowledged\": 7\n  },\n  \"byType\": {\n    \"AP_DISCONNECTED\": 3,\n    \"HIGH_CLIENT_COUNT\": 2,\n    \"AUTHENTICATION_FAILURE\": 4,\n    \"INTERFERENCE_DETECTED\": 2,\n    \"FIRMWARE_MISMATCH\": 2,\n    \"LICENSE_EXPIRING\": 1,\n    \"LOW_MEMORY\": 1\n  },\n  \"recentCritical\": [\n    {\n      \"id\": \"alarm-uuid-1\",\n      \"severity\": \"Critical\",\n      \"type\": \"AP_DISCONNECTED\",\n      \"message\": \"Access Point 12:34:56:78:90:AB disconnected\",\n      \"timestamp\": \"2024-12-28T08:30:00Z\"\n    },\n    {\n      \"id\": \"alarm-uuid-2\",\n      \"severity\": \"Critical\",\n      \"type\": \"LOW_MEMORY\",\n      \"message\": \"Controller memory usage above 90%\",\n      \"timestamp\": \"2024-12-28T09:00:00Z\"\n    }\n  ]\n}"
  },
  "meta": {
    "tool": "ruckus.alarms.get_summary"
  }
}
```

### Response Fields

**Counts**
- **total**: Total active alarms
- **bySeverity**: Count per severity level
  - Critical: Immediate action required
  - Major: Significant impact
  - Minor: Limited impact
  - Warning: Informational

**Status**
- **acknowledged**: Alarms staff has reviewed
- **unacknowledged**: Requires attention

**Types**
- **byType**: Count per alarm category
- **recentCritical**: Latest critical alarms
  - id: Alarm UUID
  - severity: Alarm level
  - type: Alarm category
  - message: Description
  - timestamp: When occurred

### No Active Alarms

```json
{
  "status": "ok",
  "data": {
    "result": "{\n  \"total\": 0,\n  \"bySeverity\": {},\n  \"byStatus\": {\"acknowledged\": 0, \"unacknowledged\": 0}\n}"
  }
}
```

## Detailed Alarm Operations

### List All Alarms

```bash
curl -s -H "Content-Type: application/json" -X POST \
  "http://localhost:8082/v1/tools/call" \
  -d '{
    "tool": "ruckus.alarms.list",
    "args": {"list_size": 50}
  }' | jq
```

### Get Specific Alarm Details

```bash
curl -s -H "Content-Type: application/json" -X POST \
  "http://localhost:8082/v1/tools/call" \
  -d '{
    "tool": "ruckus.alarms.get",
    "args": {"alarm_id": "alarm-uuid-1"}
  }' | jq
```

### Expected Alarm Details

```json
{
  "status": "ok",
  "data": {
    "result": "{\n  \"id\": \"alarm-uuid-1\",\n  \"severity\": \"Critical\",\n  \"type\": \"AP_DISCONNECTED\",\n  \"category\": \"Access Point\",\n  \"message\": \"Access Point 12:34:56:78:90:AB disconnected\",\n  \"description\": \"AP lost connectivity to controller\",\n  \"apMac\": \"12:34:56:78:90:AB\",\n  \"apName\": \"Building-A-Floor-2-AP-01\",\n  \"zoneName\": \"Campus-Zone\",\n  \"timestamp\": \"2024-12-28T08:30:00Z\",\n  \"acknowledged\": false,\n  \"acknowledgedBy\": null,\n  \"acknowledgedAt\": null,\n  \"cleared\": false,\n  \"clearedAt\": null,\n  \"occurrenceCount\": 1,\n  \"lastOccurrence\": \"2024-12-28T08:30:00Z\"\n}"
  }
}
```

### Acknowledge an Alarm

```bash
curl -s -H "Content-Type: application/json" -X POST \
  "http://localhost:8082/v1/tools/call" \
  -d '{
    "tool": "ruckus.alarms.acknowledge",
    "args": {"alarm_id": "alarm-uuid-1"}
  }' | jq
```

## Alarm Severity Levels

### Critical
- **Impact**: Service outage or major degradation
- **Examples**: 
  - Multiple APs offline
  - Controller failure
  - Zero clients can connect
  - Complete zone down
- **Action**: Immediate response required
- **SLA**: < 15 minutes

### Major
- **Impact**: Significant service degradation
- **Examples**:
  - Single AP offline
  - High authentication failures
  - Zone over capacity
  - Firmware mismatch
- **Action**: Address within 1 hour
- **SLA**: < 1 hour

### Minor
- **Impact**: Limited degradation
- **Examples**:
  - AP restarted
  - Moderate interference
  - Client roaming issues
  - Config sync delay
- **Action**: Schedule maintenance
- **SLA**: < 4 hours

### Warning
- **Impact**: Informational, potential future issues
- **Examples**:
  - License approaching expiration
  - Memory usage elevated
  - Backup recommended
  - Update available
- **Action**: Plan preventive action
- **SLA**: Next maintenance window

## Common Alarm Types

### AP_DISCONNECTED
**Description**: Access point lost connection to controller

**Causes**:
- Network connectivity issue
- Power loss (PoE failure)
- AP hardware failure
- Switch port down

**Resolution**:
1. Check AP physical status
2. Verify switch port/PoE
3. Check network path to controller
4. Review AP logs
5. Replace if hardware failure

### HIGH_CLIENT_COUNT
**Description**: Zone or AP exceeded client threshold

**Causes**:
- Insufficient AP density
- Popular area (cafeteria, lobby)
- Event or meeting
- Poor AP distribution

**Resolution**:
1. Verify actual client count
2. Check for client issues
3. Load balance to other APs
4. Plan additional APs
5. Adjust client limits

### AUTHENTICATION_FAILURE
**Description**: High rate of authentication failures

**Causes**:
- Incorrect SSID password
- RADIUS server issues
- Certificate problems
- Client configuration issues

**Resolution**:
1. Check RADIUS server status
2. Verify SSID credentials
3. Review client error details
4. Check certificate validity
5. Test authentication manually

### INTERFERENCE_DETECTED
**Description**: RF interference detected on channel

**Causes**:
- Non-Wi-Fi interference (microwave, Bluetooth)
- Neighboring Wi-Fi networks
- Rogue APs
- Faulty equipment

**Resolution**:
1. Identify interference source
2. Change channel if persistent
3. Adjust power levels
4. Remove interference source
5. Enable DFS channels if needed

### FIRMWARE_MISMATCH
**Description**: AP firmware differs from zone policy

**Causes**:
- Manual AP upgrade
- Failed upgrade
- New AP added
- Policy change

**Resolution**:
1. Review zone firmware policy
2. Schedule coordinated upgrade
3. Monitor upgrade progress
4. Verify post-upgrade

### LICENSE_EXPIRING
**Description**: Controller license approaching expiration

**Causes**:
- Subscription renewal needed
- Expired payment method
- Administrative oversight

**Resolution**:
1. Check license expiration date
2. Contact Ruckus for renewal
3. Apply new license key
4. Verify license activation

### LOW_MEMORY
**Description**: Controller memory usage critical

**Causes**:
- Too many managed APs
- Memory leak
- Excessive logging
- Process issues

**Resolution**:
1. Review controller capacity
2. Check for memory leaks
3. Restart controller if safe
4. Plan controller upgrade
5. Review log settings

## Alarm Management Workflow

### 1. Morning Check
```bash
# Get summary
ruckus.alarms.get_summary

# Prioritize by severity
# Critical → Major → Minor → Warning
```

### 2. Review Details
```bash
# List all alarms
ruckus.alarms.list

# Get details for each critical
ruckus.alarms.get
```

### 3. Investigate
```bash
# Check affected resources
# Review related statistics
# Identify root cause
```

### 4. Acknowledge
```bash
# Acknowledge after review
ruckus.alarms.acknowledge

# Document actions taken
# Assign to technician if needed
```

### 5. Resolve and Monitor
```bash
# Take corrective action
# Verify resolution
# Monitor for recurrence
# Update procedures
```

## Automated Monitoring

### Alarm Thresholds
```python
summary = get_alarm_summary()

if summary['bySeverity']['Critical'] > 0:
    page_oncall_engineer()
    
if summary['total'] > 50:
    escalate_to_manager()
    
if summary['byStatus']['unacknowledged'] > 10:
    send_team_notification()
```

### Integration Examples
- Send to SIEM
- Create tickets in ServiceNow
- Post to Slack/Teams
- Email daily digest
- Update dashboards

## Tips

- **Check summary first thing**: Identify urgent issues quickly
- **Prioritize critical alarms**: Address before major/minor
- **Acknowledge promptly**: Shows alarm is being handled
- **Track unacknowledged count**: High count indicates overwhelm
- **Review alarm trends**: Recurring alarms need permanent fix
- **Document resolutions**: Build knowledge base
- **Set up alerting**: Don't rely on manual checks
- **Clean up old alarms**: Archive or clear resolved alarms

## Related Examples

- [03 - Monitor Access Points](03_monitor_access_points.md)
- [04 - Client Management](04_client_management.md)
- [08 - Bulk AP Operations](08_bulk_ap_operations.md)
