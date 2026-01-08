"""Configuration management for Ruckus vSZ MCP Server.

Supports:
- Multi-controller configuration via config.yaml
- Per-controller credentials via environment variables
- Bearer token authentication
- IP whitelisting
- Rate limiting
"""

from __future__ import annotations

import os
import logging
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

import yaml

logger = logging.getLogger(__name__)


@dataclass
class ControllerConfig:
    """Configuration for a single vSZ controller."""

    id: str
    name: str
    url: str
    username: str
    password: str
    verify_ssl: bool = False
    timeout: int = 30
    api_version: str = "v11_0"
    tags: List[str] = field(default_factory=list)

    @property
    def base_url(self) -> str:
        """Alias for url (backwards compatibility)."""
        return self.url


@dataclass
class SecurityConfig:
    """Security configuration."""
    
    api_key: Optional[str] = None
    allowed_ips: Optional[List[str]] = None
    rate_limit_per_minute: int = 60
    public_endpoints: List[str] = field(default_factory=lambda: ["/healthz", "/health", "/mcp/info"])


@dataclass
class ServerConfig:
    """Server configuration."""
    
    host: str = "0.0.0.0"
    port: int = 8082
    log_level: str = "INFO"


@dataclass
class AppConfig:
    """Complete application configuration."""
    
    controllers: Dict[str, ControllerConfig] = field(default_factory=dict)
    default_controller_id: str = "default"
    security: SecurityConfig = field(default_factory=SecurityConfig)
    server: ServerConfig = field(default_factory=ServerConfig)


def _resolve_env(env_key: Optional[str], fallback: Optional[str] = None) -> Optional[str]:
    """Resolve value from environment variable."""
    if env_key:
        return os.getenv(env_key, fallback)
    return fallback


def _parse_controller(data: Dict[str, Any]) -> ControllerConfig:
    """Parse controller configuration from dict."""
    controller_id = data.get("id")
    if not controller_id:
        raise ValueError("Controller 'id' is required")
    
    url = data.get("url")
    if not url:
        raise ValueError(f"Controller '{controller_id}': 'url' is required")
    
    # Resolve credentials from env vars
    username = _resolve_env(data.get("username_env"), data.get("username"))
    password = _resolve_env(data.get("password_env"), data.get("password"))
    
    if not username:
        raise ValueError(f"Controller '{controller_id}': username required (set {data.get('username_env')})")
    if not password:
        raise ValueError(f"Controller '{controller_id}': password required (set {data.get('password_env')})")
    
    return ControllerConfig(
        id=controller_id,
        name=data.get("name", controller_id),
        url=url.rstrip("/"),
        username=username,
        password=password,
        verify_ssl=data.get("verify_ssl", False),
        timeout=data.get("timeout", 30),
        api_version=data.get("api_version", "v11_0"),
        tags=data.get("tags", []),
    )


def _parse_security(data: Dict[str, Any]) -> SecurityConfig:
    """Parse security configuration."""
    api_key = _resolve_env(data.get("api_key_env"), data.get("api_key"))
    
    allowed_ips_str = _resolve_env(data.get("allowed_ips_env"), data.get("allowed_ips"))
    allowed_ips = None
    if allowed_ips_str:
        allowed_ips = [ip.strip() for ip in allowed_ips_str.split(",") if ip.strip()]
    
    return SecurityConfig(
        api_key=api_key,
        allowed_ips=allowed_ips,
        rate_limit_per_minute=data.get("rate_limit_per_minute", 60),
        public_endpoints=data.get("public_endpoints", ["/healthz", "/health", "/mcp/info"]),
    )


def _parse_server(data: Dict[str, Any]) -> ServerConfig:
    """Parse server configuration."""
    return ServerConfig(
        host=data.get("host", "0.0.0.0"),
        port=data.get("port", 8082),
        log_level=data.get("log_level", "INFO"),
    )


def load_config(path: str = "config.yaml") -> AppConfig:
    """Load configuration from YAML file.
    
    Args:
        path: Path to config.yaml file
        
    Returns:
        AppConfig with all settings
    """
    # Load YAML file
    try:
        with open(path, "r", encoding="utf-8") as f:
            raw = yaml.safe_load(f) or {}
        logger.info(f"Loaded config from {path}")
    except FileNotFoundError:
        logger.error(f"Config file not found: {path}")
        raise
    except yaml.YAMLError as e:
        logger.error(f"Invalid YAML in {path}: {e}")
        raise
    
    # Parse controllers
    controllers: Dict[str, ControllerConfig] = {}
    if "controllers" not in raw or not raw["controllers"]:
        raise ValueError("No controllers defined in config.yaml")
    
    for ctrl_data in raw["controllers"]:
        try:
            ctrl = _parse_controller(ctrl_data)
            controllers[ctrl.id] = ctrl
            logger.info(f"Loaded controller: {ctrl.id} ({ctrl.name})")
        except ValueError as e:
            logger.error(f"Invalid controller config: {e}")
            raise
    
    # Get default controller
    default_id = raw.get("default_controller")
    if not default_id:
        default_id = list(controllers.keys())[0]
    if default_id not in controllers:
        raise ValueError(f"Default controller '{default_id}' not found in controllers")
    
    # Parse security
    security = SecurityConfig()
    if "security" in raw:
        security = _parse_security(raw["security"])
    
    # Parse server
    server = ServerConfig()
    if "server" in raw:
        server = _parse_server(raw["server"])
    
    return AppConfig(
        controllers=controllers,
        default_controller_id=default_id,
        security=security,
        server=server,
    )


# Global cached config
_app_config: Optional[AppConfig] = None


def get_app_config() -> AppConfig:
    """Get application configuration (cached singleton).
    
    Looks for config.yaml in:
    1. /app/config.yaml (Docker container)
    2. ./config.yaml (current directory)
    3. ../config.yaml (parent directory)
    """
    global _app_config
    if _app_config is not None:
        return _app_config
    
    config_paths = [
        "/app/config.yaml",
        "config.yaml",
        "../config.yaml",
        os.path.join(os.path.dirname(__file__), "..", "config.yaml"),
    ]
    
    for path in config_paths:
        if os.path.exists(path):
            _app_config = load_config(path)
            return _app_config
    
    raise FileNotFoundError(f"Config file not found. Tried: {config_paths}")


def get_ruckus_vsz_config() -> ControllerConfig:
    """Get default controller configuration (backwards compatibility).
    
    Returns the default controller's configuration.
    """
    config = get_app_config()
    return config.controllers[config.default_controller_id]


# Backwards compatibility alias
RuckusVSZConfig = ControllerConfig
