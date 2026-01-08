"""LLM-friendly response formatters for Ruckus vSZ MCP Server.

These formatters transform raw API responses into concise, structured data
optimized for LLM consumption - removing nulls, extracting key fields,
and adding human-readable summaries.
"""

import json
from typing import Any, Dict, List, Optional


def _clean_nulls(data: Any) -> Any:
    """Recursively remove null/None values from dict/list."""
    if isinstance(data, dict):
        return {k: _clean_nulls(v) for k, v in data.items() if v is not None}
    elif isinstance(data, list):
        return [_clean_nulls(item) for item in data if item is not None]
    return data


def _to_json(data: Any) -> str:
    """Convert to compact JSON string."""
    return json.dumps(data, ensure_ascii=False, separators=(',', ':'))


# =============================================================================
# System Formatters
# =============================================================================

def format_system_info(data: Dict[str, Any]) -> str:
    """Format system info for LLM."""
    result = {
        "controller": {
            "name": data.get("clusterName") or data.get("hostName"),
            "model": data.get("model"),
            "version": data.get("version"),
            "serial": data.get("serialNumber"),
            "uptime": data.get("uptimeStr") or data.get("uptime"),
        },
        "network": {
            "management_ip": data.get("managementIp"),
            "control_ip": data.get("controlIp"),
            "cluster_ip": data.get("clusterIp"),
        }
    }
    return _to_json(_clean_nulls(result))


def format_system_summary(data: Dict[str, Any]) -> str:
    """Format system summary for LLM.
    
    Handles both dedicated summary endpoints and controller info fallback.
    """
    # Try to extract stats from various possible formats
    result = {
        "controller": {
            "name": data.get("clusterName") or data.get("hostName") or data.get("name"),
            "model": data.get("model"),
            "version": data.get("version"),
        },
        "totals": {
            "aps": data.get("totalAPs") or data.get("apTotal") or data.get("apCount"),
            "aps_online": data.get("connectedAPs") or data.get("apOnline") or data.get("onlineAPs"),
            "clients": data.get("totalClients") or data.get("clientTotal") or data.get("clientCount"),
            "zones": data.get("totalZones") or data.get("zoneTotal") or data.get("zoneCount"),
            "wlans": data.get("totalWlans") or data.get("wlanTotal") or data.get("wlanCount"),
        },
        "status": {
            "aps_offline": data.get("disconnectedAPs") or data.get("apOffline") or data.get("offlineAPs"),
            "alerts": data.get("totalAlerts") or data.get("alertTotal") or data.get("alertCount"),
        }
    }
    return _to_json(_clean_nulls(result))


def format_cluster_status(data: Dict[str, Any]) -> str:
    """Format cluster status for LLM.
    
    vSZ 6.x cluster/state returns:
    - clusterName, clusterState, clusterRole
    - currentNodeId, currentNodeName
    - nodeStateList: [{nodeId, nodeName, nodeState}, ...]
    """
    nodes = []
    
    # Try nodeStateList first (vSZ 6.x cluster/state format)
    node_list = data.get("nodeStateList", data.get("list", data.get("nodes", data.get("clusterNodes", []))))
    
    for node in node_list:
        node_info = {
            "name": node.get("nodeName") or node.get("name") or node.get("hostName"),
            "id": node.get("nodeId"),
            "state": node.get("nodeState") or node.get("state") or node.get("status"),
            "role": node.get("role") or node.get("clusterRole") or node.get("nodeRole"),
            "ip": node.get("managementIp") or node.get("ip") or node.get("controlIp"),
        }
        # Only add if we have at least a name or id
        if node_info.get("name") or node_info.get("id"):
            nodes.append(node_info)
    
    result = {
        "cluster": {
            "name": data.get("clusterName"),
            "state": data.get("clusterState") or data.get("state") or data.get("status"),
            "role": data.get("clusterRole"),
            "current_node": data.get("currentNodeName"),
        },
        "node_count": len(nodes) if nodes else data.get("totalCount"),
        "nodes": nodes if nodes else None
    }
    return _to_json(_clean_nulls(result))


