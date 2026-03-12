"""Switch module for Ruckus vSZ API - ICX switch fleet management.

Supports two API surfaces:
- SmartZone Switch Manager API (/switchm/api/v1) - fleet-level via controller
- ICX RESTCONF API (direct per-switch port 443) - deep diagnostics

D3ECHO/Trinity priority tools marked with # PRIORITY
"""

from typing import TYPE_CHECKING, Any, Dict, List, Optional

if TYPE_CHECKING:
    from ..api_client import RuckusVSZClient


class SwitchesModule:
    """ICX Switch management module."""

    def __init__(self, client: "RuckusVSZClient"):
        """Initialize Switches module."""
        self.client = client

    # ── SmartZone Switch Manager API ──────────────────────────────────────

    def list_switches(self, zone_id: Optional[str] = None,
                      domain_id: Optional[str] = None) -> Dict[str, Any]:
        """List all ICX switches managed by this controller.

        Args:
            zone_id: Filter by zone ID
            domain_id: Filter by domain ID

        Returns:
            List of switches with status, firmware, IP, model
        """
        params: Dict[str, Any] = {"limit": 1000}
        if zone_id:
            params["zoneId"] = zone_id
        if domain_id:
            params["domainId"] = domain_id
        return self.client.get("switchm/switches", params=params)

    def get_switch(self, switch_id: str) -> Dict[str, Any]:
        """Get full details for a specific ICX switch.

        Args:
            switch_id: Switch ID (from list_switches)

        Returns:
            Switch detail including model, serial, firmware, IP, uptime
        """
        return self.client.get(f"switchm/switches/{switch_id}")

    def get_switch_health(self, switch_id: str) -> Dict[str, Any]:
        """Get hardware health for a switch: CPU, memory, temperature, fans, PSUs.

        Args:
            switch_id: Switch ID

        Returns:
            Health metrics - CPU%, mem%, temp readings, fan/PSU states
        """  # PRIORITY
        return self.client.try_endpoints([
            f"switchm/switches/{switch_id}/hardware",
            f"switchm/switches/{switch_id}/health",
            f"switchm/switches/{switch_id}/status",
        ])

    def get_switch_firmware(self, switch_id: str) -> Dict[str, Any]:
        """Get firmware version and upgrade availability for a switch.

        Args:
            switch_id: Switch ID

        Returns:
            Current firmware, available upgrade version if any
        """
        return self.client.try_endpoints([
            f"switchm/switches/{switch_id}/firmware",
            f"switchm/switches/{switch_id}/version",
        ])

    def get_switch_config(self, switch_id: str) -> Dict[str, Any]:
        """Pull running configuration backup from a switch.

        Args:
            switch_id: Switch ID

        Returns:
            Running config text or structured config object
        """
        return self.client.get(f"switchm/switches/{switch_id}/config")

    def list_switch_ports(self, switch_id: str) -> Dict[str, Any]:
        """List all ports on a switch with status, speed, VLAN, and PoE info.

        Args:
            switch_id: Switch ID

        Returns:
            Per-port status: up/down, speed, tagged/untagged VLANs, PoE draw
        """  # PRIORITY
        return self.client.try_endpoints([
            f"switchm/switches/{switch_id}/ports",
            f"switchm/switches/{switch_id}/portStatus",
        ])

    def get_port_errors(self, switch_id: str,
                        port_id: Optional[str] = None) -> Dict[str, Any]:
        """Get error counters for switch ports - catches bad SFPs and cabling.

        Args:
            switch_id: Switch ID
            port_id: Optional specific port (e.g. '1/1/1'). All ports if omitted.

        Returns:
            CRC errors, RX/TX drop counters, input/output errors per port
        """  # PRIORITY - would have caught today's bad SFP before stack went down
        base = f"switchm/switches/{switch_id}/ports"
        if port_id:
            return self.client.try_endpoints([
                f"{base}/{port_id}/errors",
                f"{base}/{port_id}/counters",
                f"{base}/{port_id}/statistics",
            ])
        return self.client.try_endpoints([
            f"{base}/errors",
            f"{base}/counters",
            f"{base}/statistics",
        ])

    def get_lldp_topology(self, switch_id: str) -> Dict[str, Any]:
        """Get LLDP neighbor table for a switch - maps APs and devices to ports.

        Args:
            switch_id: Switch ID

        Returns:
            LLDP neighbors per port: device name, MAC, port, system description
        """  # PRIORITY
        return self.client.try_endpoints([
            f"switchm/switches/{switch_id}/lldpNeighbors",
            f"switchm/switches/{switch_id}/topology/lldp",
            f"switchm/switches/{switch_id}/neighbors",
        ])

    def list_switch_alarms(self, switch_id: str,
                           severity: Optional[str] = None) -> Dict[str, Any]:
        """Get active alarms for a specific switch.

        Args:
            switch_id: Switch ID
            severity: Filter by severity (Critical, Major, Minor, Warning)

        Returns:
            Active alarms with description, severity, timestamp
        """
        params: Dict[str, Any] = {}
        if severity:
            params["severity"] = severity
        return self.client.try_endpoints([
            f"switchm/switches/{switch_id}/alarms",
            f"switchm/switches/{switch_id}/events",
        ], params=params if params else None)

    def get_stack(self, stack_id: str) -> Dict[str, Any]:
        """Get stack topology: member units, roles, and inter-unit link status.

        Args:
            stack_id: Stack ID (from list_stacks)

        Returns:
            Stack units with role (active/standby/member), inter-unit link state,
            active/standby unit IDs, stack bandwidth
        """  # PRIORITY - monitors the inter-stack LAG links that caused today's outage
        return self.client.try_endpoints([
            f"switchm/switchStacks/{stack_id}",
            f"switchm/stacks/{stack_id}",
        ])

    def list_stacks(self, zone_id: Optional[str] = None) -> Dict[str, Any]:
        """List all switch stacks managed by this controller.

        Args:
            zone_id: Filter by zone ID

        Returns:
            List of stacks with ID, name, member count, status
        """
        params = {"limit": 500}
        if zone_id:
            params["zoneId"] = zone_id
        return self.client.try_endpoints([
            "switchm/switchStacks",
            "switchm/stacks",
        ], params=params)

    def reboot_switch(self, switch_id: str) -> Dict[str, Any]:
        """Reboot a switch via SmartZone.

        Args:
            switch_id: Switch ID

        Returns:
            Reboot initiation result
        """
        return self.client.post(f"switchm/switches/{switch_id}/reboot", {})

    def upgrade_switch_firmware(self, switch_id: str,
                                firmware_version: Optional[str] = None) -> Dict[str, Any]:
        """Upgrade switch firmware via SmartZone.

        Args:
            switch_id: Switch ID
            firmware_version: Target firmware version. Uses latest if omitted.

        Returns:
            Upgrade initiation result
        """
        data: Dict[str, Any] = {}
        if firmware_version:
            data["firmwareVersion"] = firmware_version
        return self.client.post(f"switchm/switches/{switch_id}/upgrade", data)

    # ── ICX RESTCONF API (direct per-switch) ─────────────────────────────

    def _restconf_get(self, switch_ip: str, yang_path: str,
                      username: str = "admin",
                      password: str = "") -> Dict[str, Any]:
        """Internal: direct RESTCONF call to an ICX switch.

        Args:
            switch_ip: Switch management IP
            yang_path: YANG model path (e.g. 'brocade-interface:interface')
            username: Switch login (default admin)
            password: Switch password

        Returns:
            RESTCONF response dict
        """
        import requests, urllib3
        urllib3.disable_warnings()
        url = f"https://{switch_ip}/rest/v1/{yang_path}"
        resp = requests.get(url, auth=(username, password),
                            verify=False, timeout=10)
        resp.raise_for_status()
        return resp.json()

    def get_optics(self, switch_ip: str,
                   username: str = "admin",
                   password: str = "") -> Dict[str, Any]:
        """Get SFP/optic Tx/Rx power levels (dBm) per port via RESTCONF.

        Healthy range: Rx -3 to -20 dBm. Below -20 = degraded/bad fiber or SFP.
        Use this to catch bad optics before they cause stack outages.

        Args:
            switch_ip: Switch management IP
            username: Switch login
            password: Switch password

        Returns:
            Per-port optic stats: Tx dBm, Rx dBm, temp, voltage, vendor
        """  # PRIORITY - this tool catches the exact failure mode from today
        try:
            return self._restconf_get(switch_ip,
                "brocade-interface:interface-optical-monitoring-detail",
                username, password)
        except Exception:
            return self._restconf_get(switch_ip,
                "brocade-interface:interface/gigabitethernet",
                username, password)

    def get_lag_status(self, switch_ip: str,
                       username: str = "admin",
                       password: str = "") -> Dict[str, Any]:
        """Get LAG/trunk member status, active bandwidth, and LACP state via RESTCONF.

        Args:
            switch_ip: Switch management IP
            username: Switch login
            password: Switch password

        Returns:
            LAG groups with member ports, LACP state, active/inactive members,
            aggregate bandwidth
        """  # PRIORITY - monitors the 20Gbps inter-stack LAGs
        return self._restconf_get(switch_ip,
            "brocade-lag:lag", username, password)

    def get_ospf_neighbors(self, switch_ip: str,
                           username: str = "admin",
                           password: str = "") -> Dict[str, Any]:
        """Get OSPF neighbor adjacency state via RESTCONF.

        Args:
            switch_ip: Switch management IP
            username: Switch login
            password: Switch password

        Returns:
            OSPF neighbors with state (Full/Init/Down), router-id, interface
        """
        return self._restconf_get(switch_ip,
            "brocade-ospf:ospf/ospf-neighbor", username, password)

    def get_mac_table(self, switch_ip: str,
                      vlan_id: Optional[int] = None,
                      port: Optional[str] = None,
                      username: str = "admin",
                      password: str = "") -> Dict[str, Any]:
        """Get MAC address table via RESTCONF.

        Args:
            switch_ip: Switch management IP
            vlan_id: Filter by VLAN ID
            port: Filter by port (e.g. '1/1/1')
            username: Switch login
            password: Switch password

        Returns:
            MAC table entries with port, VLAN, type (dynamic/static)
        """
        path = "brocade-mac-address-table:mac-address-table"
        data = self._restconf_get(switch_ip, path, username, password)
        if vlan_id or port:
            entries = data.get("mac-address-table", {}).get("mac-address", [])
            if vlan_id:
                entries = [e for e in entries if e.get("vlanid") == vlan_id]
            if port:
                entries = [e for e in entries if port in str(e.get("port-name", ""))]
            return {"mac-address-table": {"mac-address": entries}}
        return data

    def get_vlan_config(self, switch_ip: str,
                        username: str = "admin",
                        password: str = "") -> Dict[str, Any]:
        """Get VLAN configuration (tagged/untagged ports) via RESTCONF.

        Args:
            switch_ip: Switch management IP
            username: Switch login
            password: Switch password

        Returns:
            VLAN list with tagged and untagged port assignments
        """
        return self._restconf_get(switch_ip,
            "brocade-vlan:vlan", username, password)
