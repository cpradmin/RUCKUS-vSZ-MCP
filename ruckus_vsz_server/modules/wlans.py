"""WLANs module for Ruckus vSZ API - WLAN/SSID management."""

from typing import TYPE_CHECKING, Any, Dict, List, Optional

if TYPE_CHECKING:
    from ..api_client import RuckusVSZClient


class WLANsModule:
    """WLANs API module for managing wireless networks (SSIDs)."""

    def __init__(self, client: "RuckusVSZClient"):
        """Initialize WLANs module."""
        self.client = client

    def list_wlans(
        self,
        zone_id: str,
        index: Optional[int] = None,
        list_size: Optional[int] = None,
    ) -> Dict[str, Any]:
        """List WLANs in a zone.
        
        Args:
            zone_id: Zone UUID
            index: Starting index for pagination
            list_size: Number of items to return
            
        Returns:
            List of WLANs
        """
        params = {}
        if index is not None:
            params["index"] = index
        if list_size is not None:
            params["listSize"] = list_size
        return self.client.get(f"rkszones/{zone_id}/wlans", params=params)

    def get_wlan(self, zone_id: str, wlan_id: str) -> Dict[str, Any]:
        """Get WLAN details.
        
        Args:
            zone_id: Zone UUID
            wlan_id: WLAN UUID
            
        Returns:
            WLAN details
        """
        return self.client.get(f"rkszones/{zone_id}/wlans/{wlan_id}")

    def create_wlan(
        self,
        zone_id: str,
        name: str,
        ssid: str,
        authentication_type: str = "Open",
        encryption_method: Optional[str] = None,
        passphrase: Optional[str] = None,
        vlan_id: Optional[int] = None,
        description: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Create a new WLAN.
        
        Args:
            zone_id: Zone UUID
            name: WLAN name
            ssid: SSID broadcast name
            authentication_type: Authentication type (Open, WPA2, WPA3, etc.)
            encryption_method: Encryption method (AES, TKIP, etc.)
            passphrase: WPA passphrase
            vlan_id: VLAN ID
            description: WLAN description
            **kwargs: Additional WLAN parameters
            
        Returns:
            Created WLAN details
        """
        data = {
            "name": name,
            "ssid": ssid,
        }
        
        # Authentication settings
        auth_data: Dict[str, Any] = {"type": authentication_type}
        if encryption_method:
            auth_data["encryption"] = {"method": encryption_method}
        if passphrase:
            auth_data["passphrase"] = passphrase
        data["authentication"] = auth_data
        
        if vlan_id:
            data["vlan"] = {"id": vlan_id}
        if description:
            data["description"] = description
            
        data.update(kwargs)
        return self.client.post(f"rkszones/{zone_id}/wlans", data)

    def update_wlan(
        self,
        zone_id: str,
        wlan_id: str,
        name: Optional[str] = None,
        ssid: Optional[str] = None,
        description: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Update WLAN.
        
        Args:
            zone_id: Zone UUID
            wlan_id: WLAN UUID
            name: New WLAN name
            ssid: New SSID
            description: New description
            **kwargs: Additional WLAN parameters
            
        Returns:
            Update result
        """
        data = {}
        if name:
            data["name"] = name
        if ssid:
            data["ssid"] = ssid
        if description:
            data["description"] = description
        data.update(kwargs)
        return self.client.patch(f"rkszones/{zone_id}/wlans/{wlan_id}", data)

    def delete_wlan(self, zone_id: str, wlan_id: str) -> Dict[str, Any]:
        """Delete WLAN.
        
        Args:
            zone_id: Zone UUID
            wlan_id: WLAN UUID
            
        Returns:
            Delete result
        """
        return self.client.delete(f"rkszones/{zone_id}/wlans/{wlan_id}")

    def enable_wlan(self, zone_id: str, wlan_id: str) -> Dict[str, Any]:
        """Enable WLAN.
        
        Args:
            zone_id: Zone UUID
            wlan_id: WLAN UUID
            
        Returns:
            Enable result
        """
        return self.client.put(f"rkszones/{zone_id}/wlans/{wlan_id}/enable", {})

    def disable_wlan(self, zone_id: str, wlan_id: str) -> Dict[str, Any]:
        """Disable WLAN.
        
        Args:
            zone_id: Zone UUID
            wlan_id: WLAN UUID
            
        Returns:
            Disable result
        """
        return self.client.put(f"rkszones/{zone_id}/wlans/{wlan_id}/disable", {})

    def get_wlan_encryption(self, zone_id: str, wlan_id: str) -> Dict[str, Any]:
        """Get WLAN encryption settings.
        
        Args:
            zone_id: Zone UUID
            wlan_id: WLAN UUID
            
        Returns:
            Encryption settings
        """
        return self.client.get(f"rkszones/{zone_id}/wlans/{wlan_id}/encryption")

    def update_wlan_encryption(
        self,
        zone_id: str,
        wlan_id: str,
        method: str,
        passphrase: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Update WLAN encryption settings.
        
        Args:
            zone_id: Zone UUID
            wlan_id: WLAN UUID
            method: Encryption method (AES, TKIP, Auto)
            passphrase: WPA passphrase
            
        Returns:
            Update result
        """
        data = {"method": method}
        if passphrase:
            data["passphrase"] = passphrase
        return self.client.patch(f"rkszones/{zone_id}/wlans/{wlan_id}/encryption", data)

    def get_wlan_schedule(self, zone_id: str, wlan_id: str) -> Dict[str, Any]:
        """Get WLAN schedule.
        
        Args:
            zone_id: Zone UUID
            wlan_id: WLAN UUID
            
        Returns:
            WLAN schedule settings
        """
        return self.client.get(f"rkszones/{zone_id}/wlans/{wlan_id}/schedule")