def format_licenses(data: Dict[str, Any]) -> str:
    """Format license info for LLM.
    
    vSZ 6.x returns: name, description, count, expireDate, createTime
    """
    licenses = []
    raw_list = data.get("list", data.get("licenses", [data]))
    
    # Aggregate by license type
    aggregated: Dict[str, Dict[str, Any]] = {}
    for lic in raw_list:
        lic_name = lic.get("name") or lic.get("licenseType") or lic.get("type") or "Unknown"
        count = lic.get("count") or lic.get("capacity") or 0
        expiry = lic.get("expireDate") or lic.get("expirationDate") or lic.get("expiry")
        desc = lic.get("description", "")
        
        if lic_name in aggregated:
            aggregated[lic_name]["count"] += count
        else:
            aggregated[lic_name] = {
                "name": lic_name,
                "description": desc,
                "count": count,
                "expiry": expiry
            }
    
    # Convert to list
    for lic_data in aggregated.values():
        licenses.append({
            "type": lic_data["name"],
            "description": lic_data["description"][:50] if lic_data["description"] else None,
            "capacity": lic_data["count"],
            "expiry": lic_data["expiry"] if lic_data["expiry"] and not lic_data["expiry"].startswith("29227") else "Permanent",
        })
    
    # Calculate totals for AP licenses
    total_ap_capacity = sum(l["capacity"] for l in licenses if "AP" in (l.get("type") or ""))
    
    result = {
        "summary": {
            "license_types": len(licenses),
            "total_ap_capacity": total_ap_capacity if total_ap_capacity > 0 else None,
        },
        "licenses": licenses
    }
    return _to_json(_clean_nulls(result))


def format_system_inventory(data: Dict[str, Any]) -> str:
    """Format system inventory (zone stats) for LLM."""
    zones = []
    raw_list = data.get("list", [])
    
    total_aps = 0
    total_connected = 0
    total_disconnected = 0
    total_clients = 0
    
    for zone in raw_list:
        aps = zone.get("totalAPs", 0)
        connected = zone.get("connectedAPs", 0)
        disconnected = zone.get("disconnectedAPs", 0)
        clients = zone.get("clients", 0)
        
        total_aps += aps
        total_connected += connected
        total_disconnected += disconnected
        total_clients += clients
        
        zones.append({
            "name": zone.get("zoneName"),
            "aps": aps,
            "online": connected,
            "offline": disconnected,
            "clients": clients,
            "firmware": zone.get("apFirmwareVersion"),
        })
    
    result = {
        "summary": {
            "zones": len(zones),
            "total_aps": total_aps,
            "online_aps": total_connected,
            "offline_aps": total_disconnected,
            "total_clients": total_clients,
        },
        "zones": zones
    }
    return _to_json(_clean_nulls(result))


# =============================================================================
# Access Point Formatters
# =============================================================================

def format_ap_list(data: Dict[str, Any]) -> str:
    """Format AP list for LLM - concise summary with key fields only."""
    aps = []
    raw_list = data.get("list", [])
    
    # Count status
    online = offline = flagged = 0
    
    for ap in raw_list:
        status = (ap.get("status") or "Unknown").lower()
        if status == "online":
            online += 1
        elif status == "offline":
            offline += 1
        else:
            flagged += 1
        
        aps.append({
            "name": ap.get("deviceName") or ap.get("apName") or ap.get("name"),
            "mac": ap.get("apMac") or ap.get("mac"),
            "status": ap.get("status"),
            "ip": ap.get("ip") or ap.get("ipAddress"),
            "model": ap.get("model"),
            "zone": ap.get("zoneName"),
            "clients": ap.get("numClients") or ap.get("clientCount") or 0,
            "firmware": ap.get("firmwareVersion"),
        })
    
    result = {
        "summary": {
            "total": data.get("totalCount", len(aps)),
            "online": online,
            "offline": offline,
            "flagged": flagged,
            "has_more": data.get("hasMore", False),
        },
        "aps": aps
    }
    return _to_json(_clean_nulls(result))


