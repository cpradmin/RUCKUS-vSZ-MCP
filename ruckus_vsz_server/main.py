"""Ruckus vSZ MCP Server - Main server implementation with comprehensive API coverage.

Optimized for OpenWebUI integration with compact response modes for LLM token efficiency.
Supports MCP Streamable HTTP protocol (required for OpenWebUI v0.6.31+).

Features:
- Multi-controller support (multiple vSZ instances)
- Bearer token authentication
- IP whitelisting
- Rate limiting
"""

from __future__ import annotations

import asyncio
import json
import logging
import os
import uuid
from typing import Any, Dict, List, Optional, Union

from fastapi import Depends, FastAPI, Query, Request
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel, Field

from .api_client import RuckusVSZAPIError, RuckusVSZClient
from .config import get_app_config, get_ruckus_vsz_config, AppConfig
from .controller_manager import ControllerManager
from .security import SecurityMiddleware, get_client_ip
from .tool_definitions import TOOL_DEFINITIONS
from .tools import RuckusVSZTools

logger = logging.getLogger("ruckus_vsz_mcp_server")

# Server version
SERVER_VERSION = "1.1.0"


def setup_logging() -> None:
    """Setup logging configuration."""
    level = os.environ.get("LOG_LEVEL", "INFO").upper()
    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )


class MCPMetadata(BaseModel):
    """MCP platform metadata."""

    protocol_version: str = "1.0"
    server_name: str = "Ruckus vSZ MCP Server"
    server_version: str = SERVER_VERSION
    capabilities: Dict[str, bool] = Field(
        default_factory=lambda: {
            "tools": True,
            "resources": False,
            "prompts": False,
        }
    )


class AuthzContext(BaseModel):
    """Authorization context."""

    subject: Optional[str] = None
    scopes: Optional[list[str]] = None
    correlation_id: Optional[str] = None


class ToolCallRequest(BaseModel):
    """Tool call request."""

    tool: str
    args: Dict[str, Any] = Field(default_factory=dict)
    context: Optional[AuthzContext] = None
    controller_id: Optional[str] = Field(default=None, description="Target controller ID (multi-vSZ mode)")


class ToolCallResponse(BaseModel):
    """Tool call response."""

    status: str
    data: Optional[Any] = None
    error: Optional[Dict[str, str]] = None
    meta: Optional[Dict[str, str]] = None


class ToolInfo(BaseModel):
    """Tool information - full schema."""

    name: str
    description: str
    parameters: Dict[str, Any]


class ToolInfoCompact(BaseModel):
    """Tool information - compact (name + description only)."""

    name: str
    description: str


class ToolsListResponse(BaseModel):
    """Tools list response - full."""

    tools: list[ToolInfo]


class ToolsListResponseCompact(BaseModel):
    """Tools list response - compact."""

    tools: list[ToolInfoCompact]


class ToolsListResponseUltraCompact(BaseModel):
    """Tools list response - ultra compact (names only)."""

    tools: list[str]


class ToolsListRequestBody(BaseModel):
    """Request body for tools list with compact mode options."""

    compact: Optional[bool] = True  # Default to compact mode
    ultra_compact: Optional[bool] = False


# MCP JSON-RPC Models for Streamable HTTP
class MCPJsonRpcRequest(BaseModel):
    """MCP JSON-RPC 2.0 request."""

    jsonrpc: str = "2.0"
    id: Optional[Union[str, int]] = None
    method: str
    params: Optional[Dict[str, Any]] = None


class MCPJsonRpcResponse(BaseModel):
    """MCP JSON-RPC 2.0 response."""

    jsonrpc: str = "2.0"
    id: Optional[Union[str, int]] = None
    result: Optional[Any] = None
    error: Optional[Dict[str, Any]] = None


def get_tool_infos_full() -> list[ToolInfo]:
    """Get list of available tools with full schema."""
    return [
        ToolInfo(name=name, description=desc, parameters=params)
        for name, desc, params in TOOL_DEFINITIONS
    ]


def get_tool_infos_compact() -> list[ToolInfoCompact]:
    """Get list of available tools with name + description only (default mode)."""
    return [
        ToolInfoCompact(name=name, description=desc)
        for name, desc, _ in TOOL_DEFINITIONS
    ]


def get_tool_names_only() -> list[str]:
    """Get list of tool names only (ultra compact mode for LLMs)."""
    return [name for name, _, _ in TOOL_DEFINITIONS]


