"""Multi-controller manager for Ruckus vSZ MCP Server.

Manages multiple vSZ controller connections with individual credentials.
"""

from __future__ import annotations

import logging
from typing import Dict, List, Optional

from .api_client import RuckusVSZClient
from .config import AppConfig, RuckusVSZConfig

logger = logging.getLogger(__name__)


class ControllerManager:
    """Manages multiple vSZ controller connections."""
    
    def __init__(self, app_config: AppConfig):
        self.config = app_config
        self.clients: Dict[str, RuckusVSZClient] = {}
        self._initialize_clients()
    
    def _initialize_clients(self):
        """Initialize API clients for all configured controllers."""
        for controller_id, controller_config in self.config.controllers.items():
            try:
                client = RuckusVSZClient(controller_config)
                self.clients[controller_id] = client
                logger.info(f"Initialized controller: {controller_id} ({controller_config.name})")
            except Exception as e:
                logger.error(f"Failed to initialize controller {controller_id}: {e}")
    
    def get_client(self, controller_id: Optional[str] = None) -> RuckusVSZClient:
        """Get API client for specified controller.
        
        Args:
            controller_id: Controller ID, or None for default
            
        Returns:
            RuckusVSZClient instance
            
        Raises:
            ValueError: If controller not found
        """
        if controller_id is None:
            controller_id = self.config.default_controller_id
        
        if controller_id not in self.clients:
            available = list(self.clients.keys())
            raise ValueError(
                f"Controller '{controller_id}' not found. "
                f"Available controllers: {available}"
            )
        
        return self.clients[controller_id]
    
    def get_default_client(self) -> RuckusVSZClient:
        """Get the default controller client."""
        return self.get_client(self.config.default_controller_id)
    
    def list_controllers(self) -> List[Dict]:
        """List all available controllers.
        
        Returns:
            List of controller info dicts
        """
        controllers = []
        for controller_id, config in self.config.controllers.items():
            controllers.append({
                "id": controller_id,
                "name": config.name,
                "url": config.base_url,
                "api_version": config.api_version,
                "tags": config.tags,
                "is_default": controller_id == self.config.default_controller_id,
                "connected": controller_id in self.clients,
            })
        return controllers
    
    def get_controller_info(self, controller_id: Optional[str] = None) -> Dict:
        """Get info for a specific controller.
        
        Args:
            controller_id: Controller ID, or None for default
            
        Returns:
            Controller info dict
        """
        if controller_id is None:
            controller_id = self.config.default_controller_id
        
        if controller_id not in self.config.controllers:
            raise ValueError(f"Controller '{controller_id}' not found")
        
        config = self.config.controllers[controller_id]
        return {
            "id": controller_id,
            "name": config.name,
            "url": config.base_url,
            "api_version": config.api_version,
            "tags": config.tags,
            "is_default": controller_id == self.config.default_controller_id,
            "connected": controller_id in self.clients,
        }
    
    @property
    def controller_count(self) -> int:
        """Get number of configured controllers."""
        return len(self.clients)
    
    @property
    def controller_ids(self) -> List[str]:
        """Get list of controller IDs."""
        return list(self.clients.keys())
