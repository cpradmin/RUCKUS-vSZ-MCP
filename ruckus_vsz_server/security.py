"""Security middleware for Ruckus vSZ MCP Server.

Provides:
- Bearer token authentication
- IP whitelisting
- Rate limiting
"""

from __future__ import annotations

import ipaddress
import logging
import time
from collections import defaultdict
from functools import wraps
from typing import Callable, Dict, List, Optional, Tuple

from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from .config import SecurityConfig

logger = logging.getLogger(__name__)


class RateLimiter:
    """Simple in-memory rate limiter."""
    
    def __init__(self, max_requests: int = 60, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests: Dict[str, List[float]] = defaultdict(list)
    
    def is_allowed(self, client_ip: str) -> Tuple[bool, int]:
        """Check if request is allowed.
        
        Returns:
            Tuple of (allowed, remaining_requests)
        """
        now = time.time()
        window_start = now - self.window_seconds
        
        # Clean old requests
        self.requests[client_ip] = [
            ts for ts in self.requests[client_ip] 
            if ts > window_start
        ]
        
        current_count = len(self.requests[client_ip])
        
        if current_count >= self.max_requests:
            return False, 0
        
        self.requests[client_ip].append(now)
        return True, self.max_requests - current_count - 1
    
    def get_retry_after(self, client_ip: str) -> int:
        """Get seconds until next request is allowed."""
        if not self.requests[client_ip]:
            return 0
        
        oldest_request = min(self.requests[client_ip])
        retry_after = int(oldest_request + self.window_seconds - time.time())
        return max(0, retry_after)


class IPWhitelist:
    """IP whitelist checker."""
    
    def __init__(self, allowed_cidrs: Optional[List[str]] = None):
        self.networks: List[ipaddress.IPv4Network | ipaddress.IPv6Network] = []
        
        if allowed_cidrs:
            for cidr in allowed_cidrs:
                try:
                    network = ipaddress.ip_network(cidr.strip(), strict=False)
                    self.networks.append(network)
                except ValueError as e:
                    logger.warning(f"Invalid CIDR '{cidr}': {e}")
    
    def is_allowed(self, client_ip: str) -> bool:
        """Check if IP is in whitelist."""
        if not self.networks:
            return True  # No whitelist = allow all
        
        try:
            ip = ipaddress.ip_address(client_ip)
            return any(ip in network for network in self.networks)
        except ValueError:
            logger.warning(f"Invalid IP address: {client_ip}")
            return False


def get_client_ip(request: Request) -> str:
    """Extract client IP from request, handling proxies."""
    # Check X-Forwarded-For header
    forwarded_for = request.headers.get("X-Forwarded-For")
    if forwarded_for:
        # Take the first IP (original client)
        return forwarded_for.split(",")[0].strip()
    
    # Check X-Real-IP header
    real_ip = request.headers.get("X-Real-IP")
    if real_ip:
        return real_ip.strip()
    
    # Fall back to direct connection
    if request.client:
        return request.client.host
    
    return "unknown"


def verify_bearer_token(request: Request, expected_token: str) -> bool:
    """Verify Bearer token from Authorization header."""
    auth_header = request.headers.get("Authorization", "")
    
    if not auth_header.startswith("Bearer "):
        return False
    
    token = auth_header[7:]  # Remove "Bearer " prefix
    return token == expected_token


class SecurityMiddleware(BaseHTTPMiddleware):
    """FastAPI middleware for security checks."""
    
    def __init__(self, app, security_config: SecurityConfig):
        super().__init__(app)
        self.config = security_config
        
        # Initialize rate limiter
        self.rate_limiter = RateLimiter(
            max_requests=security_config.rate_limit_per_minute,
            window_seconds=60
        )
        
        # Initialize IP whitelist
        self.ip_whitelist = IPWhitelist(security_config.allowed_ips)
        
        logger.info(f"Security middleware initialized:")
        logger.info(f"  - API key required: {bool(security_config.api_key)}")
        logger.info(f"  - IP whitelist: {len(self.ip_whitelist.networks)} networks")
        logger.info(f"  - Rate limit: {security_config.rate_limit_per_minute}/min")
    
    async def dispatch(self, request: Request, call_next):
        client_ip = get_client_ip(request)
        path = request.url.path
        
        # Skip security for public endpoints
        if self._is_public_endpoint(path):
            return await call_next(request)
        
        # Check IP whitelist
        if not self.ip_whitelist.is_allowed(client_ip):
            logger.warning(f"Access denied for IP {client_ip}: not in whitelist")
            return JSONResponse(
                status_code=status.HTTP_403_FORBIDDEN,
                content={"error": "Access denied", "detail": "IP not allowed"}
            )
        
        # Check rate limit
        allowed, remaining = self.rate_limiter.is_allowed(client_ip)
        if not allowed:
            retry_after = self.rate_limiter.get_retry_after(client_ip)
            logger.warning(f"Rate limit exceeded for IP {client_ip}")
            return JSONResponse(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                content={"error": "Rate limit exceeded", "retry_after": retry_after},
                headers={"Retry-After": str(retry_after)}
            )
        
        # Check Bearer token if configured
        if self.config.api_key:
            if not verify_bearer_token(request, self.config.api_key):
                logger.warning(f"Unauthorized access attempt from {client_ip} to {path}")
                return JSONResponse(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    content={"error": "Unauthorized", "detail": "Invalid or missing Bearer token"},
                    headers={"WWW-Authenticate": "Bearer"}
                )
        
        # Add rate limit headers to response
        response = await call_next(request)
        response.headers["X-RateLimit-Limit"] = str(self.config.rate_limit_per_minute)
        response.headers["X-RateLimit-Remaining"] = str(remaining)
        
        return response
    
    def _is_public_endpoint(self, path: str) -> bool:
        """Check if endpoint is public (no auth required)."""
        return any(
            path == endpoint or path.startswith(endpoint + "/")
            for endpoint in self.config.public_endpoints
        )


def require_auth(security_config: SecurityConfig):
    """Decorator for protecting individual endpoints."""
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(request: Request, *args, **kwargs):
            if security_config.api_key:
                if not verify_bearer_token(request, security_config.api_key):
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Invalid or missing Bearer token",
                        headers={"WWW-Authenticate": "Bearer"}
                    )
            return await func(request, *args, **kwargs)
        return wrapper
    return decorator
