"""Ruckus vSZ MCP Server - Main server implementation with comprehensive API coverage."""

from __future__ import annotations

import logging
import os
from typing import Any, Dict, Optional

from fastapi import Depends, FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from .api_client import RuckusVSZAPIError, RuckusVSZClient
from .config import get_ruckus_vsz_config
from .tool_definitions import TOOL_DEFINITIONS
from .tools import RuckusVSZTools

logger = logging.getLogger("ruckus_vsz_mcp_server")


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
    server_version: str = "1.0.0"
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


class ToolCallResponse(BaseModel):
    """Tool call response."""

    status: str
    data: Optional[Any] = None
    error: Optional[Dict[str, str]] = None
    meta: Optional[Dict[str, str]] = None


class ToolInfo(BaseModel):
    """Tool information."""

    name: str
    description: str
    parameters: Dict[str, Any]


class ToolsListResponse(BaseModel):
    """Tools list response."""

    tools: list[ToolInfo]


def get_tool_infos() -> list[ToolInfo]:
    """Get list of available tools from definitions."""
    return [
        ToolInfo(name=name, description=desc, parameters=params)
        for name, desc, params in TOOL_DEFINITIONS
    ]


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
    """Create FastAPI application."""
    setup_logging()

    app = FastAPI(
        title="Ruckus vSZ MCP Server",
        version="1.0.0",
        description="Model Context Protocol server for Ruckus Virtual SmartZone - Complete API coverage",
    )

    def get_ruckus_client() -> RuckusVSZClient:
        """Get Ruckus vSZ client instance."""
        config = get_ruckus_vsz_config()
        return RuckusVSZClient(config)

    @app.get("/healthz")
    async def healthz():
        """Health check endpoint."""
        return {"status": "ok", "version": "1.0.0"}

    @app.get("/mcp/metadata")
    async def mcp_metadata():
        """MCP platform metadata endpoint for capability discovery."""
        return MCPMetadata().model_dump()

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

    @app.post("/v1/tools/list")
    async def tools_list():
        """List available tools."""
        tool_infos = get_tool_infos()
        logger.info(f"Listing {len(tool_infos)} available tools")
        return ToolsListResponse(tools=tool_infos).model_dump()

    @app.post("/v1/tools/call")
    async def tools_call(
        req: ToolCallRequest, client: RuckusVSZClient = Depends(get_ruckus_client)
    ):
        """Execute tool call."""
        try:
            tools = RuckusVSZTools(client)
            result = route_tool_call(tools, req.tool, req.args)

            return ToolCallResponse(
                status="ok", data={"result": result}, meta={"tool": req.tool}
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

    return app


def main():
    """Main entry point for uvicorn."""
    import uvicorn
    import os

    port = int(os.getenv("SERVER_PORT", "8082"))
    uvicorn.run(create_app(), host="0.0.0.0", port=port)


if __name__ == "__main__":
    main()
