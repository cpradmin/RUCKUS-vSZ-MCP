"""Switches module for Ruckus vSZ API - ICX Switch management via SmartZone Switch Manager and direct RESTCONF."""

from typing import TYPE_CHECKING, Any, Dict, Optional
import requests
import urllib3

if TYPE_CHECKING:
    from ..api_client import RuckusVSZClient

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class SwitchesModule:
    """ICX Switch management via SmartZone Switch Manager API and direct RESTCONF."""

    def __init__(self, client: "RuckusVSZClient"):
        """Initialize Switches module."""
        self.client = client

    # ---- SmartZone Switch Manager (fleet-level, /switchm/api/v1/) ----

    def _sw(self, path: str, params=None) -> Dict[str, Any]:
        return self.client.get(f"switchm/api/v1/{path}", params=params)

    def _sw_post(self, path: str, data: Dict) -> Dict[str, Any]:
        return self.client.post(f"switchm/api/v1/{path}", data)

    def list_switches(self, page: int = 0, page_size: int = 100) -> Dict[str, Any]:
        """List all ICX switches managed by this controller."""
        return self._sw_post("switches/query", {"page": page, "pageSize": page_size})

    def get_switch(self, switch_id: str) -> Dict[str, Any]:
        """Get full details for a specific switch."""
        return self._sw(f"switches/{switch_id}")

    def get_switch_health(self, switch_id: str) -> Dict[str, Any]:
        """Get hardware health: CPU, memory, temperature, fans, PSUs."""
        try:
            return self._sw(f"switches/{switch_id}/status")
        except Exception:
            return self._sw(f"switches/{switch_id}")

    def get_switch_firmware(self, switch_id: str) -> Dict[str, Any]:
        """Get firmware version and upgrade availability."""
        return self._sw(f"switches/{switch_id}/firmware")

    def get_switch_config(self, switch_id: str) -> Dict[str, Any]:
        """Get running configuration backup."""
        return self._sw(f"switches/{switch_id}/config")

    def list_ports(self, switch_id: str) -> Dict[str, Any]:
        """List all ports: status, speed, VLAN, error counts.
        High errors + low Rx = bad SFP/fiber (the I-10 HUB7 pattern)."""
        return self._sw(f"switches/{switch_id}/ports")

    def get_port_errors(self, switch_id: str, port_id: Optional[str] = None) -> Dict[str, Any]:
        """Get CRC/error counters. High CRC + low RX = bad SFP or fiber."""
        if port_id:
            return self._sw(f"switches/{switch_id}/ports/{port_id}/errors")
        try:
            return self._sw(f"switches/{switch_id}/ports/errors")
        except Exception:
            return self.list_ports(switch_id)

    def get_lldp_topology(self, switch_id: str) -> Dict[str, Any]:
        """Get LLDP neighbor table - maps APs, DMS signs, cameras to ports.
        Essential for D3ECHO corridor device-to-port mapping."""
        return self._sw(f"switches/{switch_id}/lldpNeighbors")

    def list_switch_alarms(self, switch_id: str, severity: Optional[str] = None) -> Dict[str, Any]:
        """Get active alarms for a switch (severity: CRITICAL/MAJOR/MINOR/WARNING)."""
        params = {}
        if severity:
            params["severity"] = severity
        try:
            return self._sw(f"switches/{switch_id}/alarms", params=params)
        except Exception:
            return self._sw_post("switches/alarms/query", {"switchId": switch_id})

    def get_stack_details(self, stack_id: str) -> Dict[str, Any]:
        """Get ICX stack: unit inventory, roles, inter-unit link status.
        For I-10 corridor: each hub has 12-unit ICX stack; East LAG / West LAG 20Gbps ring."""
        return self._sw(f"switchStacks/{stack_id}")

    def list_stacks(self) -> Dict[str, Any]:
        """List all ICX stacks on this controller."""
        try:
            return self._sw_post("switchStacks/query", {})
        except Exception:
            return self._sw("switchStacks")

    def reboot_switch(self, switch_id: str) -> Dict[str, Any]:
        """Reboot a switch. USE WITH CAUTION on live corridor infrastructure."""
        return self.client.post(f"switchm/api/v1/switches/{switch_id}/reboot", {})

    def upgrade_firmware(self, switch_id: str, firmware_version: Optional[str] = None) -> Dict[str, Any]:
        """Trigger firmware upgrade. USE WITH CAUTION."""
        data: Dict[str, Any] = {}
        if firmware_version:
            data["firmwareVersion"] = firmware_version
        return self.client.post(f"switchm/api/v1/switches/{switch_id}/firmware", data)

    # ---- ICX RESTCONF (direct per-switch, port 443) ----

    def _restconf_get(self, switch_ip: str, yang_path: str,
                      username: str = "admin", password: str = "admin",
                      verify_ssl: bool = False) -> Dict[str, Any]:
        """GET RESTCONF data directly from an ICX switch."""
        url = f"https://{switch_ip}/rest/v1/{yang_path}"
        resp = requests.get(
            url, auth=(username, password), verify=verify_ssl, timeout=15,
            headers={"Accept": "application/vnd.yang.data+json"}
        )
        resp.raise_for_status()
        return resp.json()

    def get_optics(self, switch_ip: str, username: str = "admin",
                   password: str = "admin") -> Dict[str, Any]:
        """Get SFP Tx/Rx dBm per port. Healthy range: -3 to -20 dBm Rx.
        Outside range = bad SFP or degraded fiber. Requires RESTCONF on ICX."""
        try:
            return self._restconf_get(switch_ip, "brocade-interface-ext:optic-info", username, password)
        except Exception as e:
            return {"error": str(e), "hint": "Enable RESTCONF: 'web-management https' on ICX"}

    def get_lag_status(self, switch_ip: str, username: str = "admin",
                       password: str = "admin") -> Dict[str, Any]:
        """Get LAG member status and active bandwidth.
        I-10 corridor: East LAG (Switch 1s, 20Gbps) + West LAG (Switch 12s, 20Gbps)."""
        try:
            return self._restconf_get(switch_ip, "brocade-lag:lag", username, password)
        except Exception as e:
            return {"error": str(e)}

    def get_ospf_neighbors(self, switch_ip: str, username: str = "admin",
                           password: str = "admin") -> Dict[str, Any]:
        """Get OSPF neighbor adjacency state (FULL/2WAY/INIT/DOWN)."""
        try:
            return self._restconf_get(switch_ip, "brocade-ospf:ospf", username, password)
        except Exception as e:
            return {"error": str(e)}

    def get_mac_table(self, switch_ip: str, vlan_id: Optional[int] = None,
                      port: Optional[str] = None,
                      username: str = "admin", password: str = "admin") -> Dict[str, Any]:
        """Get MAC table, optionally filtered by VLAN or port."""
        try:
            data = self._restconf_get(switch_ip, "brocade-mac:mac-address-table", username, password)
            entries = data.get("mac-address-table", {}).get("mac-address", [])
            if vlan_id:
                entries = [e for e in entries if e.get("vlan-id") == vlan_id]
            if port:
                entries = [e for e in entries if port in str(e.get("port-name", ""))]
            return {"mac-address": entries, "count": len(entries)}
        except Exception as e:
            return {"error": str(e)}

    def get_vlan_config(self, switch_ip: str, username: str = "admin",
                        password: str = "admin") -> Dict[str, Any]:
        """Get VLAN tagged/untagged port assignments."""
        try:
            return self._restconf_get(switch_ip, "brocade-vlan:vlan", username, password)
        except Exception as e:
            return {"error": str(e)}
