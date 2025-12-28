"""Ruckus vSZ API modules."""

from .system import SystemModule
from .zones import ZonesModule
from .wlans import WLANsModule
from .access_points import AccessPointsModule
from .clients import ClientsModule
from .authentication import AuthenticationModule
from .network import NetworkModule
from .monitoring import MonitoringModule
from .alarms import AlarmModule

__all__ = [
    "SystemModule",
    "ZonesModule",
    "WLANsModule",
    "AccessPointsModule",
    "ClientsModule",
    "AuthenticationModule",
    "NetworkModule",
    "MonitoringModule",
    "AlarmModule",
]
