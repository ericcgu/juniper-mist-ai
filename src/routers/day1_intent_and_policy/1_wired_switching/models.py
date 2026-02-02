"""
Wired Models - Switching & L2
Network/VLAN definitions and switch templates.
"""
from pydantic import BaseModel, Field


class NetworkCreate(BaseModel):
    """Network/VLAN creation request."""
    name: str = Field(..., description="Network name")
    vlan_id: int = Field(..., ge=1, le=4094, description="VLAN ID")
    subnet: str = Field(..., description="Subnet in CIDR notation")
    gateway: str | None = Field(None, description="Gateway IP address")
    isolation: bool = Field(default=False, description="Enable client isolation")
    internet_access: bool = Field(default=True, description="Allow internet access")


class SwitchTemplateCreate(BaseModel):
    """Switch template creation request."""
    name: str = Field(..., description="Template name")
    port_usages: dict = Field(default_factory=dict, description="Port usage definitions")
    networks: list[str] = Field(default_factory=list, description="Network IDs to include")
    radius_config: dict | None = Field(None, description="RADIUS configuration for 802.1X")
