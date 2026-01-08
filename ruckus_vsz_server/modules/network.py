"""Network module for Ruckus vSZ API - VLAN, QoS, and network services."""

from typing import TYPE_CHECKING, Any, Dict, Optional

if TYPE_CHECKING:
    from ..api_client import RuckusVSZClient


class NetworkModule:
    """Network API module for VLAN, QoS, and network configuration."""

    def __init__(self, client: "RuckusVSZClient"):
        """Initialize Network module."""
        self.client = client

    def list_vlan_pools(self, zone_id: str) -> Dict[str, Any]:
        """List VLAN pools.
        
        Multi-version: tries multiple endpoints for different vSZ versions.
        
        Args:
            zone_id: Zone UUID
            
        Returns:
            List of VLAN pools
        """
        # Try different endpoint patterns
        for endpoint in [
            f"rkszones/{zone_id}/vlanpools",
            f"rkszones/{zone_id}/vlanPoolProfiles",
            f"rkszones/{zone_id}/diffServ/vlanpoolprofiles"
        ]:
            try:
                return self.client.get(endpoint)
            except Exception:
                continue
        
        return {
            "list": [],
            "totalCount": 0,
            "error": "VLAN pools not available. This feature may require vSZ 7.x+ or different license."
        }

    def get_vlan_pool(self, zone_id: str, pool_id: str) -> Dict[str, Any]:
        """Get VLAN pool details.
        
        Args:
            zone_id: Zone UUID
            pool_id: VLAN pool UUID
            
        Returns:
            VLAN pool details
        """
        return self.client.get(f"rkszones/{zone_id}/vlanpools/{pool_id}")

    def create_vlan_pool(
        self,
        zone_id: str,
        name: str,
        vlan_list: str,
        description: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Create VLAN pool.
        
        Args:
            zone_id: Zone UUID
            name: Pool name
            vlan_list: Comma-separated VLAN IDs (e.g., "10,20,30" or "10-20")
            description: Pool description
            
        Returns:
            Created pool details
        """
        data = {
            "name": name,
            "vlanList": vlan_list
        }
        if description:
            data["description"] = description
        return self.client.post(f"rkszones/{zone_id}/vlanpools", data)

    def delete_vlan_pool(self, zone_id: str, pool_id: str) -> Dict[str, Any]:
        """Delete VLAN pool.
        
        Args:
            zone_id: Zone UUID
            pool_id: VLAN pool UUID
            
        Returns:
            Delete result
        """
        return self.client.delete(f"rkszones/{zone_id}/vlanpools/{pool_id}")

    def list_l2acl_profiles(self, zone_id: str) -> Dict[str, Any]:
        """List Layer 2 ACL profiles.
        
        Args:
            zone_id: Zone UUID
            
        Returns:
            List of L2 ACL profiles
        """
        return self.client.get(f"rkszones/{zone_id}/l2acl")

    def get_l2acl_profile(self, zone_id: str, profile_id: str) -> Dict[str, Any]:
        """Get L2 ACL profile details.
        
        Args:
            zone_id: Zone UUID
            profile_id: L2 ACL profile UUID
            
        Returns:
            L2 ACL profile details
        """
        return self.client.get(f"rkszones/{zone_id}/l2acl/{profile_id}")

    def list_l3acl_profiles(self, zone_id: str) -> Dict[str, Any]:
        """List Layer 3 ACL profiles.
        
        Args:
            zone_id: Zone UUID
            
        Returns:
            List of L3 ACL profiles
        """
        return self.client.get(f"rkszones/{zone_id}/l3acl")

    def get_l3acl_profile(self, zone_id: str, profile_id: str) -> Dict[str, Any]:
        """Get L3 ACL profile details.
        
        Args:
            zone_id: Zone UUID
            profile_id: L3 ACL profile UUID
            
        Returns:
            L3 ACL profile details
        """
        return self.client.get(f"rkszones/{zone_id}/l3acl/{profile_id}")

    def list_qos_profiles(self, zone_id: str) -> Dict[str, Any]:
        """List QoS profiles.
        
        Multi-version: tries multiple endpoints for different vSZ versions.
        
        Args:
            zone_id: Zone UUID
            
        Returns:
            List of QoS profiles
        """
        # Try different endpoint patterns
        for endpoint in [
            f"rkszones/{zone_id}/qos",
            f"rkszones/{zone_id}/diffServ/qos",
            f"rkszones/{zone_id}/qosProfiles"
        ]:
            try:
                return self.client.get(endpoint)
            except Exception:
                continue
        
        return {
            "list": [],
            "totalCount": 0,
            "error": "QoS profiles not available. This feature may require vSZ 7.x+ or different license."
        }

    def get_qos_profile(self, zone_id: str, profile_id: str) -> Dict[str, Any]:
        """Get QoS profile details.
        
        Args:
            zone_id: Zone UUID
            profile_id: QoS profile UUID
            
        Returns:
            QoS profile details
        """
        return self.client.get(f"rkszones/{zone_id}/qos/{profile_id}")

    def list_application_policies(self, zone_id: str) -> Dict[str, Any]:
        """List application policies.
        
        Args:
            zone_id: Zone UUID
            
        Returns:
            List of application policies
        """
        return self.client.get(f"rkszones/{zone_id}/applicationPolicyProfile")

    def list_dhcp_profiles(self, zone_id: str) -> Dict[str, Any]:
        """List DHCP profiles.
        
        Args:
            zone_id: Zone UUID
            
        Returns:
            List of DHCP profiles
        """
        return self.client.get(f"rkszones/{zone_id}/dhcpProfiles")

    def get_dhcp_profile(self, zone_id: str, profile_id: str) -> Dict[str, Any]:
        """Get DHCP profile details.
        
        Args:
            zone_id: Zone UUID
            profile_id: DHCP profile UUID
            
        Returns:
            DHCP profile details
        """
        return self.client.get(f"rkszones/{zone_id}/dhcpProfiles/{profile_id}")
