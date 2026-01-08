"""Clients module for Ruckus vSZ API - Client management and monitoring.

Multi-version support:
- vSZ 6.x: Uses query/client endpoint for listing
- vSZ 7.x+: Uses clients endpoint directly
"""

from typing import TYPE_CHECKING, Any, Dict, Optional

if TYPE_CHECKING:
    from ..api_client import RuckusVSZClient


class ClientsModule:
    """Clients API module for wireless client management."""

    def __init__(self, client: "RuckusVSZClient"):
        """Initialize Clients module."""
        self.client = client

    def list_clients(
        self,
        index: Optional[int] = None,
        list_size: Optional[int] = None,
    ) -> Dict[str, Any]:
        """List all connected clients.
        
        Multi-version: uses query/client with 'limit' param for vSZ 6.x.
        
        Args:
            index: Starting index for pagination
            list_size: Number of items to return (default: 100)
            
        Returns:
            List of clients
        """
        # Use query endpoint (works on all versions)
        # vSZ 6.x uses 'limit' parameter, not 'listSize'
        data: Dict[str, Any] = {}
        if list_size is not None:
            data["limit"] = list_size
        else:
            data["limit"] = 100  # Default to 100 for better usability
        
        try:
            return self.client.post("query/client", data)
        except Exception:
            # Fallback to direct endpoint (vSZ 7.x+)
            params = {}
            if index is not None:
                params["index"] = index
            if list_size is not None:
                params["listSize"] = list_size
            return self.client.get("clients", params=params)

    def get_client(self, client_mac: str) -> Dict[str, Any]:
        """Get client details by MAC address.
        
        Multi-version: tries clients/{mac} first, then query/client with MAC filter.
        
        Args:
            client_mac: Client MAC address
            
        Returns:
            Client details
        """
        # Try direct endpoint first (vSZ 7.x+)
        try:
            return self.client.get(f"clients/{client_mac}")
        except Exception:
            pass
        
        # Fallback: query with MAC filter (vSZ 6.x)
        # vSZ 6.x uses 'limit' not 'listSize'
        try:
            result = self.client.post("query/client", {
                "filters": [{"type": "MAC", "value": client_mac}],
                "limit": 1
            })
            if result.get("list") and len(result["list"]) > 0:
                return result["list"][0]
        except Exception:
            pass
        
        # Try fullTextSearch as last resort
        try:
            result = self.client.post("query/client", {
                "fullTextSearch": {"type": "OR", "value": client_mac},
                "limit": 10
            })
            if result.get("list"):
                # Find exact MAC match
                for item in result["list"]:
                    if item.get("clientMac", "").lower() == client_mac.lower():
                        return item
                # Return first match if no exact
                if result["list"]:
                    return result["list"][0]
        except Exception:
            pass
        
        return {"error": f"Client {client_mac} not found"}

    def disconnect_client(self, client_mac: str) -> Dict[str, Any]:
        """Disconnect a client.
        
        Args:
            client_mac: Client MAC address
            
        Returns:
            Disconnect result
        """
        return self.client.delete(f"clients/{client_mac}")

    def query_clients(
        self,
        filters: Optional[Dict[str, Any]] = None,
        full_text_search: Optional[str] = None,
        index: Optional[int] = None,
        list_size: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Query clients with filters.
        
        Args:
            filters: Filter criteria (e.g., {"type": "SSID", "value": "Guest"})
            full_text_search: Search string
            index: Starting index for pagination
            list_size: Number of items to return (uses 'limit' for vSZ 6.x)
            
        Returns:
            Filtered list of clients
        """
        data: Dict[str, Any] = {}
        if filters:
            # Ensure filters is in correct format
            if isinstance(filters, dict) and "type" in filters:
                data["filters"] = [filters]
            else:
                data["filters"] = [filters] if isinstance(filters, dict) else filters
        if full_text_search:
            data["fullTextSearch"] = {"type": "AND", "value": full_text_search}
        # vSZ 6.x uses 'limit' parameter
        if list_size is not None:
            data["limit"] = list_size
            
        return self.client.post("query/client", data)

    def get_client_session_history(
        self,
        client_mac: str,
        index: Optional[int] = None,
        list_size: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Get client session history.
        
        Args:
            client_mac: Client MAC address
            index: Starting index for pagination
            list_size: Number of items to return
            
        Returns:
            Client session history
        """
        params = {}
        if index is not None:
            params["index"] = index
        if list_size is not None:
            params["listSize"] = list_size
        return self.client.get(f"clients/{client_mac}/sessionHistory", params=params)
