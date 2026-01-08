"""Tools implementation for Ruckus vSZ MCP Server.

LLM-optimized tool responses with structured, clean data.
"""

import json
from typing import Any, Dict, Optional

from .api_client import RuckusVSZClient, RuckusVSZAPIError
from . import response_formatters as fmt


class RuckusVSZTools:
    """Ruckus vSZ tools implementation for MCP."""

    def __init__(self, client: RuckusVSZClient):
        """Initialize tools with API client."""
        self.client = client

    # System Module Tools
    def system_get_info(self) -> str:
        """Get system information."""
        try:
            result = self.client.system.get_system_info()
            return fmt.format_system_info(result)
        except RuckusVSZAPIError as e:
            return fmt.format_error(str(e))

    def system_get_inventory(self) -> str:
        """Get system inventory."""
        try:
            result = self.client.system.get_system_inventory()
            return fmt.format_system_inventory(result)
        except RuckusVSZAPIError as e:
            return fmt.format_error(str(e))

    def system_get_summary(self) -> str:
        """Get system summary."""
        try:
            result = self.client.system.get_system_summary()
            return fmt.format_system_summary(result)
        except RuckusVSZAPIError as e:
            return fmt.format_error(str(e))

    def system_get_licenses(self) -> str:
        """Get license information."""
        try:
            result = self.client.system.get_licenses()
            return fmt.format_licenses(result)
        except RuckusVSZAPIError as e:
            return fmt.format_error(str(e))

    def system_get_cluster_status(self) -> str:
        """Get cluster status."""
        try:
            result = self.client.system.get_cluster_status()
            return fmt.format_cluster_status(result)
        except RuckusVSZAPIError as e:
            return fmt.format_error(str(e))

    # Zones Module Tools
    def zones_list(self, index: Optional[int] = None, list_size: Optional[int] = None) -> str:
        """List all zones."""
        try:
            result = self.client.zones.list_zones(index=index, list_size=list_size)
            return fmt.format_zone_list(result)
        except RuckusVSZAPIError as e:
            return fmt.format_error(str(e))

    def zones_get(self, zone_id: str) -> str:
        """Get zone details."""
        try:
            result = self.client.zones.get_zone(zone_id)
            return fmt.format_zone_detail(result)
        except RuckusVSZAPIError as e:
            return fmt.format_error(str(e))

    def zones_create(
        self,
        name: str,
        description: Optional[str] = None,
        domain_id: Optional[str] = None,
    ) -> str:
        """Create a new zone."""
        try:
            result = self.client.zones.create_zone(
                name=name, description=description, domain_id=domain_id
            )
            return fmt.format_success(f"Zone '{name}' created successfully")
        except RuckusVSZAPIError as e:
            return fmt.format_error(str(e))

    def zones_update(
        self,
        zone_id: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
    ) -> str:
        """Update zone."""
        try:
            result = self.client.zones.update_zone(
                zone_id=zone_id, name=name, description=description
            )
            return fmt.format_success(f"Zone updated successfully")
        except RuckusVSZAPIError as e:
            return fmt.format_error(str(e))

    def zones_delete(self, zone_id: str) -> str:
        """Delete zone."""
        try:
            result = self.client.zones.delete_zone(zone_id)
            return fmt.format_success(f"Zone deleted successfully")
        except RuckusVSZAPIError as e:
            return fmt.format_error(str(e))

    def zones_get_aps(
        self, zone_id: str, index: Optional[int] = None, list_size: Optional[int] = None
    ) -> str:
        """Get APs in a zone."""
        try:
            result = self.client.zones.get_zone_aps(
                zone_id=zone_id, index=index, list_size=list_size
            )
            return fmt.format_ap_list(result)
        except RuckusVSZAPIError as e:
            return fmt.format_error(str(e))

    def zones_get_wlans(self, zone_id: str) -> str:
        """Get WLANs in a zone."""
        try:
            result = self.client.zones.get_zone_wlans(zone_id)
            return fmt.format_wlan_list(result)
        except RuckusVSZAPIError as e:
            return fmt.format_error(str(e))

    def zones_list_domains(self) -> str:
        """List all domains."""
        try:
            result = self.client.zones.list_domains()
            return fmt.format_generic(result)
        except RuckusVSZAPIError as e:
            return fmt.format_error(str(e))

    # WLANs Module Tools
    def wlans_list(
        self, zone_id: str, index: Optional[int] = None, list_size: Optional[int] = None
    ) -> str:
        """List WLANs in a zone."""
        try:
            result = self.client.wlans.list_wlans(
                zone_id=zone_id, index=index, list_size=list_size
            )
            return fmt.format_wlan_list(result)
        except RuckusVSZAPIError as e:
            return fmt.format_error(str(e))

    def wlans_get(self, zone_id: str, wlan_id: str) -> str:
        """Get WLAN details."""
        try:
            result = self.client.wlans.get_wlan(zone_id=zone_id, wlan_id=wlan_id)
            return fmt.format_wlan_detail(result)
        except RuckusVSZAPIError as e:
            return fmt.format_error(str(e))

    def wlans_create(
        self,
        zone_id: str,
        name: str,
        ssid: str,
        authentication_type: str = "Open",
        encryption_method: Optional[str] = None,
        passphrase: Optional[str] = None,
        vlan_id: Optional[int] = None,
        description: Optional[str] = None,
    ) -> str:
        """Create a new WLAN."""
        try:
            result = self.client.wlans.create_wlan(
                zone_id=zone_id,
                name=name,
                ssid=ssid,
                authentication_type=authentication_type,
                encryption_method=encryption_method,
                passphrase=passphrase,
                vlan_id=vlan_id,
                description=description,
            )
            return fmt.format_success(f"WLAN '{name}' (SSID: {ssid}) created successfully")
        except RuckusVSZAPIError as e:
            return fmt.format_error(str(e))

    def wlans_update(
        self,
        zone_id: str,
        wlan_id: str,
        name: Optional[str] = None,
        ssid: Optional[str] = None,
        description: Optional[str] = None,
    ) -> str:
        """Update WLAN."""
        try:
            result = self.client.wlans.update_wlan(
                zone_id=zone_id, wlan_id=wlan_id, name=name, ssid=ssid, description=description
            )
            return fmt.format_success("WLAN updated successfully")
        except RuckusVSZAPIError as e:
            return fmt.format_error(str(e))

    def wlans_delete(self, zone_id: str, wlan_id: str) -> str:
        """Delete WLAN."""
        try:
            result = self.client.wlans.delete_wlan(zone_id=zone_id, wlan_id=wlan_id)
            return fmt.format_success("WLAN deleted successfully")
        except RuckusVSZAPIError as e:
            return fmt.format_error(str(e))

    def wlans_enable(self, zone_id: str, wlan_id: str) -> str:
        """Enable WLAN."""
        try:
            result = self.client.wlans.enable_wlan(zone_id=zone_id, wlan_id=wlan_id)
            return fmt.format_success("WLAN enabled successfully")
        except RuckusVSZAPIError as e:
            return fmt.format_error(str(e))

    def wlans_disable(self, zone_id: str, wlan_id: str) -> str:
        """Disable WLAN."""
        try:
            result = self.client.wlans.disable_wlan(zone_id=zone_id, wlan_id=wlan_id)
            return fmt.format_success("WLAN disabled successfully")
        except RuckusVSZAPIError as e:
            return fmt.format_error(str(e))

    # Access Points Module Tools
    def aps_list(self, index: Optional[int] = None, list_size: Optional[int] = None) -> str:
        """List all access points."""
        try:
            result = self.client.access_points.list_aps(index=index, list_size=list_size)
            return fmt.format_ap_list(result)
        except RuckusVSZAPIError as e:
            return fmt.format_error(str(e))

    def aps_get(self, ap_mac: str) -> str:
        """Get AP details."""
        try:
            result = self.client.access_points.get_ap(ap_mac)
            return fmt.format_ap_detail(result)
        except RuckusVSZAPIError as e:
            return fmt.format_error(str(e))

    def aps_update(
        self,
        ap_mac: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        location: Optional[str] = None,
        latitude: Optional[float] = None,
        longitude: Optional[float] = None,
    ) -> str:
        """Update AP configuration."""
        try:
            result = self.client.access_points.update_ap(
                ap_mac=ap_mac,
                name=name,
                description=description,
                location=location,
                latitude=latitude,
                longitude=longitude,
            )
            return fmt.format_success(f"AP {ap_mac} updated successfully")
        except RuckusVSZAPIError as e:
            return fmt.format_error(str(e))

    def aps_delete(self, ap_mac: str) -> str:
        """Remove AP from management."""
        try:
            result = self.client.access_points.delete_ap(ap_mac)
            return fmt.format_success(f"AP {ap_mac} removed from management")
        except RuckusVSZAPIError as e:
            return fmt.format_error(str(e))

    def aps_reboot(self, ap_mac: str) -> str:
        """Reboot an access point."""
        try:
            result = self.client.access_points.reboot_ap(ap_mac)
            return fmt.format_success(f"AP {ap_mac} reboot initiated")
        except RuckusVSZAPIError as e:
            return fmt.format_error(str(e))

    def aps_get_operational_info(self, ap_mac: str) -> str:
        """Get AP operational information."""
        try:
            result = self.client.access_points.get_ap_operational_info(ap_mac)
            return fmt.format_ap_detail(result)
        except RuckusVSZAPIError as e:
            return fmt.format_error(str(e))

    def aps_get_clients(self, ap_mac: str) -> str:
        """Get clients connected to an AP."""
        try:
            result = self.client.access_points.get_ap_clients(ap_mac)
            return fmt.format_client_list(result)
        except RuckusVSZAPIError as e:
            return fmt.format_error(str(e))

    def aps_get_lldp_neighbors(self, ap_mac: str) -> str:
        """Get LLDP neighbors discovered by an AP."""
        try:
            result = self.client.access_points.get_ap_lldp_neighbors(ap_mac)
            return fmt.format_ap_lldp_neighbors(result)
        except RuckusVSZAPIError as e:
            return fmt.format_error(str(e))

    def aps_query(
        self,
        filters: Optional[Dict[str, Any]] = None,
        full_text_search: Optional[str] = None,
        index: Optional[int] = None,
        list_size: Optional[int] = None,
    ) -> str:
        """Query APs with filters."""
        try:
            result = self.client.access_points.query_aps(
                filters=filters,
                full_text_search=full_text_search,
                index=index,
                list_size=list_size,
            )
            return fmt.format_ap_list(result)
        except RuckusVSZAPIError as e:
            return fmt.format_error(str(e))

    # Clients Module Tools
    def clients_list(self, index: Optional[int] = None, list_size: Optional[int] = None) -> str:
        """List all connected clients."""
        try:
            result = self.client.clients.list_clients(index=index, list_size=list_size)
            return fmt.format_client_list(result)
        except RuckusVSZAPIError as e:
            return fmt.format_error(str(e))

    def clients_get(self, client_mac: str) -> str:
        """Get client details."""
        try:
            result = self.client.clients.get_client(client_mac)
            return fmt.format_client_detail(result)
        except RuckusVSZAPIError as e:
            return fmt.format_error(str(e))

    def clients_disconnect(self, client_mac: str) -> str:
        """Disconnect a client."""
        try:
            result = self.client.clients.disconnect_client(client_mac)
            return fmt.format_success(f"Client {client_mac} disconnected")
        except RuckusVSZAPIError as e:
            return fmt.format_error(str(e))

    def clients_query(
        self,
        filters: Optional[Dict[str, Any]] = None,
        full_text_search: Optional[str] = None,
        index: Optional[int] = None,
        list_size: Optional[int] = None,
    ) -> str:
        """Query clients with filters."""
        try:
            result = self.client.clients.query_clients(
                filters=filters,
                full_text_search=full_text_search,
                index=index,
                list_size=list_size,
            )
            return fmt.format_client_list(result)
        except RuckusVSZAPIError as e:
            return fmt.format_error(str(e))

    # Monitoring Module Tools
    def monitoring_get_ap_statistics(self, ap_mac: str) -> str:
        """Get AP statistics."""
        try:
            result = self.client.monitoring.get_ap_statistics(ap_mac)
            return fmt.format_generic(result)
        except RuckusVSZAPIError as e:
            return fmt.format_error(str(e))

    def monitoring_get_wlan_statistics(self, zone_id: str, wlan_id: str) -> str:
        """Get WLAN statistics."""
        try:
            result = self.client.monitoring.get_wlan_statistics(zone_id=zone_id, wlan_id=wlan_id)
            return fmt.format_generic(result)
        except RuckusVSZAPIError as e:
            return fmt.format_error(str(e))

    def monitoring_get_zone_statistics(self, zone_id: str) -> str:
        """Get zone statistics."""
        try:
            result = self.client.monitoring.get_zone_statistics(zone_id)
            return fmt.format_generic(result)
        except RuckusVSZAPIError as e:
            return fmt.format_error(str(e))

    def monitoring_get_active_client_count(self) -> str:
        """Get active client count."""
        try:
            result = self.client.monitoring.get_active_client_count()
            return fmt.format_generic(result)
        except RuckusVSZAPIError as e:
            return fmt.format_error(str(e))

    # Alarms Module Tools
    def alarms_list(self, index: Optional[int] = None, list_size: Optional[int] = None) -> str:
        """List all alarms."""
        try:
            result = self.client.alarms.list_alarms(index=index, list_size=list_size)
            return fmt.format_alarm_list(result)
        except RuckusVSZAPIError as e:
            return fmt.format_error(str(e))

    def alarms_get(self, alarm_id: str) -> str:
        """Get alarm details."""
        try:
            result = self.client.alarms.get_alarm(alarm_id)
            return fmt.format_generic(result)
        except RuckusVSZAPIError as e:
            return fmt.format_error(str(e))

    def alarms_acknowledge(self, alarm_id: str) -> str:
        """Acknowledge an alarm."""
        try:
            result = self.client.alarms.acknowledge_alarm(alarm_id)
            return fmt.format_success(f"Alarm {alarm_id} acknowledged")
        except RuckusVSZAPIError as e:
            return fmt.format_error(str(e))

    def alarms_get_summary(self) -> str:
        """Get alarm summary with counts by severity."""
        try:
            # Get alarms list to count by severity
            result = self.client.alarms.list_alarms(list_size=500)
            return fmt.format_alarm_list(result)
        except RuckusVSZAPIError as e:
            return fmt.format_error(str(e))

    # Authentication Module Tools
    def authentication_list_radius_profiles(self, zone_id: str) -> str:
        """List RADIUS authentication profiles."""
        try:
            result = self.client.authentication.list_radius_profiles(zone_id)
            return fmt.format_generic(result)
        except RuckusVSZAPIError as e:
            return fmt.format_error(str(e))

    def authentication_get_radius_profile(self, zone_id: str, profile_id: str) -> str:
        """Get RADIUS profile details."""
        try:
            result = self.client.authentication.get_radius_profile(
                zone_id=zone_id, profile_id=profile_id
            )
            return fmt.format_generic(result)
        except RuckusVSZAPIError as e:
            return fmt.format_error(str(e))

    def authentication_create_radius_profile(
        self,
        zone_id: str,
        name: str,
        primary_server: str,
        primary_port: int = 1812,
        primary_shared_secret: str = "",
    ) -> str:
        """Create RADIUS authentication profile."""
        try:
            result = self.client.authentication.create_radius_profile(
                zone_id=zone_id,
                name=name,
                primary_server=primary_server,
                primary_port=primary_port,
                primary_shared_secret=primary_shared_secret,
            )
            return fmt.format_success(f"RADIUS profile '{name}' created successfully")
        except RuckusVSZAPIError as e:
            return fmt.format_error(str(e))

    # Network Module Tools
    def network_list_vlan_pools(self, zone_id: str) -> str:
        """List VLAN pools."""
        try:
            result = self.client.network.list_vlan_pools(zone_id)
            return fmt.format_generic(result)
        except RuckusVSZAPIError as e:
            return fmt.format_error(str(e))

    def network_create_vlan_pool(
        self,
        zone_id: str,
        name: str,
        vlan_list: str,
        description: Optional[str] = None,
    ) -> str:
        """Create VLAN pool."""
        try:
            result = self.client.network.create_vlan_pool(
                zone_id=zone_id, name=name, vlan_list=vlan_list, description=description
            )
            return fmt.format_success(f"VLAN pool '{name}' created successfully")
        except RuckusVSZAPIError as e:
            return fmt.format_error(str(e))

    def network_list_qos_profiles(self, zone_id: str) -> str:
        """List QoS profiles."""
        try:
            result = self.client.network.list_qos_profiles(zone_id)
            return fmt.format_generic(result)
        except RuckusVSZAPIError as e:
            return fmt.format_error(str(e))
