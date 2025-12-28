"""Authentication module for Ruckus vSZ API - AAA, RADIUS, and Hotspot management."""

from typing import TYPE_CHECKING, Any, Dict, Optional

if TYPE_CHECKING:
    from ..api_client import RuckusVSZClient


class AuthenticationModule:
    """Authentication API module for AAA, RADIUS, and Hotspot services."""

    def __init__(self, client: "RuckusVSZClient"):
        """Initialize Authentication module."""
        self.client = client

    def list_radius_profiles(self, zone_id: str) -> Dict[str, Any]:
        """List RADIUS authentication profiles.
        
        Args:
            zone_id: Zone UUID
            
        Returns:
            List of RADIUS profiles
        """
        return self.client.get(f"rkszones/{zone_id}/aaa/radius")

    def get_radius_profile(self, zone_id: str, profile_id: str) -> Dict[str, Any]:
        """Get RADIUS profile details.
        
        Args:
            zone_id: Zone UUID
            profile_id: RADIUS profile UUID
            
        Returns:
            RADIUS profile details
        """
        return self.client.get(f"rkszones/{zone_id}/aaa/radius/{profile_id}")

    def create_radius_profile(
        self,
        zone_id: str,
        name: str,
        primary_server: str,
        primary_port: int = 1812,
        primary_shared_secret: str = "",
        secondary_server: Optional[str] = None,
        secondary_port: Optional[int] = None,
        secondary_shared_secret: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Create RADIUS authentication profile.
        
        Args:
            zone_id: Zone UUID
            name: Profile name
            primary_server: Primary RADIUS server IP
            primary_port: Primary server port
            primary_shared_secret: Primary server shared secret
            secondary_server: Secondary RADIUS server IP
            secondary_port: Secondary server port
            secondary_shared_secret: Secondary server shared secret
            **kwargs: Additional parameters
            
        Returns:
            Created profile details
        """
        data = {
            "name": name,
            "primary": {
                "ip": primary_server,
                "port": primary_port,
                "sharedSecret": primary_shared_secret
            }
        }
        
        if secondary_server:
            data["secondary"] = {
                "ip": secondary_server,
                "port": secondary_port or 1812,
                "sharedSecret": secondary_shared_secret or ""
            }
            
        data.update(kwargs)
        return self.client.post(f"rkszones/{zone_id}/aaa/radius", data)

    def update_radius_profile(
        self,
        zone_id: str,
        profile_id: str,
        name: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Update RADIUS profile.
        
        Args:
            zone_id: Zone UUID
            profile_id: RADIUS profile UUID
            name: New profile name
            **kwargs: Additional parameters
            
        Returns:
            Update result
        """
        data = {}
        if name:
            data["name"] = name
        data.update(kwargs)
        return self.client.patch(f"rkszones/{zone_id}/aaa/radius/{profile_id}", data)

    def delete_radius_profile(self, zone_id: str, profile_id: str) -> Dict[str, Any]:
        """Delete RADIUS profile.
        
        Args:
            zone_id: Zone UUID
            profile_id: RADIUS profile UUID
            
        Returns:
            Delete result
        """
        return self.client.delete(f"rkszones/{zone_id}/aaa/radius/{profile_id}")

    def list_hotspot_profiles(self, zone_id: str) -> Dict[str, Any]:
        """List Hotspot profiles.
        
        Args:
            zone_id: Zone UUID
            
        Returns:
            List of Hotspot profiles
        """
        return self.client.get(f"rkszones/{zone_id}/portals/hotspot")

    def get_hotspot_profile(self, zone_id: str, profile_id: str) -> Dict[str, Any]:
        """Get Hotspot profile details.
        
        Args:
            zone_id: Zone UUID
            profile_id: Hotspot profile UUID
            
        Returns:
            Hotspot profile details
        """
        return self.client.get(f"rkszones/{zone_id}/portals/hotspot/{profile_id}")

    def create_hotspot_profile(
        self,
        zone_id: str,
        name: str,
        redirect_url: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Create Hotspot profile.
        
        Args:
            zone_id: Zone UUID
            name: Profile name
            redirect_url: Redirect URL after authentication
            **kwargs: Additional parameters
            
        Returns:
            Created profile details
        """
        data = {"name": name}
        if redirect_url:
            data["redirectUrl"] = redirect_url
        data.update(kwargs)
        return self.client.post(f"rkszones/{zone_id}/portals/hotspot", data)

    def list_guest_access_profiles(self, zone_id: str) -> Dict[str, Any]:
        """List Guest Access profiles.
        
        Args:
            zone_id: Zone UUID
            
        Returns:
            List of Guest Access profiles
        """
        return self.client.get(f"rkszones/{zone_id}/portals/guestAccess")
