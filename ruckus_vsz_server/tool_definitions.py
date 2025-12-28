"""Tool definitions for Ruckus vSZ MCP Server - Complete API coverage."""

from typing import Any, Dict, List, Tuple

# Each tool is defined as (name, description, parameters_schema)
TOOL_DEFINITIONS: List[Tuple[str, str, Dict[str, Any]]] = [
    # System Module Tools
    (
        "ruckus.system.get_info",
        "Get system information including version, model, and uptime",
        {"type": "object", "properties": {}, "required": []},
    ),
    (
        "ruckus.system.get_inventory",
        "Get system inventory information",
        {"type": "object", "properties": {}, "required": []},
    ),
    (
        "ruckus.system.get_summary",
        "Get system summary with statistics",
        {"type": "object", "properties": {}, "required": []},
    ),
    (
        "ruckus.system.get_licenses",
        "Get license information",
        {"type": "object", "properties": {}, "required": []},
    ),
    (
        "ruckus.system.get_cluster_status",
        "Get cluster status information",
        {"type": "object", "properties": {}, "required": []},
    ),
    
    # Zones Module Tools
    (
        "ruckus.zones.list",
        "List all zones with optional pagination",
        {
            "type": "object",
            "properties": {
                "index": {"type": "integer", "description": "Starting index for pagination"},
                "list_size": {"type": "integer", "description": "Number of items to return"},
            },
            "required": [],
        },
    ),
    (
        "ruckus.zones.get",
        "Get zone details by UUID",
        {
            "type": "object",
            "properties": {
                "zone_id": {"type": "string", "description": "Zone UUID"},
            },
            "required": ["zone_id"],
        },
    ),
    (
        "ruckus.zones.create",
        "Create a new zone",
        {
            "type": "object",
            "properties": {
                "name": {"type": "string", "description": "Zone name"},
                "description": {"type": "string", "description": "Zone description"},
                "domain_id": {"type": "string", "description": "Domain UUID"},
            },
            "required": ["name"],
        },
    ),
    (
        "ruckus.zones.update",
        "Update zone configuration",
        {
            "type": "object",
            "properties": {
                "zone_id": {"type": "string", "description": "Zone UUID"},
                "name": {"type": "string", "description": "New zone name"},
                "description": {"type": "string", "description": "New zone description"},
            },
            "required": ["zone_id"],
        },
    ),
    (
        "ruckus.zones.delete",
        "Delete a zone",
        {
            "type": "object",
            "properties": {
                "zone_id": {"type": "string", "description": "Zone UUID"},
            },
            "required": ["zone_id"],
        },
    ),
    (
        "ruckus.zones.get_aps",
        "Get access points in a zone",
        {
            "type": "object",
            "properties": {
                "zone_id": {"type": "string", "description": "Zone UUID"},
                "index": {"type": "integer", "description": "Starting index for pagination"},
                "list_size": {"type": "integer", "description": "Number of items to return"},
            },
            "required": ["zone_id"],
        },
    ),
    (
        "ruckus.zones.get_wlans",
        "Get WLANs in a zone",
        {
            "type": "object",
            "properties": {
                "zone_id": {"type": "string", "description": "Zone UUID"},
            },
            "required": ["zone_id"],
        },
    ),
    (
        "ruckus.zones.list_domains",
        "List all domains",
        {"type": "object", "properties": {}, "required": []},
    ),
    
    # WLANs Module Tools
    (
        "ruckus.wlans.list",
        "List WLANs in a zone",
        {
            "type": "object",
            "properties": {
                "zone_id": {"type": "string", "description": "Zone UUID"},
                "index": {"type": "integer", "description": "Starting index for pagination"},
                "list_size": {"type": "integer", "description": "Number of items to return"},
            },
            "required": ["zone_id"],
        },
    ),
    (
        "ruckus.wlans.get",
        "Get WLAN details",
        {
            "type": "object",
            "properties": {
                "zone_id": {"type": "string", "description": "Zone UUID"},
                "wlan_id": {"type": "string", "description": "WLAN UUID"},
            },
            "required": ["zone_id", "wlan_id"],
        },
    ),
    (
        "ruckus.wlans.create",
        "Create a new WLAN/SSID",
        {
            "type": "object",
            "properties": {
                "zone_id": {"type": "string", "description": "Zone UUID"},
                "name": {"type": "string", "description": "WLAN name"},
                "ssid": {"type": "string", "description": "SSID broadcast name"},
                "authentication_type": {"type": "string", "description": "Authentication type (Open, WPA2, WPA3)", "default": "Open"},
                "encryption_method": {"type": "string", "description": "Encryption method (AES, TKIP)"},
                "passphrase": {"type": "string", "description": "WPA passphrase"},
                "vlan_id": {"type": "integer", "description": "VLAN ID"},
                "description": {"type": "string", "description": "WLAN description"},
            },
            "required": ["zone_id", "name", "ssid"],
        },
    ),
    (
        "ruckus.wlans.update",
        "Update WLAN configuration",
        {
            "type": "object",
            "properties": {
                "zone_id": {"type": "string", "description": "Zone UUID"},
                "wlan_id": {"type": "string", "description": "WLAN UUID"},
                "name": {"type": "string", "description": "New WLAN name"},
                "ssid": {"type": "string", "description": "New SSID"},
                "description": {"type": "string", "description": "New description"},
            },
            "required": ["zone_id", "wlan_id"],
        },
    ),
    (
        "ruckus.wlans.delete",
        "Delete a WLAN",
        {
            "type": "object",
            "properties": {
                "zone_id": {"type": "string", "description": "Zone UUID"},
                "wlan_id": {"type": "string", "description": "WLAN UUID"},
            },
            "required": ["zone_id", "wlan_id"],
        },
    ),
    (
        "ruckus.wlans.enable",
        "Enable a WLAN",
        {
            "type": "object",
            "properties": {
                "zone_id": {"type": "string", "description": "Zone UUID"},
                "wlan_id": {"type": "string", "description": "WLAN UUID"},
            },
            "required": ["zone_id", "wlan_id"],
        },
    ),
    (
        "ruckus.wlans.disable",
        "Disable a WLAN",
        {
            "type": "object",
            "properties": {
                "zone_id": {"type": "string", "description": "Zone UUID"},
                "wlan_id": {"type": "string", "description": "WLAN UUID"},
            },
            "required": ["zone_id", "wlan_id"],
        },
    ),
    
    # Access Points Module Tools
    (
        "ruckus.aps.list",
        "List all access points",
        {
            "type": "object",
            "properties": {
                "index": {"type": "integer", "description": "Starting index for pagination"},
                "list_size": {"type": "integer", "description": "Number of items to return"},
            },
            "required": [],
        },
    ),
    (
        "ruckus.aps.get",
        "Get AP details by MAC address",
        {
            "type": "object",
            "properties": {
                "ap_mac": {"type": "string", "description": "AP MAC address"},
            },
            "required": ["ap_mac"],
        },
    ),
    (
        "ruckus.aps.update",
        "Update AP configuration",
        {
            "type": "object",
            "properties": {
                "ap_mac": {"type": "string", "description": "AP MAC address"},
                "name": {"type": "string", "description": "AP name"},
                "description": {"type": "string", "description": "AP description"},
                "location": {"type": "string", "description": "Location description"},
                "latitude": {"type": "number", "description": "GPS latitude"},
                "longitude": {"type": "number", "description": "GPS longitude"},
            },
            "required": ["ap_mac"],
        },
    ),
    (
        "ruckus.aps.delete",
        "Remove AP from management",
        {
            "type": "object",
            "properties": {
                "ap_mac": {"type": "string", "description": "AP MAC address"},
            },
            "required": ["ap_mac"],
        },
    ),
    (
        "ruckus.aps.reboot",
        "Reboot an access point",
        {
            "type": "object",
            "properties": {
                "ap_mac": {"type": "string", "description": "AP MAC address"},
            },
            "required": ["ap_mac"],
        },
    ),
    (
        "ruckus.aps.get_operational_info",
        "Get AP operational information",
        {
            "type": "object",
            "properties": {
                "ap_mac": {"type": "string", "description": "AP MAC address"},
            },
            "required": ["ap_mac"],
        },
    ),
    (
        "ruckus.aps.get_clients",
        "Get clients connected to an AP",
        {
            "type": "object",
            "properties": {
                "ap_mac": {"type": "string", "description": "AP MAC address"},
            },
            "required": ["ap_mac"],
        },
    ),
    (
        "ruckus.aps.query",
        "Query APs with filters",
        {
            "type": "object",
            "properties": {
                "filters": {"type": "object", "description": "Filter criteria"},
                "full_text_search": {"type": "string", "description": "Search string"},
                "index": {"type": "integer", "description": "Starting index for pagination"},
                "list_size": {"type": "integer", "description": "Number of items to return"},
            },
            "required": [],
        },
    ),
    
    # Clients Module Tools
    (
        "ruckus.clients.list",
        "List all connected clients",
        {
            "type": "object",
            "properties": {
                "index": {"type": "integer", "description": "Starting index for pagination"},
                "list_size": {"type": "integer", "description": "Number of items to return"},
            },
            "required": [],
        },
    ),
    (
        "ruckus.clients.get",
        "Get client details by MAC address",
        {
            "type": "object",
            "properties": {
                "client_mac": {"type": "string", "description": "Client MAC address"},
            },
            "required": ["client_mac"],
        },
    ),
    (
        "ruckus.clients.disconnect",
        "Disconnect a client",
        {
            "type": "object",
            "properties": {
                "client_mac": {"type": "string", "description": "Client MAC address"},
            },
            "required": ["client_mac"],
        },
    ),
    (
        "ruckus.clients.query",
        "Query clients with filters",
        {
            "type": "object",
            "properties": {
                "filters": {"type": "object", "description": "Filter criteria"},
                "full_text_search": {"type": "string", "description": "Search string"},
                "index": {"type": "integer", "description": "Starting index for pagination"},
                "list_size": {"type": "integer", "description": "Number of items to return"},
            },
            "required": [],
        },
    ),
    
    # Monitoring Module Tools
    (
        "ruckus.monitoring.get_ap_statistics",
        "Get AP statistics",
        {
            "type": "object",
            "properties": {
                "ap_mac": {"type": "string", "description": "AP MAC address"},
            },
            "required": ["ap_mac"],
        },
    ),
    (
        "ruckus.monitoring.get_wlan_statistics",
        "Get WLAN statistics",
        {
            "type": "object",
            "properties": {
                "zone_id": {"type": "string", "description": "Zone UUID"},
                "wlan_id": {"type": "string", "description": "WLAN UUID"},
            },
            "required": ["zone_id", "wlan_id"],
        },
    ),
    (
        "ruckus.monitoring.get_zone_statistics",
        "Get zone statistics",
        {
            "type": "object",
            "properties": {
                "zone_id": {"type": "string", "description": "Zone UUID"},
            },
            "required": ["zone_id"],
        },
    ),
    (
        "ruckus.monitoring.get_active_client_count",
        "Get active client count",
        {"type": "object", "properties": {}, "required": []},
    ),
    
    # Alarms Module Tools
    (
        "ruckus.alarms.list",
        "List all alarms",
        {
            "type": "object",
            "properties": {
                "index": {"type": "integer", "description": "Starting index for pagination"},
                "list_size": {"type": "integer", "description": "Number of items to return"},
            },
            "required": [],
        },
    ),
    (
        "ruckus.alarms.get",
        "Get alarm details",
        {
            "type": "object",
            "properties": {
                "alarm_id": {"type": "string", "description": "Alarm UUID"},
            },
            "required": ["alarm_id"],
        },
    ),
    (
        "ruckus.alarms.acknowledge",
        "Acknowledge an alarm",
        {
            "type": "object",
            "properties": {
                "alarm_id": {"type": "string", "description": "Alarm UUID"},
            },
            "required": ["alarm_id"],
        },
    ),
    (
        "ruckus.alarms.get_summary",
        "Get alarm summary with counts by severity",
        {"type": "object", "properties": {}, "required": []},
    ),
    
    # Authentication Module Tools
    (
        "ruckus.authentication.list_radius_profiles",
        "List RADIUS authentication profiles",
        {
            "type": "object",
            "properties": {
                "zone_id": {"type": "string", "description": "Zone UUID"},
            },
            "required": ["zone_id"],
        },
    ),
    (
        "ruckus.authentication.get_radius_profile",
        "Get RADIUS profile details",
        {
            "type": "object",
            "properties": {
                "zone_id": {"type": "string", "description": "Zone UUID"},
                "profile_id": {"type": "string", "description": "RADIUS profile UUID"},
            },
            "required": ["zone_id", "profile_id"],
        },
    ),
    (
        "ruckus.authentication.create_radius_profile",
        "Create RADIUS authentication profile",
        {
            "type": "object",
            "properties": {
                "zone_id": {"type": "string", "description": "Zone UUID"},
                "name": {"type": "string", "description": "Profile name"},
                "primary_server": {"type": "string", "description": "Primary RADIUS server IP"},
                "primary_port": {"type": "integer", "description": "Primary server port", "default": 1812},
                "primary_shared_secret": {"type": "string", "description": "Primary server shared secret"},
            },
            "required": ["zone_id", "name", "primary_server", "primary_shared_secret"],
        },
    ),
    
    # Network Module Tools
    (
        "ruckus.network.list_vlan_pools",
        "List VLAN pools",
        {
            "type": "object",
            "properties": {
                "zone_id": {"type": "string", "description": "Zone UUID"},
            },
            "required": ["zone_id"],
        },
    ),
    (
        "ruckus.network.create_vlan_pool",
        "Create VLAN pool",
        {
            "type": "object",
            "properties": {
                "zone_id": {"type": "string", "description": "Zone UUID"},
                "name": {"type": "string", "description": "Pool name"},
                "vlan_list": {"type": "string", "description": "Comma-separated VLAN IDs (e.g., '10,20,30' or '10-20')"},
                "description": {"type": "string", "description": "Pool description"},
            },
            "required": ["zone_id", "name", "vlan_list"],
        },
    ),
    (
        "ruckus.network.list_qos_profiles",
        "List QoS profiles",
        {
            "type": "object",
            "properties": {
                "zone_id": {"type": "string", "description": "Zone UUID"},
            },
            "required": ["zone_id"],
        },
    ),
]