def format_ap_detail(data: Dict[str, Any]) -> str:
    """Format single AP detail for LLM."""
    result = {
        "ap": {
            "name": data.get("deviceName") or data.get("name"),
            "mac": data.get("apMac") or data.get("mac"),
            "status": data.get("status") or data.get("connectionState"),
            "ip": data.get("ip") or data.get("ipAddress"),
            "model": data.get("model"),
            "serial": data.get("serial") or data.get("serialNumber"),
            "firmware": data.get("firmwareVersion"),
            "zone": data.get("zoneName"),
            "group": data.get("apGroupName"),
            "location": data.get("location"),
            "description": data.get("description"),
        },
        "radio": {
            "channel_2g": data.get("channel24G"),
            "channel_5g": data.get("channel5G"),
            "channel_6g": data.get("channel6G"),
        },
        "stats": {
            "clients": data.get("numClients") or 0,
            "uptime": data.get("uptime"),
            "last_seen": data.get("lastSeen"),
        }
    }
    return _to_json(_clean_nulls(result))


def format_ap_lldp_neighbors(data: Dict[str, Any]) -> str:
    """Format AP LLDP neighbors for LLM.
    
    Shows network devices discovered by the AP via LLDP protocol,
    including switches, phones, and other connected equipment.
    """
    neighbors = []
    raw_list = data.get("list", [])
    
    for neighbor in raw_list:
        neighbors.append({
            "ap_port": neighbor.get("lldpInterface"),  # AP's local port (eth0, eth4)
            "neighbor_name": neighbor.get("lldpSysName"),  # Remote device hostname
            "neighbor_desc": neighbor.get("lldpSysDesc"),  # Remote device description
            "neighbor_chassis": neighbor.get("lldpChassisID"),  # Remote chassis ID
            "neighbor_port": neighbor.get("lldpPortID"),  # Remote port ID
            "neighbor_port_desc": neighbor.get("lldpPortDesc"),  # Remote port description
            "neighbor_ip": neighbor.get("lldpMgmtIP"),  # Remote management IP
            "capabilities": neighbor.get("lldpCapability"),
            "uptime": neighbor.get("lldpTime"),
            "power_source": neighbor.get("lldpPowerSource"),
            "link_speed": neighbor.get("lldpMAUOperType"),
            "managed": neighbor.get("neighborManaged", False),
        })
    
    result = {
        "summary": {
            "total": data.get("totalCount", len(neighbors)),
            "returned": len(neighbors),
            "note": "Use EXACT neighbor_name and neighbor_ip values below - do not invent or modify"
        },
        "neighbors": neighbors
    }
    return _to_json(_clean_nulls(result))


# =============================================================================
# Client Formatters
# =============================================================================

def format_client_list(data: Dict[str, Any]) -> str:
    """Format client list for LLM."""
    clients = []
    raw_list = data.get("list", [])
    
    for client in raw_list:
        clients.append({
            "mac": client.get("clientMac") or client.get("mac"),
            "ip": client.get("ipAddress") or client.get("ip"),
            "hostname": client.get("hostName") or client.get("hostname"),
            "user": client.get("userName") or client.get("user"),
            "os": client.get("osType") or client.get("os"),
            "ssid": client.get("ssid") or client.get("wlanName"),
            "ap_name": client.get("apName"),
            "ap_mac": client.get("apMac"),
            "rssi": client.get("rssi"),
            "snr": client.get("snr"),
            "channel": client.get("channel"),
            "radio": client.get("radioType"),
            "vlan": client.get("vlan"),
        })
    
    result = {
        "summary": {
            "total": data.get("totalCount", len(clients)),
            "returned": len(clients),
            "has_more": data.get("hasMore", False),
        },
        "clients": clients
    }
    return _to_json(_clean_nulls(result))


