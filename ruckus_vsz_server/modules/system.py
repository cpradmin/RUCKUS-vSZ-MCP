"""System module for Ruckus vSZ API - System information and controller management.

Multi-version support:
- vSZ 6.x: Uses controller and licenses endpoints
- vSZ 7.x+: Uses system/* endpoints
"""

from typing import TYPE_CHECKING, Any, Dict, Optional

if TYPE_CHECKING:
    from ..api_client import RuckusVSZClient


class SystemModule:
    """System API module."""

    def __init__(self, client: "RuckusVSZClient"):
        """Initialize System module."""
        self.client = client

    def get_system_info(self) -> Dict[str, Any]:
        """Get system information.
        
        Returns:
            System information including version, model, uptime
        """
        try:
            result = self.client.get("controller")
            # If result is a list response, return first controller
            if isinstance(result, dict) and "list" in result and result["list"]:
                return result["list"][0]
            return result
        except Exception:
            return self.client.get("system")

    def get_system_inventory(self) -> Dict[str, Any]:
        """Get system inventory.
        
        Returns:
            System inventory information
        """
        try:
            return self.client.get("system/inventory")
        except Exception:
            try:
                return self.client.get("controller")
            except Exception:
                return {"error": "Inventory not available"}

    def get_system_summary(self) -> Dict[str, Any]:
        """Get system summary with controller details and stats.
        
        Builds a comprehensive summary by querying multiple endpoints.
        
        Returns:
            System summary with statistics
        """
        summary = {}
        
        # Get controller info
        try:
            result = self.client.get("controller")
            if isinstance(result, dict) and "list" in result and result["list"]:
                ctrl = result["list"][0]
            else:
                ctrl = result
            summary.update({
                "clusterName": ctrl.get("clusterName") or ctrl.get("hostName"),
                "model": ctrl.get("model"),
                "version": ctrl.get("version"),
            })
        except Exception:
            pass
        
        # Get AP counts from query/ap with status breakdown
        try:
            ap_result = self.client.post("query/ap", {"limit": 1000})
            summary["totalAPs"] = ap_result.get("totalCount", 0)
            
            # Count by status
            online = offline = flagged = 0
            for ap in ap_result.get("list", []):
                status = (ap.get("status") or "").lower()
                if status == "online":
                    online += 1
                elif status == "offline":
                    offline += 1
                else:
                    flagged += 1
            
            summary["connectedAPs"] = online
            summary["disconnectedAPs"] = offline
            summary["flaggedAPs"] = flagged if flagged > 0 else None
        except Exception:
            pass
        
        # Get client counts from query/client
        try:
            client_result = self.client.post("query/client", {"limit": 1})
            summary["totalClients"] = client_result.get("totalCount", 0)
        except Exception:
            pass
        
        # Get zone count
        try:
            zone_result = self.client.get("rkszones")
            if isinstance(zone_result, dict) and "list" in zone_result:
                summary["totalZones"] = zone_result.get("totalCount", len(zone_result["list"]))
        except Exception:
            pass
        
        # Get alarm count
        try:
            alarm_result = self.client.post("alert/alarm/list", {"limit": 1})
            summary["totalAlerts"] = alarm_result.get("totalCount", 0)
        except Exception:
            pass
        
        return summary if summary else {"error": "System summary not available"}

    def get_licenses(self) -> Dict[str, Any]:
        """Get license information.
        
        Multi-version: tries multiple license endpoints.
        
        Returns:
            License details
        """
        endpoints = ["licenses", "system/license", "system/licenses"]
        
        for endpoint in endpoints:
            try:
                return self.client.get(endpoint)
            except Exception:
                continue
        
        return {"error": "License endpoint not available"}

    def get_backup_list(self) -> Dict[str, Any]:
        """Get list of system backups.
        
        Returns:
            List of available backups
        """
        try:
            return self.client.get("system/backup")
        except Exception:
            return {"error": "Backup list not available", "list": []}

    def create_backup(self, backup_name: Optional[str] = None) -> Dict[str, Any]:
        """Create a system backup.
        
        Args:
            backup_name: Optional name for the backup
            
        Returns:
            Backup creation result
        """
        data = {}
        if backup_name:
            data["backupName"] = backup_name
        return self.client.post("system/backup", data)

    def get_cluster_status(self) -> Dict[str, Any]:
        """Get cluster status.
        
        Returns:
            Cluster status information with node states
        """
        # Try cluster/state first (works on 6.x)
        try:
            return self.client.get("cluster/state")
        except Exception:
            pass
        
        # Fallback endpoints
        for endpoint in ["cluster", "controller/cluster"]:
            try:
                return self.client.get(endpoint)
            except Exception:
                continue
        
        return {"error": "Cluster status not available"}

    def get_system_time(self) -> Dict[str, Any]:
        """Get system time configuration.
        
        Returns:
            System time settings
        """
        try:
            return self.client.get("system/systemTime")
        except Exception:
            return {"error": "System time not available"}
