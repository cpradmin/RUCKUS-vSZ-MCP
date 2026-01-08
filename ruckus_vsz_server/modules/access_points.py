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
        """List all access points with operational status.
        
        Uses query/ap endpoint to get full operational data including
        connection status, IP, model, firmware version, etc.
        
        Args:
            index: Starting index for pagination
            list_size: Number of items to return (default: 100)
            
        Returns:
            List of access points with status
        """
        # Use query/ap to get operational data (status, connection state, etc.)
        # vSZ 6.x uses 'limit' parameter in body, not 'listSize'
        data: Dict[str, Any] = {}
        if list_size is not None:
            data["limit"] = list_size
        else:
            # Default to 100 items for better usability
            data["limit"] = 100
        
        try:
            return self.client.post("query/ap", data)
        except Exception:
            # Fallback to basic aps endpoint (config only, no status)
            params = {}
            if index is not None:
                params["index"] = index
            if list_size is not None:
                params["listSize"] = list_size
            return self.client.get("aps", params=params)

    def get_ap(self, ap_mac: str) -> Dict[str, Any]:
        """Get AP details by MAC address.
        
        Combines operational data from query/ap with configuration from aps/{mac}.
        
        Args:
            ap_mac: AP MAC address
            
        Returns:
            AP details with both operational status and configuration
        """
        result = {}
        
        # First get operational data from query/ap
        try:
            query_result = self.client.post("query/ap", {
                "filters": [{"type": "AP", "value": ap_mac}],
                "limit": 1
            })
            if query_result.get("list"):
                result.update(query_result["list"][0])
        except Exception:
            pass
        
        # Then get configuration from aps/{mac}
        try:
            config_result = self.client.get(f"aps/{ap_mac}")
            # Merge config into result, but don't overwrite operational data
            for key, value in config_result.items():
                if key not in result or result[key] is None:
                    result[key] = value
        except Exception:
            pass
        
        return result if result else {"error": f"AP {ap_mac} not found"}

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
        
        Multi-version: tries aps/{mac}/operational first, then uses query/ap.
        
        Args:
            ap_mac: AP MAC address
            
        Returns:
            AP operational status
        """
        # Try direct endpoint first (vSZ 7.x+)
        try:
            return self.client.get(f"aps/{ap_mac}/operational")
        except Exception:
            pass
        
        # Fallback: use query/ap with MAC filter (vSZ 6.x)
        try:
            query_result = self.client.post("query/ap", {
                "filters": [{"type": "AP", "value": ap_mac}],
                "limit": 1
            })
            if query_result.get("list"):
                return query_result["list"][0]
        except Exception:
            pass
        
        return {"error": f"AP {ap_mac} operational info not available"}

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
            list_size: Number of items to return (uses 'limit' for vSZ 6.x)
            
        Returns:
            Filtered list of APs
        """
        data: Dict[str, Any] = {}
        if filters:
            data["filters"] = [filters]
        if full_text_search:
            data["fullTextSearch"] = {"type": "AND", "value": full_text_search}
        # vSZ 6.x uses 'limit' parameter, not 'index'/'listSize'
        if list_size is not None:
            data["limit"] = list_size
            
        return self.client.post("query/ap", data)

    def get_ap_clients(self, ap_mac: str) -> Dict[str, Any]:
        """Get clients connected to an AP.
        
        Multi-version: tries aps/{mac}/clients first, then uses query/client with AP filter.
        
        Args:
            ap_mac: AP MAC address
            
        Returns:
            List of connected clients
        """
        # Try direct endpoint first (vSZ 7.x+)
        try:
            return self.client.get(f"aps/{ap_mac}/clients")
        except Exception:
            pass
        
        # Fallback: use query/client with AP filter (vSZ 6.x)
        try:
            return self.client.post("query/client", {
                "filters": [{"type": "APNAME", "value": ap_mac}],
                "limit": 100
            })
        except Exception:
            pass
        
        # Try MAC format variation
        try:
            return self.client.post("query/client", {
                "filters": [{"type": "AP", "value": ap_mac}],
                "limit": 100
            })
        except Exception:
            pass
        
        return {"list": [], "totalCount": 0, "error": f"No clients found for AP {ap_mac}"}

    def get_ap_lldp_neighbors(self, ap_mac: str) -> Dict[str, Any]:
        """Get LLDP neighbors discovered by an AP.
        
        Returns information about network devices (switches, phones, etc.)
        connected to or discovered by the AP via LLDP protocol.
        
        Args:
            ap_mac: AP MAC address
            
        Returns:
            List of LLDP neighbors with interface, chassis ID, system name,
            port description, capabilities, and power information
        """
        return self.client.get(f"aps/{ap_mac}/apLldpNeighbors")

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
