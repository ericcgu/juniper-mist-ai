"""
Day 1 Models - Policy Deployment
WAN, Wired, and Wireless request/response models.
"""
from pydantic import BaseModel, Field


# =============================================================================
# WAN Models (Steps 3, 5, 6)
# =============================================================================

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


# =============================================================================
# Wired Models (Steps 4, 7)
# =============================================================================

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


# =============================================================================
# Wireless Models (Steps 8-13)
# =============================================================================

class RFTemplateCreate(BaseModel):
    """RF Template configuration."""
    name: str = Field(..., description="Template name")
    band_24: dict = Field(default_factory=lambda: {"enabled": True, "power": 8}, description="2.4GHz settings")
    band_5: dict = Field(default_factory=lambda: {"enabled": True, "power": 12}, description="5GHz settings")
    band_6: dict = Field(default_factory=lambda: {"enabled": False}, description="6GHz settings")
    country_code: str = Field(default="US", description="Regulatory domain")


class WLANTemplateCreate(BaseModel):
    """WLAN Template configuration."""
    name: str = Field(..., description="Template name")
    applies_to: str = Field(default="site", description="Template scope: site or org")


class WLANCreate(BaseModel):
    """WLAN/SSID configuration."""
    ssid: str = Field(..., description="SSID name")
    enabled: bool = Field(default=True)
    auth_type: str = Field(default="psk", description="Auth type: open, psk, eap")
    vlan_id: int | None = Field(None, description="VLAN ID for this WLAN")
    hide_ssid: bool = Field(default=False)
    band: str = Field(default="both", description="Band: 2.4, 5, 6, both")
    template_id: str | None = Field(None, description="Parent WLAN template ID")


class LabelCreate(BaseModel):
    """Label for policy matching."""
    name: str = Field(..., description="Label name")
    label_type: str = Field(default="wlan", description="Label type: wlan, client, ap")
    values: list[str] = Field(default_factory=list, description="Match values")


class WxRuleCreate(BaseModel):
    """Wireless security rule (wxrule)."""
    name: str = Field(..., description="Rule name")
    order: int = Field(..., ge=1, description="Rule order/priority")
    action: str = Field(default="allow", description="Action: allow, deny")
    src_labels: list[str] = Field(default_factory=list, description="Source labels")
    dst_labels: list[str] = Field(default_factory=list, description="Destination labels")


class OrgPSKCreate(BaseModel):
    """Organization PSK configuration."""
    name: str = Field(..., description="PSK name/identifier")
    passphrase: str = Field(..., min_length=8, max_length=63, description="PSK passphrase")
    ssid: str = Field(..., description="Target SSID")
    vlan_id: int | None = Field(None, description="VLAN override for this PSK")
    usage: str = Field(default="multi", description="Usage: single, multi")
    expiry: int | None = Field(None, description="Expiry in seconds")
