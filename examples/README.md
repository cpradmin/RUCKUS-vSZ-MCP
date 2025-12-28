# Ruckus vSZ MCP Server - Usage Examples

Comprehensive real-world examples demonstrating Ruckus vSZ MCP Server capabilities. Each example includes purpose, use cases, complete curl requests with arguments, expected responses, and follow-up actions.

## 📚 Available Examples

### Core Operations

1. **[List Zones](01_list_zones.md)** - Zone inventory and management
   - Get wireless zone overview
   - Zone capacity analysis
   - Finding zone IDs for operations

2. **[Create Guest WLAN](02_create_guest_wlan.md)** - WLAN deployment
   - Guest network setup with WPA2/WPA3
   - Open networks
   - Security configuration

3. **[Monitor Access Points](03_monitor_access_points.md)** - AP health and status
   - Detailed AP information
   - Troubleshooting connectivity
   - Performance monitoring

4. **[Client Management](04_client_management.md)** - Connected clients
   - List active clients
   - Track client sessions
   - Disconnect unauthorized devices

5. **[Alarm Management](05_alarm_management.md)** - Proactive monitoring
   - Alarm summary by severity
   - Critical issue identification
   - Incident response

6. **[WLAN Management](06_wlan_management.md)** - WLAN updates
   - Password rotation
   - SSID changes
   - VLAN reassignment

## 🎯 Quick Reference

### By Task

**Network Discovery**
- List zones → Example 1
- List APs → Example 3
- List clients → Example 4

**Configuration**
- Create WLAN → Example 2
- Update WLAN → Example 6
- Configure VLANs → See Network Configuration

**Monitoring**
- AP status → Example 3
- Client tracking → Example 4
- Alarm monitoring → Example 5

**Security**
- Password rotation → Example 6
- Guest access → Example 2
- Client disconnect → Example 4

## 📖 Example Format

Each example follows this structure:

### Purpose
What the tool does and why it's useful

### When to Use
Specific scenarios and use cases

### Use Case
Real-world scenario with context

### Request
Complete curl command with arguments

### Arguments
Detailed parameter documentation

### Expected Response
Example responses (success and errors)

### Follow-up Actions
Related operations and next steps

### Tips
Best practices and recommendations

## 🚀 Getting Started

### Prerequisites

1. **Server Running**
   ```bash
   # Docker
   cd deploy && docker-compose up -d
   
   # Or Python
   ruckus-vsz-mcp-server
   ```

2. **Environment Configured**
   ```bash
   export RUCKUS_VSZ_URL="https://vsz.example.com:8443"
   export RUCKUS_VSZ_USERNAME="admin"
   export RUCKUS_VSZ_PASSWORD="your_password"
   ```

3. **Server Health Check**
   ```bash
   curl http://localhost:8082/healthz
   ```

### Running Examples

All examples use this base curl command:

```bash
curl -s \
  -H "Content-Type: application/json" \
  -X POST "http://localhost:8082/v1/tools/call" \
  -d '{
    "context": {
      "subject": "user@company.com",
      "correlation_id": "operation-id"
    },
    "tool": "ruckus.tool.name",
    "args": {
      "param": "value"
    }
  }' | jq
```

**Tips**:
- Install `jq` for formatted JSON output
- Use `-s` flag for silent curl (no progress bar)
- Set `correlation_id` for tracking operations
- Adjust `subject` for audit logging

## 🔧 Common Workflows

### Daily Operations

**Morning Health Check**
```bash
# 1. Get alarm summary
ruckus.alarms.get_summary

# 2. Check critical zones
ruckus.zones.list

# 3. Verify AP count
ruckus.aps.list
```

**User Issue Troubleshooting**
```bash
# 1. Find client
ruckus.clients.query (by hostname)

# 2. Check client status
ruckus.clients.get

# 3. Check connected AP
ruckus.aps.get

# 4. Review alarms
ruckus.alarms.list
```

### Scheduled Maintenance

**Monthly Guest Password Rotation**
```bash
# 1. List guest WLANs
ruckus.wlans.list

# 2. Update password
ruckus.wlans.update

# 3. Verify change
ruckus.wlans.get

# 4. Update documentation
```

**Firmware Updates**
```bash
# 1. List all APs
ruckus.aps.list

# 2. Check firmware versions
ruckus.aps.get (for each)

# 3. Plan upgrade window
# 4. Monitor post-upgrade
```

## 💡 Tips and Best Practices

### Tool Selection
- **List operations**: Use for inventory and discovery
- **Get operations**: Retrieve specific resource details
- **Query operations**: Advanced filtering and search
- **Update operations**: Modify existing configurations
- **Create operations**: Deploy new resources

### Error Handling
```bash
# Check HTTP status
curl -w "\n%{http_code}\n" ...

# Validate before operations
# Check prerequisites (zone exists, etc.)
# Verify post-operation
```

### Performance
- **Use pagination**: `list_size` parameter
- **Specific queries**: Better than list + filter
- **Parallel operations**: Multiple zones simultaneously
- **Cache zone/WLAN IDs**: Avoid repeated lookups

### Security
- **Rotate credentials**: Regular password updates
- **Audit logs**: Track who did what
- **Least privilege**: Limited API user access
- **Secure storage**: Never commit credentials

## 📊 Response Formats

### Success Response
```json
{
  "status": "ok",
  "data": {
    "result": "<JSON data or message>"
  },
  "meta": {
    "tool": "ruckus.tool.name"
  }
}
```

### Error Response
```json
{
  "status": "error",
  "error": {
    "code": "api_error",
    "message": "Error description"
  },
  "meta": {
    "tool": "ruckus.tool.name"
  }
}
```

### Common Error Codes
- `api_error`: vSZ API returned error
- `unknown_tool`: Tool name incorrect
- `invalid_request`: Missing/invalid parameters
- `internal_error`: Server-side error

## 🔗 Additional Resources

### Documentation
- [Main README](../README.md)
- [Quick Start Guide](../QUICKSTART.md)
- [Deployment Guide](../deploy/README.md)
- [Tool Definitions](../ruckus_vsz_server/tool_definitions.py)

### API Reference
- [Ruckus vSZ API Documentation](https://docs.ruckuswireless.com/smartzone/7.1.1/)
- [MCP Protocol](https://modelcontextprotocol.io/)

### Support
- **Issues**: [GitHub Issues](https://github.com/rpoulard/RUCKUS-vSZ-MCP/issues)
- **Examples**: This directory
- **Questions**: Create GitHub issue

## 🎓 Learning Path

### Beginner
1. Read Example 1 (List Zones)
2. Try Example 3 (Monitor APs)
3. Experiment with Example 4 (Client List)

### Intermediate
4. Create guest network (Example 2)
5. Set up monitoring (Example 5)
6. Practice updates (Example 6)

### Advanced
7. Automate workflows
8. Integrate with monitoring systems
9. Build custom scripts

## 🤝 Contributing Examples

Have a useful example? Contributions welcome!

**Example Template**:
1. Clear purpose statement
2. Real-world use case
3. Complete curl commands
4. Expected responses
5. Follow-up actions
6. Best practices

**Submit**:
- Fork repository
- Add example file
- Update this README
- Submit pull request

---

**Note**: All examples assume server is running on `localhost:8082`. Adjust URL if different.

For questions or issues, please open a [GitHub Issue](https://github.com/rpoulard/RUCKUS-vSZ-MCP/issues).
