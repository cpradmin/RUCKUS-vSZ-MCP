"""Configuration management for Ruckus vSZ MCP Server."""

import os
from dataclasses import dataclass


@dataclass
class RuckusVSZConfig:
    """Ruckus vSZ API configuration."""

    base_url: str
    username: str
    password: str
    verify_ssl: bool = True
    timeout: int = 30
    api_version: str = "v11_0"


def get_ruckus_vsz_config() -> RuckusVSZConfig:
    """Get Ruckus vSZ configuration from environment variables."""
    base_url = os.getenv("RUCKUS_VSZ_URL")
    username = os.getenv("RUCKUS_VSZ_USERNAME")
    password = os.getenv("RUCKUS_VSZ_PASSWORD")

    if not base_url:
        raise ValueError("RUCKUS_VSZ_URL environment variable is required")
    if not username:
        raise ValueError("RUCKUS_VSZ_USERNAME environment variable is required")
    if not password:
        raise ValueError("RUCKUS_VSZ_PASSWORD environment variable is required")

    return RuckusVSZConfig(
        base_url=base_url.rstrip("/"),
        username=username,
        password=password,
        verify_ssl=os.getenv("RUCKUS_VSZ_VERIFY_SSL", "true").lower() != "false",
        timeout=int(os.getenv("RUCKUS_VSZ_TIMEOUT", "30")),
        api_version=os.getenv("RUCKUS_VSZ_API_VERSION", "v11_0"),
    )
