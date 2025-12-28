"""Zones module for Ruckus vSZ API - Zone and AP Zone management."""

from typing import TYPE_CHECKING, Any, Dict, Optional

if TYPE_CHECKING:
    from ..api_client import RuckusVSZClient


class ZonesModule:
    """Zones API module for managing AP zones and domains."""

    def __init__(self, client: "RuckusVSZClient"):
        """Initialize Zones module."""
        self.client = client

    def list_zones(
        self,
        index: Optional[int] = None,
        list_size: Optional[int] = None,
    ) -> Dict[str, Any]:
        """List all zones.
        
        Args:
            index: Starting index for pagination
            list_size: Number of items to return
            
        Returns:
            List of zones
        """
        params = {}
        if index is not None:
            params["index"] = index
        if list_size is not None:
            params["listSize"] = list_size
        return self.client.get("rkszones", params=params)

    def get_zone(self, zone_id: str) -> Dict[str, Any]:
        """Get zone details.
        
        Args:
            zone_id: Zone UUID
            
        Returns:
            Zone details
        """
        return self.client.get(f"rkszones/{zone_id}")

    def create_zone(
        self,
        name: str,
        description: Optional[str] = None,
        domain_id: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Create a new zone.
        
        Args:
            name: Zone name
            description: Zone description
            domain_id: Domain UUID
            **kwargs: Additional zone parameters
            
        Returns:
            Created zone details
        """
        data = {"name": name}
        if description:
            data["description"] = description
        if domain_id:
            data["domainId"] = domain_id
        data.update(kwargs)
        return self.client.post("rkszones", data)

    def update_zone(
        self,
        zone_id: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Update zone.
        
        Args:
            zone_id: Zone UUID
            name: New zone name
            description: New zone description
            **kwargs: Additional zone parameters
            
        Returns:
            Update result
        """
        data = {}
        if name:
            data["name"] = name
        if description:
            data["description"] = description
        data.update(kwargs)
        return self.client.patch(f"rkszones/{zone_id}", data)

    def delete_zone(self, zone_id: str) -> Dict[str, Any]:
        """Delete zone.
        
        Args:
            zone_id: Zone UUID
            
        Returns:
            Delete result
        """
        return self.client.delete(f"rkszones/{zone_id}")

    def get_zone_aps(
        self,
        zone_id: str,
        index: Optional[int] = None,
        list_size: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Get APs in a zone.
        
        Args:
            zone_id: Zone UUID
            index: Starting index for pagination
            list_size: Number of items to return
            
        Returns:
            List of APs in the zone
        """
        params = {}
        if index is not None:
            params["index"] = index
        if list_size is not None:
            params["listSize"] = list_size
        return self.client.get(f"rkszones/{zone_id}/aps", params=params)

    def get_zone_wlans(self, zone_id: str) -> Dict[str, Any]:
        """Get WLANs in a zone.
        
        Args:
            zone_id: Zone UUID
            
        Returns:
            List of WLANs in the zone
        """
        return self.client.get(f"rkszones/{zone_id}/wlans")

    def list_domains(self) -> Dict[str, Any]:
        """List all domains.
        
        Returns:
            List of domains
        """
        return self.client.get("domains")

    def get_domain(self, domain_id: str) -> Dict[str, Any]:
        """Get domain details.
        
        Args:
            domain_id: Domain UUID
            
        Returns:
            Domain details
        """
        return self.client.get(f"domains/{domain_id}")
