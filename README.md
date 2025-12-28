# Ruckus vSZ MCP Server

[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![MCP Compatible](https://img.shields.io/badge/MCP-Compatible-green.svg)](https://modelcontextprotocol.io/)
[![Docker](https://img.shields.io/badge/docker-ready-blue.svg)](https://www.docker.com/)

**Complete Model Context Protocol server for Ruckus Virtual SmartZone** - Professional wireless network management and automation through AI assistants.

Manage your entire Ruckus wireless infrastructure through natural language conversations with Claude or other MCP-compatible AI assistants.

## 🌟 Features

- **50+ Comprehensive Tools** - Complete Ruckus vSZ API coverage (API version v11_0)
- **9 Core Modules** - System, Zones, WLANs, Access Points, Clients, Authentication, Network, Monitoring, and Alarms
- **Natural Language Interface** - Interact with your wireless network through AI assistants
- **Production Ready** - Docker deployment, health checks, comprehensive logging, session management
- **Advanced Search** - Query APs and clients with powerful filters
- **Real-time Monitoring** - Statistics, alarms, and performance data
- **Complete Lifecycle Management** - Create, read, update, and delete operations for all resources

## 📑 Table of Contents

- [Quick Start](#-quick-start)
- [Installation](#-installation)
- [Usage Examples](#-usage-examples)
- [Available Tools](#-available-tools)
- [Configuration](#-configuration)
- [Deployment](#-deployment)
- [Development](#-development)

## 🚀 Quick Start

### Docker Deployment (Recommended)

```bash
# Clone repository
git clone https://github.com/0xEkho/RUCKUS-vSZ-MCP.git
cd RUCKUS-vSZ-MCP/deploy

# Configure credentials
cp .env.example .env
nano .env  # Add your Ruckus vSZ URL and credentials

# Start server
docker-compose up -d

# Verify health
curl http://localhost:8082/healthz
```

### Python Installation

```bash
# Install
pip install -e .

# Set environment variables
export RUCKUS_VSZ_URL="https://vsz.example.com:8443"
export RUCKUS_VSZ_USERNAME="admin"
export RUCKUS_VSZ_PASSWORD="your_password"

# Run server
ruckus-vsz-mcp-server
```

## 📥 Installation

### Prerequisites

- Python 3.11+ or Docker
- Ruckus Virtual SmartZone controller (vSZ-E, vSZ-H, SZ144, or SZ300)
- Valid admin credentials with API access

### Ruckus vSZ API Setup

The Ruckus vSZ API is enabled by default. You just need:
1. Admin credentials (username/password)
2. Network access to your vSZ controller (typically port 8443)
3. API version compatibility (this server uses v11_0 by default)

### From Source

```bash
git clone https://github.com/0xEkho/RUCKUS-vSZ-MCP.git
cd RUCKUS-vSZ-MCP
pip install -r requirements.txt
pip install -e .
```

## 💡 Usage Examples

### Example: List all zones

**Natural language (with Claude):**
> "Show me all wireless zones in the network"

**MCP Tool Call:**
```json
{
  "tool": "ruckus.zones.list",
  "args": {}
}
```

### Example: Create a new WLAN

**Natural language (with Claude):**
> "Create a guest Wi-Fi network called 'Guest-WiFi' with WPA2 security and password 'Welcome2024'"

**MCP Tool Call:**
```json
{
  "tool": "ruckus.wlans.create",
  "args": {
    "zone_id": "zone-uuid-here",
    "name": "Guest-WiFi",
    "ssid": "Guest-WiFi",
    "authentication_type": "WPA2",
    "encryption_method": "AES",
    "passphrase": "Welcome2024"
  }
}
```

### Example: Monitor access point status

**Natural language (with Claude):**
> "Show me statistics for access point with MAC address 12:34:56:78:90:AB"

**MCP Tool Call:**
```json
{
  "tool": "ruckus.monitoring.get_ap_statistics",
  "args": {
    "ap_mac": "12:34:56:78:90:AB"
  }
}
```

## 🛠️ Available Tools

### 50+ Comprehensive Tools

| Module | Tools | Description |
|--------|-------|-------------|
| **System** | 5 | System information, licenses, inventory, cluster status |
| **Zones** | 8 | Zone and domain management |
| **WLANs** | 7 | WLAN/SSID lifecycle management |
| **Access Points** | 8 | AP management, reboot, configuration |
| **Clients** | 4 | Connected client management and monitoring |
| **Monitoring** | 4 | Statistics and performance data |
| **Alarms** | 4 | Alarm management and summary |
| **Authentication** | 3 | RADIUS and authentication profiles |
| **Network** | 3 | VLAN pools, QoS, network services |

### Key Operations

**System**
- `ruckus.system.get_info` - Get system information
- `ruckus.system.get_licenses` - Get license information
- `ruckus.system.get_cluster_status` - Get cluster status

**Zones**
- `ruckus.zones.list` - List all zones
- `ruckus.zones.get` - Get zone details
- `ruckus.zones.create/update/delete` - Manage zones
- `ruckus.zones.get_aps` - List APs in zone
- `ruckus.zones.get_wlans` - List WLANs in zone

**WLANs**
- `ruckus.wlans.list` - List all WLANs
- `ruckus.wlans.create` - Create new WLAN/SSID
- `ruckus.wlans.update/delete` - Manage WLANs
- `ruckus.wlans.enable/disable` - Enable/disable WLAN

**Access Points**
- `ruckus.aps.list` - List all APs
- `ruckus.aps.get` - Get AP details
- `ruckus.aps.update` - Update AP configuration
- `ruckus.aps.reboot` - Reboot an AP
- `ruckus.aps.get_clients` - Get connected clients
- `ruckus.aps.query` - Advanced AP search

**Clients**
- `ruckus.clients.list` - List connected clients
- `ruckus.clients.get` - Get client details
- `ruckus.clients.disconnect` - Disconnect a client
- `ruckus.clients.query` - Advanced client search

**Monitoring**
- `ruckus.monitoring.get_ap_statistics` - AP statistics
- `ruckus.monitoring.get_wlan_statistics` - WLAN statistics
- `ruckus.monitoring.get_zone_statistics` - Zone statistics
- `ruckus.monitoring.get_active_client_count` - Active client count

**Alarms**
- `ruckus.alarms.list` - List all alarms
- `ruckus.alarms.get` - Get alarm details
- `ruckus.alarms.acknowledge` - Acknowledge alarm
- `ruckus.alarms.get_summary` - Alarm summary

## ⚙️ Configuration

### Environment Variables

```bash
# Required
RUCKUS_VSZ_URL=https://vsz.example.com:8443
RUCKUS_VSZ_USERNAME=admin
RUCKUS_VSZ_PASSWORD=your_password

# Optional
RUCKUS_VSZ_VERIFY_SSL=true
RUCKUS_VSZ_TIMEOUT=30
RUCKUS_VSZ_API_VERSION=v11_0
LOG_LEVEL=INFO
```

### Configuration File

Alternatively, use `config.yaml`:

```yaml
ruckus_vsz:
  url: "https://vsz.example.com:8443"
  username: "admin"
  password: "your_password"
  verify_ssl: true
  timeout: 30
  api_version: "v11_0"

server:
  host: "0.0.0.0"
  port: 8082
  log_level: "INFO"
```

### MCP Client Configuration

**Claude Desktop** (`~/Library/Application Support/Claude/claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "ruckus-vsz": {
      "command": "docker",
      "args": [
        "run", "-i", "--rm",
        "-e", "RUCKUS_VSZ_URL=https://vsz.example.com:8443",
        "-e", "RUCKUS_VSZ_USERNAME=admin",
        "-e", "RUCKUS_VSZ_PASSWORD=your_password",
        "ruckus-vsz-mcp-server"
      ]
    }
  }
}
```

Or with Python:

```json
{
  "mcpServers": {
    "ruckus-vsz": {
      "command": "python",
      "args": ["-m", "ruckus_vsz_server.main"],
      "env": {
        "RUCKUS_VSZ_URL": "https://vsz.example.com:8443",
        "RUCKUS_VSZ_USERNAME": "admin",
        "RUCKUS_VSZ_PASSWORD": "your_password"
      }
    }
  }
}
```

## 🐳 Deployment

### Docker Compose

```bash
cd deploy
cp .env.example .env
# Edit .env with your credentials
docker-compose up -d
```

### Docker Build

```bash
docker build -t ruckus-vsz-mcp-server -f deploy/Dockerfile .
docker run -d -p 8082:8082 \
  -e RUCKUS_VSZ_URL="https://vsz.example.com:8443" \
  -e RUCKUS_VSZ_USERNAME="admin" \
  -e RUCKUS_VSZ_PASSWORD="your_password" \
  ruckus-vsz-mcp-server
```

### Health Check

```bash
curl http://localhost:8082/healthz
```

## 🔧 Development

### Setup Development Environment

```bash
# Clone and install
git clone https://github.com/rpoulard/RUCKUS-vSZ-MCP.git
cd RUCKUS-vSZ-MCP
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
pip install -e ".[dev]"
```

### Run Tests

```bash
pytest tests/
pytest --cov=ruckus_vsz_server tests/
```

### Code Quality

```bash
# Format
black ruckus_vsz_server/
isort ruckus_vsz_server/

# Lint
ruff check ruckus_vsz_server/
mypy ruckus_vsz_server/
```

### Project Structure

```
RUCKUS-vSZ-MCP/
├── ruckus_vsz_server/       # Main application code
│   ├── main.py              # FastAPI server
│   ├── api_client.py        # Ruckus vSZ API client
│   ├── config.py            # Configuration management
│   ├── tools.py             # MCP tools implementation
│   ├── tool_definitions.py  # Tool metadata
│   └── modules/             # API modules (9 modules)
│       ├── system.py
│       ├── zones.py
│       ├── wlans.py
│       ├── access_points.py
│       ├── clients.py
│       ├── authentication.py
│       ├── network.py
│       ├── monitoring.py
│       └── alarms.py
├── deploy/                   # Docker deployment
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── .env.example
├── examples/                 # Usage examples
├── requirements.txt          # Python dependencies
├── pyproject.toml           # Package configuration
└── README.md                # This file
```

## 🔒 Security

- **Authentication**: Username/password-based with service ticket
- **Session Management**: Automatic re-authentication on token expiration
- **Transport**: HTTPS required for production
- **Environment**: Store credentials securely, never commit secrets
- **Docker**: Runs as non-root user
- **SSL Verification**: Enabled by default

## 📚 API Coverage

This server implements the Ruckus SmartZone Public API v11_0 (compatible with vSZ 7.1.1+):

- ✅ System and controller management
- ✅ Zone and domain management  
- ✅ WLAN/SSID configuration
- ✅ Access point management
- ✅ Client monitoring and management
- ✅ RADIUS and authentication
- ✅ VLAN and network services
- ✅ Statistics and monitoring
- ✅ Alarm management

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built for [Model Context Protocol](https://modelcontextprotocol.io/) by Anthropic
- Based on [Ruckus SmartZone Public API](https://docs.ruckuswireless.com/smartzone/)
- Inspired by [phpIPAM MCP](https://github.com/0xEkho/phpIPAM-MCP)

## 📞 Support

- **Documentation**: [Ruckus API Documentation](https://docs.ruckuswireless.com/smartzone/7.1.1/)
- **Issues**: [GitHub Issues](https://github.com/0xEkho/RUCKUS-vSZ-MCP/issues)

---

**Made with ❤️ for wireless network automation and AI-assisted Wi-Fi operations**
