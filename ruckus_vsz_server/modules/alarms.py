"""Alarm module for Ruckus vSZ API - Alarm and event management."""

from typing import TYPE_CHECKING, Any, Dict, Optional

if TYPE_CHECKING:
    from ..api_client import RuckusVSZClient


class AlarmModule:
    """Alarm API module for managing alarms and events."""

    def __init__(self, client: "RuckusVSZClient"):
        """Initialize Alarm module."""
        self.client = client

    def list_alarms(
        self,
        index: Optional[int] = None,
        list_size: Optional[int] = None,
    ) -> Dict[str, Any]:
        """List all alarms.
        
        Args:
            index: Starting index for pagination
            list_size: Number of items to return
            
        Returns:
            List of alarms
        """
        params = {}
        if index is not None:
            params["index"] = index
        if list_size is not None:
            params["listSize"] = list_size
        return self.client.get("alarms", params=params)

    def get_alarm(self, alarm_id: str) -> Dict[str, Any]:
        """Get alarm details.
        
        Args:
            alarm_id: Alarm UUID
            
        Returns:
            Alarm details
        """
        return self.client.get(f"alarms/{alarm_id}")

    def acknowledge_alarm(self, alarm_id: str) -> Dict[str, Any]:
        """Acknowledge an alarm.
        
        Args:
            alarm_id: Alarm UUID
            
        Returns:
            Acknowledge result
        """
        return self.client.put(f"alarms/{alarm_id}/acknowledge", {})

    def clear_alarm(self, alarm_id: str) -> Dict[str, Any]:
        """Clear an alarm.
        
        Args:
            alarm_id: Alarm UUID
            
        Returns:
            Clear result
        """
        return self.client.delete(f"alarms/{alarm_id}")

    def query_alarms(
        self,
        filters: Optional[Dict[str, Any]] = None,
        severity: Optional[str] = None,
        index: Optional[int] = None,
        list_size: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Query alarms with filters.
        
        Args:
            filters: Filter criteria
            severity: Alarm severity (Critical, Major, Minor, Warning, Info)
            index: Starting index for pagination
            list_size: Number of items to return
            
        Returns:
            Filtered list of alarms
        """
        data: Dict[str, Any] = {}
        if filters:
            data["filters"] = [filters]
        if severity:
            if "filters" not in data:
                data["filters"] = []
            data["filters"].append({"type": "SEVERITY", "value": severity})
        
        params = {}
        if index is not None:
            params["index"] = index
        if list_size is not None:
            params["listSize"] = list_size
            
        return self.client.post("query/alarm", data)

    def get_alarm_summary(self) -> Dict[str, Any]:
        """Get alarm summary.
        
        Returns:
            Alarm summary with counts by severity
        """
        return self.client.get("alarms/summary")

    def list_events(
        self,
        index: Optional[int] = None,
        list_size: Optional[int] = None,
    ) -> Dict[str, Any]:
        """List system events.
        
        Args:
            index: Starting index for pagination
            list_size: Number of items to return
            
        Returns:
            List of events
        """
        params = {}
        if index is not None:
            params["index"] = index
        if list_size is not None:
            params["listSize"] = list_size
        return self.client.get("events", params=params)

    def query_events(
        self,
        filters: Optional[Dict[str, Any]] = None,
        event_type: Optional[str] = None,
        index: Optional[int] = None,
        list_size: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Query events with filters.
        
        Args:
            filters: Filter criteria
            event_type: Event type filter
            index: Starting index for pagination
            list_size: Number of items to return
            
        Returns:
            Filtered list of events
        """
        data: Dict[str, Any] = {}
        if filters:
            data["filters"] = [filters]
        if event_type:
            if "filters" not in data:
                data["filters"] = []
            data["filters"].append({"type": "EVENT_TYPE", "value": event_type})
        
        params = {}
        if index is not None:
            params["index"] = index
        if list_size is not None:
            params["listSize"] = list_size
            
        return self.client.post("query/event", data)