def format_client_detail(data: Dict[str, Any]) -> str:
    """Format single client detail for LLM."""
    result = {
        "client": {
            "mac": data.get("clientMac") or data.get("mac"),
            "ip": data.get("ipAddress") or data.get("ip"),
            "ipv6": data.get("ipv6Address"),
            "hostname": data.get("hostName"),
            "user": data.get("userName"),
            "os": data.get("osType"),
            "device": data.get("deviceType"),
        },
        "connection": {
            "ssid": data.get("ssid"),
            "ap_name": data.get("apName"),
            "ap_mac": data.get("apMac"),
            "zone": data.get("zoneName"),
            "radio": data.get("radioType") or data.get("radioMode"),
            "channel": data.get("channel"),
            "rssi": data.get("rssi"),
            "snr": data.get("snr"),
        },
        "session": {
            "auth_method": data.get("authMethod"),
            "vlan": data.get("vlan"),
            "connected_since": data.get("connectedSince"),
            "traffic_up": data.get("txBytes"),
            "traffic_down": data.get("rxBytes"),
        }
    }
    return _to_json(_clean_nulls(result))


# =============================================================================
# Zone Formatters
# =============================================================================

def format_zone_list(data: Dict[str, Any]) -> str:
    """Format zone list for LLM."""
    zones = []
    raw_list = data.get("list", [])
    
    for zone in raw_list:
        zones.append({
            "id": zone.get("id") or zone.get("zoneId"),
            "name": zone.get("name") or zone.get("zoneName"),
            "description": zone.get("description"),
            "ap_count": zone.get("apCount") or zone.get("numAPs"),
            "client_count": zone.get("clientCount") or zone.get("numClients"),
        })
    
    result = {
        "summary": {
            "total": data.get("totalCount", len(zones)),
            "has_more": data.get("hasMore", False),
        },
        "zones": zones
    }
    return _to_json(_clean_nulls(result))


def format_zone_detail(data: Dict[str, Any]) -> str:
    """Format single zone detail for LLM."""
    result = {
        "zone": {
            "id": data.get("id"),
            "name": data.get("name"),
            "description": data.get("description"),
            "country_code": data.get("countryCode"),
            "timezone": data.get("timezone"),
        },
        "stats": {
            "ap_count": data.get("apCount"),
            "client_count": data.get("clientCount"),
            "wlan_count": data.get("wlanCount"),
        },
        "settings": {
            "ap_firmware": data.get("apFirmwareVersion"),
            "login_session_timeout": data.get("loginSessionTimeout"),
        }
    }
    return _to_json(_clean_nulls(result))


# =============================================================================
# WLAN Formatters
# =============================================================================

def format_wlan_list(data: Dict[str, Any]) -> str:
    """Format WLAN list for LLM."""
    wlans = []
    raw_list = data.get("list", [])
    
    for wlan in raw_list:
        wlans.append({
            "id": wlan.get("id") or wlan.get("wlanId"),
            "name": wlan.get("name") or wlan.get("ssid"),
            "ssid": wlan.get("ssid"),
            "zone": wlan.get("zoneName") or wlan.get("zoneId"),
            "security": wlan.get("authType") or wlan.get("encryption"),
            "vlan": wlan.get("vlan"),
            "enabled": wlan.get("enabled") if wlan.get("enabled") is not None else True,
        })
    
    result = {
        "summary": {
            "total": data.get("totalCount", len(wlans)),
            "has_more": data.get("hasMore", False),
        },
        "wlans": wlans
    }
    return _to_json(_clean_nulls(result))


