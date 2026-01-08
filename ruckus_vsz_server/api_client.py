"""Ruckus vSZ API client."""

from typing import Any, Dict, Optional
import logging

import requests

from .config import RuckusVSZConfig
from .modules import (
    SystemModule,
    ZonesModule,
    WLANsModule,
    AccessPointsModule,
    ClientsModule,
    AuthenticationModule,
    NetworkModule,
    MonitoringModule,
    AlarmModule,
)

logger = logging.getLogger(__name__)


class RuckusVSZAPIError(Exception):
    """Ruckus vSZ API error."""

    pass


class RuckusVSZClient:
    """Client for Ruckus vSZ API interactions with session management."""

    def __init__(self, config: RuckusVSZConfig):
        """Initialize Ruckus vSZ client.

        Args:
            config: RuckusVSZConfig instance with API credentials
        """
        self.config = config
        self.base_url = f"{config.base_url}/wsg/api/public/{config.api_version}"
        self.service_ticket: Optional[str] = None

        # Initialize all API modules
        self.system = SystemModule(self)
        self.zones = ZonesModule(self)
        self.wlans = WLANsModule(self)
        self.access_points = AccessPointsModule(self)
        self.clients = ClientsModule(self)
        self.authentication = AuthenticationModule(self)
        self.network = NetworkModule(self)
        self.monitoring = MonitoringModule(self)
        self.alarms = AlarmModule(self)

    def authenticate(self) -> str:
        """Authenticate with Ruckus vSZ and obtain service ticket.

        Returns:
            Service ticket for API requests

        Raises:
            RuckusVSZAPIError: If authentication fails
        """
        url = f"{self.config.base_url}/wsg/api/public/{self.config.api_version}/serviceTicket"
        
        data = {
            "username": self.config.username,
            "password": self.config.password
        }

        try:
            response = requests.post(
                url=url,
                json=data,
                verify=self.config.verify_ssl,
                timeout=self.config.timeout,
                headers={"Content-Type": "application/json;charset=UTF-8"}
            )
            response.raise_for_status()
            result = response.json()
            
            if "serviceTicket" in result:
                self.service_ticket = result["serviceTicket"]
                logger.info("Successfully authenticated with Ruckus vSZ")
                return self.service_ticket
            else:
                raise RuckusVSZAPIError("No service ticket in authentication response")
                
        except requests.exceptions.HTTPError as e:
            try:
                error_data = e.response.json()
                error_msg = error_data.get("message", str(e))
            except Exception:
                error_msg = str(e)
            raise RuckusVSZAPIError(f"Authentication failed: {error_msg}") from e
        except requests.exceptions.RequestException as e:
            raise RuckusVSZAPIError(f"Authentication failed: {e}") from e

    def _ensure_authenticated(self) -> None:
        """Ensure we have a valid service ticket."""
        if not self.service_ticket:
            self.authenticate()

    def _make_request(
        self,
        endpoint: str,
        method: str = "GET",
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Make authenticated request to Ruckus vSZ API.

        Args:
            endpoint: API endpoint path
            method: HTTP method (GET, POST, PATCH, DELETE, PUT)
            data: Request body data
            params: URL query parameters

        Returns:
            API response as dictionary

        Raises:
            RuckusVSZAPIError: If request fails
        """
        self._ensure_authenticated()

        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        # Add service ticket to params
        if params is None:
            params = {}
        params["serviceTicket"] = self.service_ticket

        headers = {"Content-Type": "application/json;charset=UTF-8"}

        try:
            response = requests.request(
                method=method,
                url=url,
                headers=headers,
                json=data,
                params=params,
                verify=self.config.verify_ssl,
                timeout=self.config.timeout,
            )
            response.raise_for_status()
            
            # Some endpoints return empty responses
            if response.status_code == 204 or not response.content:
                return {"success": True}
                
            return response.json()
            
        except requests.exceptions.HTTPError as e:
            # Handle session expiration - re-authenticate and retry once
            if e.response.status_code == 401:
                logger.warning("Session expired, re-authenticating...")
                self.service_ticket = None
                self._ensure_authenticated()
                params["serviceTicket"] = self.service_ticket
                
                # Retry the request once
                try:
                    response = requests.request(
                        method=method,
                        url=url,
                        headers=headers,
                        json=data,
                        params=params,
                        verify=self.config.verify_ssl,
                        timeout=self.config.timeout,
                    )
                    response.raise_for_status()
                    if response.status_code == 204 or not response.content:
                        return {"success": True}
                    return response.json()
                except Exception as retry_error:
                    raise RuckusVSZAPIError(f"API request failed after retry: {retry_error}") from retry_error
            
            # Try to extract error message from response
            try:
                error_data = e.response.json()
                error_msg = error_data.get("message", str(e))
            except Exception:
                error_msg = str(e)
            raise RuckusVSZAPIError(f"API request failed: {error_msg}") from e
        except requests.exceptions.RequestException as e:
            raise RuckusVSZAPIError(f"API request failed: {e}") from e

    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """GET request to Ruckus vSZ API."""
        return self._make_request(endpoint, method="GET", params=params)

    def post(
        self,
        endpoint: str,
        data: Dict[str, Any],
        params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """POST request to Ruckus vSZ API."""
        return self._make_request(endpoint, method="POST", data=data, params=params)

    def try_endpoints(
        self,
        endpoints: list,
        method: str = "GET",
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Try multiple endpoints for multi-version compatibility.
        
        Args:
            endpoints: List of endpoint paths to try in order
            method: HTTP method
            data: Request body data
            params: URL query parameters
            
        Returns:
            Response from first successful endpoint
            
        Raises:
            RuckusVSZAPIError: If all endpoints fail
        """
        last_error = None
        for endpoint in endpoints:
            try:
                return self._make_request(endpoint, method=method, data=data, params=params)
            except RuckusVSZAPIError as e:
                last_error = e
                if "404" not in str(e):
                    raise  # Re-raise non-404 errors
                logger.debug(f"Endpoint {endpoint} not found, trying next...")
                continue
        
        raise RuckusVSZAPIError(f"All endpoints failed. Last error: {last_error}")

    def patch(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """PATCH request to Ruckus vSZ API."""
        return self._make_request(endpoint, method="PATCH", data=data)

    def put(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """PUT request to Ruckus vSZ API."""
        return self._make_request(endpoint, method="PUT", data=data)

    def delete(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """DELETE request to Ruckus vSZ API."""
        return self._make_request(endpoint, method="DELETE", params=params)

    def logout(self) -> None:
        """Logout and invalidate service ticket."""
        if self.service_ticket:
            try:
                self.delete("serviceTicket")
                logger.info("Successfully logged out from Ruckus vSZ")
            except Exception as e:
                logger.warning(f"Logout failed: {e}")
            finally:
                self.service_ticket = None
