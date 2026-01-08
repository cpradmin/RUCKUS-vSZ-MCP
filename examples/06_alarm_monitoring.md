# Alarm Monitoring

Monitor, list, and acknowledge network alarms.

## Tools

| Tool | Description |
|------|-------------|
| `ruckus.alarms.list` | List all alarms |
| `ruckus.alarms.get` | Get alarm details |
| `ruckus.alarms.get_summary` | Get alarm counts by severity |
| `ruckus.alarms.acknowledge` | Acknowledge an alarm |

---

## Get Alarm Summary

Quick overview of alarm counts by severity.

### curl

```bash
curl -s -X POST http://localhost:8082/v1/tools/call \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{"tool": "ruckus.alarms.get_summary", "args": {}}'
```

### Parameters

None required.

### Response

```json
{
  "summary": {
    "total": 147,
    "critical": 3,
    "major": 12,
    "minor": 45,
    "warning": 87
  }
}
```

---

## List Alarms

### curl

```bash
curl -s -X POST http://localhost:8082/v1/tools/call \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{"tool": "ruckus.alarms.list", "args": {}}'
```

### With Pagination

```bash
curl -s -X POST http://localhost:8082/v1/tools/call \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{"tool": "ruckus.alarms.list", "args": {"index": 0, "list_size": 50}}'
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
    "total": 147,
    "critical": 3,
    "major": 12,
    "minor": 45,
    "warning": 87,
    "has_more": true
  },
  "alarms": [
    {
      "id": "alarm-uuid-1",
      "type": "AP_DISCONNECT",
      "severity": "Critical",
      "message": "Access Point disconnected",
      "source": "AP",
      "source_name": "HQ-A-Floor2-AP05",
      "time": "2026-01-08T08:30:00Z",
      "acknowledged": false
    },
    {
      "id": "alarm-uuid-2",
      "type": "HIGH_CLIENT_COUNT",
      "severity": "Major",
      "message": "AP client count exceeded threshold",
      "source": "AP",
      "source_name": "Lobby-AP-03",
      "time": "2026-01-08T09:15:00Z",
      "acknowledged": true
    },
    {
      "id": "alarm-uuid-3",
      "type": "AUTH_FAILURE",
      "severity": "Minor",
      "message": "Multiple authentication failures detected",
      "source": "WLAN",
      "source_name": "CompanyGuest",
      "time": "2026-01-08T10:00:00Z",
      "acknowledged": false
    }
  ]
}
```

---

## Get Alarm Details

### curl

```bash
curl -s -X POST http://localhost:8082/v1/tools/call \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{"tool": "ruckus.alarms.get", "args": {"alarm_id": "alarm-uuid-1"}}'
```

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `alarm_id` | string | **Yes** | Alarm UUID |

### Response

```json
{
  "id": "alarm-uuid-1",
  "type": "AP_DISCONNECT",
  "severity": "Critical",
  "category": "Access Point",
  "message": "Access Point disconnected",
  "description": "AP lost connectivity to controller",
  "source": "AP",
  "source_name": "HQ-A-Floor2-AP05",
  "ap_mac": "AA:BB:CC:DD:EE:05",
  "zone": "HQ-Building-A",
  "time": "2026-01-08T08:30:00Z",
  "acknowledged": false,
  "occurrence_count": 1
}
```

---

## Acknowledge Alarm

Mark an alarm as reviewed.

### curl

```bash
curl -s -X POST http://localhost:8082/v1/tools/call \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{"tool": "ruckus.alarms.acknowledge", "args": {"alarm_id": "alarm-uuid-1"}}'
```

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `alarm_id` | string | **Yes** | Alarm UUID |

### Response

```json
{
  "status": "success",
  "message": "Alarm acknowledged"
}
```

---

## Alarm Severity Levels

| Severity | Impact | Action | SLA |
|----------|--------|--------|-----|
| Critical | Service outage | Immediate response | < 15 min |
| Major | Significant degradation | Address within 1 hour | < 1 hour |
| Minor | Limited impact | Schedule maintenance | < 4 hours |
| Warning | Informational | Plan preventive action | Next window |

---

## Common Alarm Types

| Type | Description | Resolution |
|------|-------------|------------|
| `AP_DISCONNECT` | AP lost connectivity | Check power/network |
| `HIGH_CLIENT_COUNT` | AP overloaded | Add APs or load balance |
| `AUTH_FAILURE` | Authentication issues | Check RADIUS/credentials |
| `INTERFERENCE` | RF interference | Change channel |
| `FIRMWARE_MISMATCH` | Version inconsistency | Schedule upgrade |
| `LICENSE_EXPIRING` | License near expiry | Renew license |

---

## Morning Health Check Workflow

1. Get alarm summary:
```bash
curl -s -X POST http://localhost:8082/v1/tools/call \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{"tool": "ruckus.alarms.get_summary", "args": {}}'
```

2. List critical/major alarms:
```bash
curl -s -X POST http://localhost:8082/v1/tools/call \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{"tool": "ruckus.alarms.list", "args": {"list_size": 20}}'
```

3. Investigate and acknowledge as needed.

---

## Integration Examples

### Alerting Script

```bash
#!/bin/bash
API_KEY="YOUR_API_KEY"
URL="http://localhost:8082/v1/tools/call"

# Get summary
SUMMARY=$(curl -s -X POST "$URL" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $API_KEY" \
  -d '{"tool": "ruckus.alarms.get_summary", "args": {}}')

# Extract critical count
CRITICAL=$(echo "$SUMMARY" | jq -r '.data.result | fromjson | .summary.critical')

if [ "$CRITICAL" -gt 0 ]; then
  echo "ALERT: $CRITICAL critical alarms!"
  # Send notification (email, Slack, PagerDuty, etc.)
fi
```

### Parse Response with jq

```bash
curl -s -X POST http://localhost:8082/v1/tools/call \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{"tool": "ruckus.alarms.list", "args": {"list_size": 10}}' \
  | jq -r '.data.result | fromjson | .alarms[] | select(.severity == "Critical") | .message'
```