def format_wlan_detail(data: Dict[str, Any]) -> str:
    """Format single WLAN detail for LLM.
    
    vSZ 6.x WLAN structure:
    - encryption: {method, algorithm, mfp, ...}
    - vlan: {accessVlan, coreQinQEnabled, vlanPooling: {id, name}, ...}
    """
    # Extract encryption info
    encryption = data.get("encryption", {})
    if isinstance(encryption, dict):
        enc_method = encryption.get("method")
        enc_algo = encryption.get("algorithm")
    else:
        enc_method = encryption
        enc_algo = None
    
    # Extract VLAN info
    vlan_data = data.get("vlan", {})
    if isinstance(vlan_data, dict):
        access_vlan = vlan_data.get("accessVlan")
        vlan_pooling = vlan_data.get("vlanPooling", {})
        vlan_pool_name = vlan_pooling.get("name") if isinstance(vlan_pooling, dict) else None
    else:
        access_vlan = vlan_data
        vlan_pool_name = None
    
    # Extract auth info
    auth = data.get("authServiceOrProfile", {})
    if isinstance(auth, dict):
        auth_type = auth.get("throughController") or auth.get("authenticationProfile")
    else:
        auth_type = auth
    
    result = {
        "wlan": {
            "id": data.get("id"),
            "name": data.get("name"),
            "ssid": data.get("ssid"),
            "zone_id": data.get("zoneId"),
            "enabled": data.get("enabled"),
        },
        "security": {
            "auth_type": auth_type,
            "encryption": enc_method,
            "algorithm": enc_algo,
        },
        "network": {
            "vlan": access_vlan,
            "vlan_pool": vlan_pool_name,
            "hide_ssid": data.get("hideSsid"),
        }
    }
    return _to_json(_clean_nulls(result))


# =============================================================================
# Alarm Formatters
# =============================================================================

def format_alarm_list(data: Dict[str, Any]) -> str:
    """Format alarm list for LLM.
    
    vSZ 6.x alarm fields: id, alarmType, severity, alarmState, activity, 
    category, insertionTime, acknowledged, clearTime, clearUser
    """
    alarms = []
    raw_list = data.get("list", data.get("alarms", []))
    
    # Count by severity
    critical = major = minor = warning = 0
    
    for alarm in raw_list:
        severity = (alarm.get("severity") or alarm.get("alarmSeverity") or "").lower()
        if severity == "critical":
            critical += 1
        elif severity == "major":
            major += 1
        elif severity == "minor":
            minor += 1
        else:
            warning += 1
        
        # Convert timestamp to readable format if needed
        insert_time = alarm.get("insertionTime")
        if isinstance(insert_time, int) and insert_time > 1000000000000:
            # Milliseconds timestamp - convert to seconds
            from datetime import datetime
            try:
                insert_time = datetime.fromtimestamp(insert_time / 1000).isoformat()
            except (ValueError, OSError):
                pass
        
        alarms.append({
            "id": alarm.get("id") or alarm.get("alarmId"),
            "type": alarm.get("alarmType") or alarm.get("type"),
            "severity": alarm.get("severity") or alarm.get("alarmSeverity"),
            "state": alarm.get("alarmState"),
            "message": alarm.get("activity") or alarm.get("alarmMessage") or alarm.get("message"),
            "category": alarm.get("category"),
            "time": insert_time,
            "acknowledged": alarm.get("acknowledged"),
        })
    
    result = {
        "summary": {
            "total": data.get("totalCount") or data.get("rawDataTotalCount") or len(alarms),
            "critical": critical,
            "major": major,
            "minor": minor,
            "warning": warning,
            "has_more": data.get("hasMore", False),
        },
        "alarms": alarms
    }
    return _to_json(_clean_nulls(result))


# =============================================================================
# Generic Formatter
# =============================================================================

def format_generic(data: Any) -> str:
    """Generic formatter - clean nulls and return compact JSON."""
    return _to_json(_clean_nulls(data))


def format_success(message: str = "Operation completed successfully") -> str:
    """Format success response."""
    return _to_json({"status": "success", "message": message})


def format_error(error: str) -> str:
    """Format error response."""
    return _to_json({"status": "error", "message": str(error)})
