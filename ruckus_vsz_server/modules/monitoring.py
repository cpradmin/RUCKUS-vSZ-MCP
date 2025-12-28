"""Monitoring module for Ruckus vSZ API - Statistics and monitoring."""

from typing import TYPE_CHECKING, Any, Dict, Optional

if TYPE_CHECKING:
    from ..api_client import RuckusVSZClient


class MonitoringModule:
    """Monitoring API module for statistics and performance data."""

    def __init__(self, client: "RuckusVSZClient"):
        """Initialize Monitoring module."""
        self.client = client

    def get_ap_statistics(self, ap_mac: str) -> Dict[str, Any]:
        """Get AP statistics.
        
        Args:
            ap_mac: AP MAC address
            
        Returns:
            AP statistics
        """
        return self.client.get(f"aps/{ap_mac}/statistics")

    def get_wlan_statistics(self, zone_id: str, wlan_id: str) -> Dict[str, Any]:
        """Get WLAN statistics.
        
        Args:
            zone_id: Zone UUID
            wlan_id: WLAN UUID
            
        Returns:
            WLAN statistics
        """
        return self.client.get(f"rkszones/{zone_id}/wlans/{wlan_id}/statistics")

    def get_zone_statistics(self, zone_id: str) -> Dict[str, Any]:
        """Get zone statistics.
        
        Args:
            zone_id: Zone UUID
            
        Returns:
            Zone statistics
        """
        return self.client.get(f"rkszones/{zone_id}/statistics")

    def get_system_statistics(self) -> Dict[str, Any]:
        """Get system-wide statistics.
        
        Returns:
            System statistics
        """
        return self.client.get("system/statistics")

    def get_active_client_count(self) -> Dict[str, Any]:
        """Get active client count.
        
        Returns:
            Active client statistics
        """
        return self.client.get("clients/activeCount")

    def get_ap_capacity_summary(self) -> Dict[str, Any]:
        """Get AP capacity summary.
        
        Returns:
            AP capacity information
        """
        return self.client.get("aps/capacitySummary")

    def get_top_aps_by_traffic(
        self,
        limit: int = 10,
        interval: str = "LASTDAY"
    ) -> Dict[str, Any]:
        """Get top APs by traffic.
        
        Args:
            limit: Number of top APs to return
            interval: Time interval (LASTDAY, LASTWEEK, LASTMONTH)
            
        Returns:
            Top APs by traffic
        """
        params = {
            "limit": limit,
            "interval": interval
        }
        return self.client.get("aps/topByTraffic", params=params)

    def get_top_clients_by_traffic(
        self,
        limit: int = 10,
        interval: str = "LASTDAY"
    ) -> Dict[str, Any]:
        """Get top clients by traffic.
        
        Args:
            limit: Number of top clients to return
            interval: Time interval (LASTDAY, LASTWEEK, LASTMONTH)
            
        Returns:
            Top clients by traffic
        """
        params = {
            "limit": limit,
            "interval": interval
        }
        return self.client.get("clients/topByTraffic", params=params)

    def get_rf_performance(self, zone_id: str) -> Dict[str, Any]:
        """Get RF performance data for a zone.
        
        Args:
            zone_id: Zone UUID
            
        Returns:
            RF performance data
        """
        return self.client.get(f"rkszones/{zone_id}/rfPerformance")

    def get_mesh_info(self, zone_id: str) -> Dict[str, Any]:
        """Get mesh network information.
        
        Args:
            zone_id: Zone UUID
            
        Returns:
            Mesh topology information
        """
        return self.client.get(f"rkszones/{zone_id}/mesh")
