"""Monitoring module for Ruckus vSZ API - Statistics and monitoring.

Multi-version support:
- vSZ 6.x: Uses query endpoints and alternate paths
- vSZ 7.x+: Uses direct statistics endpoints
"""

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
        # Try multiple endpoint patterns
        try:
            return self.client.get(f"aps/{ap_mac}/operational/summary")
        except Exception:
            try:
                return self.client.get(f"aps/{ap_mac}/statistics")
            except Exception:
                # Fallback: get operational info
                return self.client.get(f"aps/{ap_mac}")

    def get_wlan_statistics(self, zone_id: str, wlan_id: str) -> Dict[str, Any]:
        """Get WLAN statistics.
        
        Args:
            zone_id: Zone UUID
            wlan_id: WLAN UUID
            
        Returns:
            WLAN statistics
        """
        try:
            return self.client.get(f"rkszones/{zone_id}/wlans/{wlan_id}/statistics")
        except Exception:
            # Fallback: get WLAN info
            return self.client.get(f"rkszones/{zone_id}/wlans/{wlan_id}")

    def get_zone_statistics(self, zone_id: str) -> Dict[str, Any]:
        """Get zone statistics.
        
        Args:
            zone_id: Zone UUID
            
        Returns:
            Zone statistics
        """
        try:
            return self.client.get(f"rkszones/{zone_id}/statistics")
        except Exception:
            # Fallback: get zone info
            return self.client.get(f"rkszones/{zone_id}")

    def get_system_statistics(self) -> Dict[str, Any]:
        """Get system-wide statistics.
        
        Returns:
            System statistics
        """
        try:
            return self.client.get("system/statistics")
        except Exception:
            try:
                return self.client.get("controller")
            except Exception:
                return self.client.get("system")

    def get_active_client_count(self) -> Dict[str, Any]:
        """Get active client count.
        
        Multi-version: tries multiple endpoints.
        
        Returns:
            Active client statistics
        """
        # Try different endpoints
        endpoints = [
            "clients/activeCount",
            "system/clientCount",
        ]
        
        for endpoint in endpoints:
            try:
                return self.client.get(endpoint)
            except Exception:
                continue
        
        # Fallback: query clients to get totalCount
        try:
            result = self.client.post("query/client", {})
            total = result.get("totalCount", 0)
            return {
                "activeCount": total,
                "note": "Count via query/client endpoint"
            }
        except Exception as e:
            return {"activeCount": 0, "error": f"Could not retrieve client count: {e}"}

    def get_ap_capacity_summary(self) -> Dict[str, Any]:
        """Get AP capacity summary.
        
        Returns:
            AP capacity information
        """
        try:
            return self.client.get("aps/capacitySummary")
        except Exception:
            # Fallback: query APs and count
            try:
                result = self.client.post("query/ap", {"listSize": 1})
                return {
                    "totalAPs": result.get("totalCount", 0),
                    "note": "Capacity via query endpoint"
                }
            except Exception:
                return {"error": "AP capacity not available"}

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
        try:
            return self.client.get("aps/topByTraffic", params=params)
        except Exception:
            return {"error": "Top APs by traffic not available", "list": []}

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
        try:
            return self.client.get("clients/topByTraffic", params=params)
        except Exception:
            return {"error": "Top clients by traffic not available", "list": []}

    def get_rf_performance(self, zone_id: str) -> Dict[str, Any]:
        """Get RF performance data for a zone.
        
        Args:
            zone_id: Zone UUID
            
        Returns:
            RF performance data
        """
        try:
            return self.client.get(f"rkszones/{zone_id}/rfPerformance")
        except Exception:
            return {"error": "RF performance data not available"}

    def get_mesh_info(self, zone_id: str) -> Dict[str, Any]:
        """Get mesh network information.
        
        Args:
            zone_id: Zone UUID
            
        Returns:
            Mesh topology information
        """
        try:
            return self.client.get(f"rkszones/{zone_id}/mesh")
        except Exception:
            return {"error": "Mesh info not available"}
