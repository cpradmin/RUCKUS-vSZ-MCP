# Changelog

All notable changes to the Ruckus vSZ MCP Server will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-12-28

### Initial Release 🎉

First stable release of Ruckus vSZ MCP Server - Complete Model Context Protocol integration for Ruckus Virtual SmartZone wireless controllers.

### Features

#### Core MCP Server
- FastAPI-based HTTP server with MCP protocol v1.0 support
- Session-based authentication with automatic token renewal
- Comprehensive error handling and logging
- Health check endpoint for monitoring
- 46 MCP tools covering complete Ruckus vSZ API v11_0

#### API Modules (9 modules)
- **System Module**: Controller information, licenses, inventory, cluster status
- **Zones Module**: Zone and domain management with full CRUD operations
- **WLANs Module**: WLAN/SSID lifecycle management (Open, WPA2, WPA3)
- **Access Points Module**: AP management, monitoring, configuration, reboot
- **Clients Module**: Connected client monitoring and management
- **Authentication Module**: RADIUS and Hotspot profile management
- **Network Module**: VLAN pools, QoS, ACL profiles
- **Monitoring Module**: Statistics and performance data collection
- **Alarms Module**: Alarm monitoring and acknowledgment

#### Tools Breakdown
- **System**: 5 tools (info, inventory, summary, licenses, cluster)
- **Zones**: 8 tools (list, get, create, update, delete, get APs/WLANs, domains)
- **WLANs**: 7 tools (list, get, create, update, delete, enable/disable)
- **Access Points**: 8 tools (list, get, update, delete, reboot, operational info, clients, query)
- **Clients**: 4 tools (list, get, disconnect, query)
- **Monitoring**: 4 tools (AP/WLAN/zone statistics, client count)
- **Alarms**: 4 tools (list, get, acknowledge, summary)
- **Authentication**: 3 tools (RADIUS profile management)
- **Network**: 3 tools (VLAN pools, QoS profiles)

#### Documentation
- Comprehensive README with feature overview and quick start
- Deployment guide for Docker and Python
- 6 detailed usage examples following best practices:
  1. List zones and network organization
  2. Create guest WLAN with WPA2/WPA3
  3. Monitor access point status and health
  4. Client management and monitoring
  5. Alarm monitoring and management
  6. WLAN configuration updates
- Complete API parameter documentation
- Examples include curl commands, expected responses, and workflows

#### Deployment
- Dockerfile for containerized deployment
- Docker Compose configuration with health checks
- Environment variable configuration
- Non-root container execution for security
- Configurable server port (default: 8082)

#### Security
- Session-based authentication with service tickets
- Automatic token renewal on expiration
- SSL/TLS support with configurable verification
- Secure credential storage via environment variables
- Docker secrets support ready

### API Coverage

Based on Ruckus SmartZone Public API v11_0 (compatible with vSZ 7.1.1+):
- ✅ System and controller management
- ✅ Zone and domain operations
- ✅ WLAN/SSID configuration and management
- ✅ Access point lifecycle management
- ✅ Client monitoring and control
- ✅ RADIUS authentication configuration
- ✅ Network services (VLAN, QoS, ACLs)
- ✅ Statistics and monitoring
- ✅ Alarm management
- ✅ Query and advanced search operations

### Technical Stack

#### Dependencies
- `mcp >= 1.1.0` - Model Context Protocol
- `requests >= 2.32.0` - HTTP client
- `pydantic >= 2.7` - Data validation
- `pydantic-settings >= 2.2` - Settings management
- `fastapi >= 0.110` - Web framework
- `uvicorn[standard] >= 0.24` - ASGI server

#### Requirements
- Python 3.11+ or Docker
- Ruckus vSZ controller (vSZ-E, vSZ-H, SZ144, SZ300)
- Admin credentials with API access
- Network connectivity to vSZ controller

### Project Structure
```
RUCKUS-vSZ-MCP/
├── ruckus_vsz_server/       # Main application (16 files)
│   ├── main.py              # FastAPI MCP server
│   ├── api_client.py        # Ruckus vSZ API client
│   ├── config.py            # Configuration management
│   ├── tools.py             # MCP tool implementations
│   ├── tool_definitions.py  # Tool metadata (46 tools)
│   └── modules/             # API modules (9 modules)
├── deploy/                  # Docker deployment
├── examples/                # Usage examples (6 examples)
├── README.md                # Main documentation
├── CHANGELOG.md             # This file
├── LICENSE                  # MIT License
├── pyproject.toml           # Package configuration
└── requirements.txt         # Python dependencies
```

### Compatibility

- **API Version**: v11_0
- **Tested with**: Ruckus SmartZone 7.1.1+
- **Controller Models**: vSZ-E, vSZ-H, SZ144, SZ300
- **Python**: 3.11, 3.12
- **Docker**: Latest stable

### Known Limitations

- Some advanced monitoring endpoints may not be available in all API versions
- Specific features may require controller licenses
- No caching of API responses (all calls are live)

### Future Enhancements

Planned for future releases:
- Additional authentication methods (OAuth, API keys)
- Prometheus metrics endpoint
- Advanced filtering and bulk operations
- Configuration backup/restore tools
- RF optimization and planning tools
- Extended monitoring capabilities
- Kubernetes deployment manifests
- Comprehensive test coverage

---

For detailed installation and usage instructions, see [README.md](README.md).

For usage examples, see [examples/](examples/).

For deployment guide, see [deploy/README.md](deploy/README.md).
