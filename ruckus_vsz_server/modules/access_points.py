"""Access Points module for Ruckus vSZ API - AP management."""

from typing import TYPE_CHECKING, Any, Dict, Optional

if TYPE_CHECKING:
    from ..api_client import RuckusVSZClient


class AccessPointsModule:
    """Access Points API module."""

    def __init__(self, client: "RuckusVSZClient"):
        """Initialize Access Points module."""
        self.client = client

    def list_aps(
        self,
        index: Optional[int] = None,
        list_size: Optional[int] = None,
    ) -> Dict[str, Any]:
        """List all access points.
        
        Args:
            index: Starting index for pagination
            list_size: Number of items to return
            
        Returns:
            List of access points
        """
        params = {}
        if index is not None:
            params["index"] = index
        if list_size is not None:
            params["listSize"] = list_size
        return self.client.get("aps", params=params)

    def get_ap(self, ap_mac: str) -> Dict[str, Any]:
        """Get AP details by MAC address.
        
        Args:
            ap_mac: AP MAC address
            
        Returns:
            AP details
        """
        return self.client.get(f"aps/{ap_mac}")

    def update_ap(
        self,
        ap_mac: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        location: Optional[str] = None,
        latitude: Optional[float] = None,
        longitude: Optional[float] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Update AP configuration.
        
        Args:
            ap_mac: AP MAC address
            name: AP name
            description: AP description
            location: Location description
            latitude: GPS latitude
            longitude: GPS longitude
            **kwargs: Additional AP parameters
            
        Returns:
            Update result
        """
        data = {}
        if name:
            data["name"] = name
        if description:
            data["description"] = description
        if location:
            data["location"] = location
        if latitude is not None:
            data["latitude"] = latitude
        if longitude is not None:
            data["longitude"] = longitude
        data.update(kwargs)
        return self.client.patch(f"aps/{ap_mac}", data)

    def delete_ap(self, ap_mac: str) -> Dict[str, Any]:
        """Delete/remove AP from management.
        
        Args:
            ap_mac: AP MAC address
            
        Returns:
            Delete result
        """
        return self.client.delete(f"aps/{ap_mac}")

    def reboot_ap(self, ap_mac: str) -> Dict[str, Any]:
        """Reboot an access point.
        
        Args:
            ap_mac: AP MAC address
            
        Returns:
            Reboot command result
        """
        return self.client.put(f"aps/{ap_mac}/reboot", {})

    def get_ap_operational_info(self, ap_mac: str) -> Dict[str, Any]:
        """Get AP operational information.
        
        Args:
            ap_mac: AP MAC address
            
        Returns:
            AP operational status
        """
        return self.client.get(f"aps/{ap_mac}/operational")

    def get_ap_configuration(self, ap_mac: str) -> Dict[str, Any]:
        """Get AP configuration.
        
        Args:
            ap_mac: AP MAC address
            
        Returns:
            AP configuration
        """
        return self.client.get(f"aps/{ap_mac}/configuration")

    def list_ap_models(self) -> Dict[str, Any]:
        """List supported AP models.
        
        Returns:
            List of AP models
        """
        return self.client.get("apmodels")

    def query_aps(
        self,
        filters: Optional[Dict[str, Any]] = None,
        full_text_search: Optional[str] = None,
        index: Optional[int] = None,
        list_size: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Query APs with filters.
        
        Args:
            filters: Filter criteria (e.g., {"zoneName": "zone1"})
            full_text_search: Search string
            index: Starting index for pagination
            list_size: Number of items to return
            
        Returns:
            Filtered list of APs
        """
        data: Dict[str, Any] = {}
        if filters:
            data["filters"] = [filters]
        if full_text_search:
            data["fullTextSearch"] = {"type": "AND", "value": full_text_search}
        
        params = {}
        if index is not None:
            params["index"] = index
        if list_size is not None:
            params["listSize"] = list_size
            
        return self.client.post("query/ap", data)

    def get_ap_clients(self, ap_mac: str) -> Dict[str, Any]:
        """Get clients connected to an AP.
        
        Args:
            ap_mac: AP MAC address
            
        Returns:
            List of connected clients
        """
        return self.client.get(f"aps/{ap_mac}/clients")

    def get_ap_alarm_summary(self, ap_mac: str) -> Dict[str, Any]:
        """Get AP alarm summary.
        
        Args:
            ap_mac: AP MAC address
            
        Returns:
            AP alarm summary
        """
        return self.client.get(f"aps/{ap_mac}/alarms")

    def set_ap_location(
        self,
        ap_mac: str,
        latitude: float,
        longitude: float,
    ) -> Dict[str, Any]:
        """Set AP GPS location.
        
        Args:
            ap_mac: AP MAC address
            latitude: GPS latitude
            longitude: GPS longitude
            
        Returns:
            Update result
        """
        data = {
            "latitude": latitude,
            "longitude": longitude
        }
        return self.client.patch(f"aps/{ap_mac}/location", data)
