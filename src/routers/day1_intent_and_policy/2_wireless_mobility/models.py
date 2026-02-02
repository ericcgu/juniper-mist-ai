"""
Wireless Models - Mobility & RF
RF templates, WLANs, labels, policies, and PSKs.
"""
from pydantic import BaseModel, Field


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