def get_tool_schema(tool_name: str) -> Optional[Dict[str, Any]]:
    """Get full schema for a specific tool."""
    for name, desc, params in TOOL_DEFINITIONS:
        if name == tool_name:
            return {"name": name, "description": desc, "parameters": params}
    return None


def route_tool_call(tools: RuckusVSZTools, tool_name: str, args: Dict[str, Any]) -> str:
    """Route tool call to appropriate handler based on tool name."""
    # Map tool names to method calls
    parts = tool_name.replace("ruckus.", "").split(".")

    # Build method name from parts
    method_name = "_".join(parts)

    # Get the method from tools object
    if hasattr(tools, method_name):
        method = getattr(tools, method_name)
        try:
            return method(**args)
        except TypeError as e:
            return f"Invalid arguments for {tool_name}: {e}"

    return f"Unknown tool: {tool_name}"


def create_app() -> FastAPI:
    """Create FastAPI application with OpenWebUI optimization and security."""
    setup_logging()
    
    # Load application configuration
    app_config = get_app_config()

    app = FastAPI(
        title="Ruckus vSZ MCP Server",
        version=SERVER_VERSION,
        description="Model Context Protocol server for Ruckus Virtual SmartZone - Optimized for OpenWebUI",
    )
    
    # Add security middleware if API key is configured
    if app_config.security.api_key:
        app.add_middleware(SecurityMiddleware, security_config=app_config.security)
        logger.info("Security middleware enabled with Bearer token authentication")
    else:
        logger.warning("No API key configured - endpoints are unprotected!")
    
    # Initialize controller manager
    controller_manager = ControllerManager(app_config)
    logger.info(f"Initialized {controller_manager.controller_count} controller(s)")

    # Store active sessions for MCP Streamable HTTP
    mcp_sessions: Dict[str, Dict[str, Any]] = {}

    def get_ruckus_client(controller_id: Optional[str] = None) -> RuckusVSZClient:
        """Get Ruckus vSZ client instance for specified controller."""
        return controller_manager.get_client(controller_id)

    @app.get("/healthz", operation_id="ruckus_healthz")
    async def healthz():
        """Health check endpoint (public - no auth required)."""
        return {
            "status": "ok",
            "version": SERVER_VERSION,
            "controllers": controller_manager.controller_count
        }
    
    @app.get("/health", operation_id="ruckus_health")
    async def health():
        """Health check endpoint alias (public - no auth required)."""
        return await healthz()

    @app.get("/mcp/metadata", operation_id="ruckus_mcp_metadata")
    async def mcp_metadata():
        """MCP platform metadata endpoint for capability discovery."""
        return MCPMetadata().model_dump()
    
    # ==========================================
    # Multi-Controller Endpoints
    # ==========================================
    
    @app.get("/v1/controllers", operation_id="ruckus_list_controllers")
    async def list_controllers():
        """List all configured vSZ controllers.
        
        Returns information about each controller including ID, name, URL,
        and connection status. Use controller IDs in tool calls to target
        specific controllers.
        """
        return {
            "controllers": controller_manager.list_controllers(),
            "default_controller": app_config.default_controller_id,
            "total": controller_manager.controller_count
        }
    
    @app.get("/v1/controllers/{controller_id}", operation_id="ruckus_get_controller")
    async def get_controller(controller_id: str):
        """Get information about a specific controller."""
        try:
            return controller_manager.get_controller_info(controller_id)
        except ValueError as e:
            return JSONResponse(
                status_code=404,
                content={"error": str(e)}
            )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception):
        """Handle unhandled exceptions."""
        logger.exception("unhandled_exception", extra={"path": str(request.url.path)})
        return JSONResponse(
            status_code=500,
            content=ToolCallResponse(
                status="error",
                error={"code": "internal_error", "message": "Internal server error"},
            ).model_dump(),
        )

    @app.post("/v1/tools/list", operation_id="ruckus_tools_list")
    async def tools_list(
        request: Request,
        compact: Optional[bool] = Query(default=None, description="Return compact format (name+description)"),
        ultra_compact: Optional[bool] = Query(default=None, description="Return ultra compact format (names only)"),
    ):
        """List available tools with compact mode support for LLM token optimization.
        
        Response modes (for LLM token efficiency):
        - ultra_compact=true: Returns tool names only (~100 tokens)
        - compact=true (default): Returns name + description (~500 tokens)  
        - compact=false: Returns full schemas (~2000 tokens)
        
        Modes can be set via query params or JSON body.
        """
        # Parse body if present for mode flags
        body_compact = None
        body_ultra_compact = None
        try:
            body = await request.json()
            body_compact = body.get("compact")
            body_ultra_compact = body.get("ultra_compact")
        except Exception:
            pass  # No JSON body or invalid JSON

        # Query params take precedence over body
        use_ultra_compact = ultra_compact if ultra_compact is not None else body_ultra_compact
        use_compact = compact if compact is not None else body_compact

        # Determine response mode
        if use_ultra_compact:
            # Ultra compact: names only
            tool_names = get_tool_names_only()
            logger.info(f"Listing {len(tool_names)} tools (ultra_compact mode)")
            return {"tools": tool_names}
        elif use_compact is False:
            # Full mode: complete schemas
            tool_infos = get_tool_infos_full()
            logger.info(f"Listing {len(tool_infos)} tools (full mode)")
            return ToolsListResponse(tools=tool_infos).model_dump()
        else:
            # Default: compact mode (name + description)
            tool_infos = get_tool_infos_compact()
            logger.info(f"Listing {len(tool_infos)} tools (compact mode)")
            return {"tools": [t.model_dump() for t in tool_infos]}

    @app.get("/v1/tools/{tool_name}/schema", operation_id="ruckus_get_tool_schema")
    async def get_tool_schema_endpoint(tool_name: str):
        """Get full schema for a specific tool.
        
        Use this endpoint to get complete parameter schema when needed,
        rather than fetching all schemas at once.
        """
        schema = get_tool_schema(tool_name)
        if schema:
            return schema
        return JSONResponse(
            status_code=404,
            content={"error": f"Tool '{tool_name}' not found"}
        )

    @app.post("/v1/tools/call", operation_id="ruckus_tools_call")
    async def tools_call(req: ToolCallRequest):
        """Execute tool call.
        
        Args:
            req: Tool call request with optional controller_id for multi-vSZ mode
        """
        try:
            # Get client for specified controller (or default)
            client = get_ruckus_client(req.controller_id)
            tools = RuckusVSZTools(client)
            result = route_tool_call(tools, req.tool, req.args)

            return ToolCallResponse(
                status="ok", 
                data={"result": result}, 
                meta={
                    "tool": req.tool,
                    "controller": req.controller_id or app_config.default_controller_id
                }
            ).model_dump()

        except KeyError as e:
            logger.error(f"Unknown tool: {req.tool}", exc_info=e)
            return ToolCallResponse(
                status="error",
                error={"code": "unknown_tool", "message": str(e)},
                meta={"tool": req.tool},
            ).model_dump()
        except ValueError as e:
            logger.error(f"Invalid request for {req.tool}", exc_info=e)
            return ToolCallResponse(
                status="error",
                error={"code": "invalid_request", "message": str(e)},
                meta={"tool": req.tool},
            ).model_dump()
        except RuckusVSZAPIError as e:
            logger.error(f"API error for {req.tool}", exc_info=e)
            return ToolCallResponse(
                status="error",
                error={"code": "api_error", "message": str(e)},
                meta={"tool": req.tool},
            ).model_dump()
        except Exception as e:
            logger.exception(f"Tool call failed: {req.tool}")
            return ToolCallResponse(
                status="error",
                error={"code": "internal_error", "message": f"Internal error: {str(e)}"},
                meta={"tool": req.tool},
            ).model_dump()

    # ==========================================
    # MCP Streamable HTTP Endpoints (OpenWebUI)
    # ==========================================

    async def handle_mcp_request(
        rpc_request: MCPJsonRpcRequest,
        client: Optional[RuckusVSZClient] = None
    ) -> MCPJsonRpcResponse:
        """Handle MCP JSON-RPC request."""
        method = rpc_request.method
        params = rpc_request.params or {}
        
        try:
            if method == "initialize":
                return MCPJsonRpcResponse(
                    id=rpc_request.id,
                    result={
                        "protocolVersion": "2024-11-05",
                        "capabilities": {
                            "tools": {"listChanged": False}
                        },
                        "serverInfo": {
                            "name": "ruckus-vsz-mcp-server",
                            "version": SERVER_VERSION
                        }
                    }
                )
            
            elif method == "notifications/initialized":
                # Client acknowledgment, no response needed for notifications
                return MCPJsonRpcResponse(id=rpc_request.id, result={})
            
            elif method == "tools/list":
                # Return compact tool list for LLM efficiency
                tools = []
                for name, desc, schema in TOOL_DEFINITIONS:
                    tools.append({
                        "name": name,
                        "description": desc,
                        "inputSchema": schema
                    })
                return MCPJsonRpcResponse(
                    id=rpc_request.id,
                    result={"tools": tools}
                )
            
            elif method == "tools/call":
                tool_name = params.get("name", "")
                arguments = params.get("arguments", {})
                controller_id = params.get("controller_id")  # Optional: target specific controller
                
                # Get client for specified controller (or default)
                client = get_ruckus_client(controller_id)
                
                tools = RuckusVSZTools(client)
                result = route_tool_call(tools, tool_name, arguments)
                
                return MCPJsonRpcResponse(
                    id=rpc_request.id,
                    result={
                        "content": [
                            {"type": "text", "text": result}
                        ]
                    }
                )
            
            elif method == "ping":
                return MCPJsonRpcResponse(id=rpc_request.id, result={})
            
            else:
                return MCPJsonRpcResponse(
                    id=rpc_request.id,
                    error={"code": -32601, "message": f"Method not found: {method}"}
                )
                
        except Exception as e:
            logger.exception(f"MCP request failed: {method}")
            return MCPJsonRpcResponse(
                id=rpc_request.id,
                error={"code": -32603, "message": str(e)}
            )

    @app.post("/mcp", operation_id="ruckus_mcp_streamable")
    async def mcp_streamable_http(request: Request):
        """MCP Streamable HTTP endpoint for OpenWebUI.
        
        This endpoint implements the MCP Streamable HTTP transport required
        by OpenWebUI v0.6.31+. It accepts JSON-RPC 2.0 requests and returns
        responses in the same format.
        
        Supports:
        - initialize: Capability negotiation
        - tools/list: List available tools (compact format)
        - tools/call: Execute a tool
        - ping: Health check
        """
        try:
            body = await request.json()
            
            # Handle batch requests
            if isinstance(body, list):
                responses = []
                for item in body:
                    rpc_req = MCPJsonRpcRequest(**item)
                    response = await handle_mcp_request(rpc_req)
                    if response.id is not None:  # Don't include notification responses
                        responses.append(response.model_dump(exclude_none=True))
                return JSONResponse(content=responses)
            
            # Single request
            rpc_request = MCPJsonRpcRequest(**body)
            response = await handle_mcp_request(rpc_request)
            
            return JSONResponse(content=response.model_dump(exclude_none=True))
            
        except Exception as e:
            logger.exception("MCP request parsing failed")
            return JSONResponse(
                content={
                    "jsonrpc": "2.0",
                    "id": None,
                    "error": {"code": -32700, "message": f"Parse error: {str(e)}"}
                }
            )

    @app.get("/mcp/info", operation_id="ruckus_mcp_info")
    async def mcp_info():
        """MCP server information endpoint (public - no auth required).
        
        Returns server capabilities and version info for OpenWebUI discovery.
        """
        return {
            "name": "ruckus-vsz-mcp-server",
            "version": SERVER_VERSION,
            "protocol_version": "2024-11-05",
            "description": "Ruckus vSZ wireless controller management via MCP",
            "capabilities": {
                "tools": True,
                "resources": False,
                "prompts": False,
                "multi_controller": True
            },
            "tool_count": len(TOOL_DEFINITIONS),
            "controller_count": controller_manager.controller_count,
            "controllers": controller_manager.controller_ids,
            "default_controller": app_config.default_controller_id,
            "security": {
                "bearer_auth": bool(app_config.security.api_key),
                "ip_whitelist": bool(app_config.security.allowed_ips),
                "rate_limit": app_config.security.rate_limit_per_minute
            },
            "modules": [
                "system", "zones", "wlans", "access_points",
                "clients", "monitoring", "alarms", "authentication", "network"
            ]
        }

    return app


def main():
    """Main entry point for uvicorn."""
    import uvicorn

    port = int(os.getenv("SERVER_PORT", "8082"))
    host = os.getenv("SERVER_HOST", "0.0.0.0")
    uvicorn.run(create_app(), host=host, port=port)


if __name__ == "__main__":
    main()
