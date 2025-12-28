"""Clients module for Ruckus vSZ API - Client management and monitoring."""

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
        
        Args:
            index: Starting index for pagination
            list_size: Number of items to return
            
        Returns:
            List of clients
        """
        params = {}
        if index is not None:
            params["index"] = index
        if list_size is not None:
            params["listSize"] = list_size
        return self.client.get("clients", params=params)

    def get_client(self, client_mac: str) -> Dict[str, Any]:
        """Get client details by MAC address.
        
        Args:
            client_mac: Client MAC address
            
        Returns:
            Client details
        """
        return self.client.get(f"clients/{client_mac}")

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
            filters: Filter criteria (e.g., {"ssid": "Guest"})
            full_text_search: Search string
            index: Starting index for pagination
            list_size: Number of items to return
            
        Returns:
            Filtered list of clients
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
