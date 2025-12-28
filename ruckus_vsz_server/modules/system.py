"""System module for Ruckus vSZ API - System information and controller management."""

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
        return self.client.get("system")

    def get_system_inventory(self) -> Dict[str, Any]:
        """Get system inventory.
        
        Returns:
            System inventory information
        """
        return self.client.get("system/inventory")

    def get_system_summary(self) -> Dict[str, Any]:
        """Get system summary.
        
        Returns:
            System summary with statistics
        """
        return self.client.get("system/systemSummary")

    def get_licenses(self) -> Dict[str, Any]:
        """Get license information.
        
        Returns:
            License details
        """
        return self.client.get("system/license")

    def get_backup_list(self) -> Dict[str, Any]:
        """Get list of system backups.
        
        Returns:
            List of available backups
        """
        return self.client.get("system/backup")

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
            Cluster status information
        """
        return self.client.get("cluster")

    def get_system_time(self) -> Dict[str, Any]:
        """Get system time configuration.
        
        Returns:
            System time settings
        """
        return self.client.get("system/systemTime")
