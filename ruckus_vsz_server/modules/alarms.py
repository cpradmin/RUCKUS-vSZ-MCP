"""Alarm module for Ruckus vSZ API - Alarm and event management.

Multi-version support:
- vSZ 6.x: Uses query/alarm and alert endpoints
- vSZ 7.x+: Uses alarms endpoint directly
"""

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
        
        Multi-version: tries alert/alarm/list (6.x) first, then query/alarm.
        
        Args:
            index: Starting index for pagination
            list_size: Number of items to return (default: 100)
            
        Returns:
            List of alarms
        """
        # vSZ 6.x uses 'limit' parameter for pagination
        data: Dict[str, Any] = {}
        if list_size is not None:
            data["limit"] = list_size
        else:
            data["limit"] = 100  # Default for better usability
        
        # Try alert/alarm/list first (works on 6.x)
        try:
            return self.client.post("alert/alarm/list", data)
        except Exception:
            # Fallback to query/alarm
            try:
                return self.client.post("query/alarm", data)
            except Exception:
                # Fallback to direct endpoint (7.x+)
                params = {}
                if index is not None:
                    params["index"] = index
                if list_size is not None:
                    params["listSize"] = list_size
                return self.client.get("alarms", params=params)

    def get_alarm(self, alarm_id: str) -> Dict[str, Any]:
        """Get alarm details.
        
        Multi-version: tries multiple endpoints, then queries by ID.
        
        Args:
            alarm_id: Alarm UUID
            
        Returns:
            Alarm details
        """
        # Try direct endpoints
        for endpoint in [f"alarms/{alarm_id}", f"alert/alarm/{alarm_id}"]:
            try:
                return self.client.get(endpoint)
            except Exception:
                continue
        
        # Fallback: query alarms and find by ID
        try:
            result = self.client.post("alert/alarm/list", {
                "filters": [{"type": "alarmUUID", "value": alarm_id}],
                "limit": 1
            })
            if result.get("list") and len(result["list"]) > 0:
                return result["list"][0]
        except Exception:
            pass
        
        # Last resort: get all recent alarms and find by ID
        try:
            result = self.client.post("alert/alarm/list", {"limit": 100})
            if result.get("list"):
                for alarm in result["list"]:
                    if alarm.get("id") == alarm_id or alarm.get("alarmUUID") == alarm_id:
                        return alarm
        except Exception:
            pass
        
        return {"error": f"Alarm {alarm_id} not found"}

    def acknowledge_alarm(self, alarm_id: str) -> Dict[str, Any]:
        """Acknowledge an alarm.
        
        Args:
            alarm_id: Alarm UUID
            
        Returns:
            Acknowledge result
        """
        try:
            return self.client.put(f"alarms/{alarm_id}/acknowledge", {})
        except Exception:
            return self.client.put(f"alert/alarm/{alarm_id}/acknowledge", {})

    def clear_alarm(self, alarm_id: str) -> Dict[str, Any]:
        """Clear an alarm.
        
        Args:
            alarm_id: Alarm UUID
            
        Returns:
            Clear result
        """
        try:
            return self.client.delete(f"alarms/{alarm_id}")
        except Exception:
            return self.client.delete(f"alert/alarm/{alarm_id}")

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
            list_size: Number of items to return (uses 'limit' for vSZ 6.x)
            
        Returns:
            Filtered list of alarms
        """
        data: Dict[str, Any] = {}
        if filters:
            if isinstance(filters, dict) and "type" in filters:
                data["filters"] = [filters]
            else:
                data["filters"] = [filters] if isinstance(filters, dict) else filters
        if severity:
            if "filters" not in data:
                data["filters"] = []
            data["filters"].append({"type": "SEVERITY", "value": severity})
        # vSZ 6.x uses 'limit' parameter
        if list_size is not None:
            data["limit"] = list_size
        
        # Try alert/alarm/list first (6.x), then query/alarm
        try:
            return self.client.post("alert/alarm/list", data)
        except Exception:
            return self.client.post("query/alarm", data)

    def get_alarm_summary(self) -> Dict[str, Any]:
        """Get alarm summary by querying alarms.
        
        Multi-version: tries summary endpoints, then falls back to counting.
        
        Returns:
            Alarm summary with counts by severity
        """
        # Try different summary endpoints first
        for endpoint in ["alert/alarmSummary", "alert/alarm/summary", "alarms/summary"]:
            try:
                return self.client.get(endpoint)
            except Exception:
                continue
        
        # All summary endpoints failed, use alert/alarm/list as fallback
        try:
            result = self.client.post("alert/alarm/list", {"limit": 1})
            total = result.get("totalCount", 0) or result.get("rawDataTotalCount", 0)
            return {
                "totalAlarms": total,
                "note": "Summary computed via alert/alarm/list"
            }
        except Exception:
            # Last resort: return count from list_alarms
            try:
                result = self.list_alarms()
                total = result.get("totalCount", 0) or result.get("rawDataTotalCount", 0)
                return {
                    "totalAlarms": total,
                    "note": "Summary computed via list_alarms"
                }
            except Exception as e:
                return {"error": f"Alarm summary not available: {e}", "totalAlarms": 0}

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
        data: Dict[str, Any] = {}
        if index is not None:
            data["index"] = index
        if list_size is not None:
            data["listSize"] = list_size
        
        try:
            return self.client.post("query/event", data)
        except Exception:
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
            if isinstance(filters, dict) and "type" in filters:
                data["filters"] = [filters]
            else:
                data["filters"] = [filters] if isinstance(filters, dict) else filters
        if event_type:
            if "filters" not in data:
                data["filters"] = []
            data["filters"].append({"type": "EVENT_TYPE", "value": event_type})
        if index is not None:
            data["index"] = index
        if list_size is not None:
            data["listSize"] = list_size
            
        return self.client.post("query/event", data)
