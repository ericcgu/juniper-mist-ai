"""
WAN Models - Routing & SD-WAN
Application signatures, hub profiles, and gateway templates.
"""
from pydantic import BaseModel, Field


class ApplicationCreate(BaseModel):
    """Application definition for traffic steering."""
    name: str = Field(..., description="Application name")
    app_type: str = Field(default="custom", description="Application type")
    hostnames: list[str] = Field(default_factory=list, description="Hostname patterns")
    ips: list[str] = Field(default_factory=list, description="IP addresses/ranges")
    dscp: int | None = Field(None, ge=0, le=63, description="DSCP marking")
    traffic_class: str = Field(default="best-effort", description="Traffic class")


class HubProfileCreate(BaseModel):
    """Hub profile for SD-WAN topology."""
    name: str = Field(..., description="Hub profile name")
    hub_site_ids: list[str] = Field(..., description="Hub site IDs")
    tunnel_configs: dict = Field(default_factory=dict, description="Tunnel configurations")


class GatewayTemplateCreate(BaseModel):
    """Gateway template for WAN edge devices."""
    name: str = Field(..., description="Template name")
    port_config: dict = Field(default_factory=dict, description="WAN/LAN port configuration")
    tunnel_provider: str = Field(default="mist", description="Tunnel provider")
    routing_policies: list[dict] = Field(default_factory=list, description="Routing policies")
    idp_profiles: dict | None = Field(None, description="IDP/Security profiles")
