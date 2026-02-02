"""
Wireless Router - Day 1: RF, WLANs, & Security
Handles RF templates, WLAN templates, policies, and PSKs.

These are 'Day 1' policy objects that define the wireless standard 
for the organization.
"""
from fastapi import APIRouter, Security
from fastapi.security import APIKeyHeader

from .models import (
    RFTemplateCreate,
    WLANTemplateCreate,
    WLANCreate,
    LabelCreate,
    WxRuleCreate,
    OrgPSKCreate,
)

router = APIRouter(prefix="/wireless", tags=["Wireless - Day 1"])

mist_api_key = APIKeyHeader(name="X-Mist-API-Key", description="Your Juniper Mist API token")


# ============================================================================
# Endpoints
# ============================================================================

@router.post("/rf-templates", summary="Step 9: Create RF Templates")
async def create_rf_template(
    request: RFTemplateCreate,
    api_key: str = Security(mist_api_key)
):
    """
    **Step 9: Create RF Templates (Day 1 - Wireless)**
    
    Defines radio frequency parameters including power levels, channel
    width, and band steering. Applied to sites via Late Binding.
    """
    return {
        "id": f"rf-tmpl-{request.name.lower().replace(' ', '-')}",
        "name": request.name,
        "country_code": request.country_code,
        "bands_enabled": {
            "2.4GHz": request.band_24.get("enabled", True),
            "5GHz": request.band_5.get("enabled", True),
            "6GHz": request.band_6.get("enabled", False)
        },
        "status": "created"
    }


@router.post("/wlan-templates", summary="Step 8: Deploy WLAN Templates")
async def create_wlan_template(
    request: WLANTemplateCreate,
    api_key: str = Security(mist_api_key)
):
    """
    **Step 8: Deploy WLAN Templates (Day 1 - Wireless)**
    
    Creates the WLAN template container that holds SSID configurations.
    WLANs are added to this template in Step 10.
    """
    return {
        "id": f"wlan-tmpl-{request.name.lower().replace(' ', '-')}",
        "name": request.name,
        "applies_to": request.applies_to,
        "status": "created"
    }


@router.post("/wlans", summary="Step 10: Create WLANs")
async def create_wlans(
    request: WLANCreate,
    api_key: str = Security(mist_api_key)
):
    """
    **Step 10: Create WLANs (Day 1 - Wireless)**
    
    Creates individual SSID configurations within a WLAN template.
    Linked to the template from Step 8.
    """
    return {
        "id": f"wlan-{request.ssid.lower().replace(' ', '-')}",
        "ssid": request.ssid,
        "auth_type": request.auth_type,
        "vlan_id": request.vlan_id,
        "template_id": request.template_id,
        "status": "created"
    }


@router.post("/labels", summary="Step 11: Create Labels")
async def create_labels(
    request: LabelCreate,
    api_key: str = Security(mist_api_key)
):
    """
    **Step 11: Create Labels (Day 1 - Wireless/Policy)**
    
    Creates labels used for policy matching in wxrules.
    Labels can match WLANs, client types, or AP groups.
    """
    return {
        "id": f"label-{request.name.lower().replace(' ', '-')}",
        "name": request.name,
        "label_type": request.label_type,
        "values": request.values,
        "status": "created"
    }


@router.post("/wxrules", summary="Step 12: Deploy WLAN Policies (wxrules)")
async def create_wx_rules(
    request: WxRuleCreate,
    api_key: str = Security(mist_api_key)
):
    """
    **Step 12: Deploy WLAN Policies (Day 1 - Wireless)**
    
    Creates wireless security rules that control traffic between
    labeled groups. Uses Labels from Step 11.
    """
    return {
        "id": f"wxrule-{request.name.lower().replace(' ', '-')}",
        "name": request.name,
        "order": request.order,
        "action": request.action,
        "src_labels": request.src_labels,
        "dst_labels": request.dst_labels,
        "status": "created"
    }


@router.post("/org-psks", summary="Step 13: Create Org PSKs")
async def create_org_psks(
    request: OrgPSKCreate,
    api_key: str = Security(mist_api_key)
):
    """
    **Step 13: Create Org PSKs (Day 1 - Wireless)**
    
    Creates organization-level PSKs for secure, scalable wireless access.
    Supports per-user/per-device VLANs and expiration policies.
    """
    return {
        "id": f"psk-{request.name.lower().replace(' ', '-')}",
        "name": request.name,
        "ssid": request.ssid,
        "vlan_id": request.vlan_id,
        "usage": request.usage,
        "has_expiry": request.expiry is not None,
        "status": "created"
    }


# ============================================================================
# List Endpoints
# ============================================================================

@router.get("/rf-templates", summary="List RF templates")
async def list_rf_templates(api_key: str = Security(mist_api_key)):
    """List all RF templates."""
    return {"templates": [], "count": 0}


@router.get("/wlan-templates", summary="List WLAN templates")
async def list_wlan_templates(api_key: str = Security(mist_api_key)):
    """List all WLAN templates."""
    return {"templates": [], "count": 0}


@router.get("/wlans", summary="List WLANs")
async def list_wlans(api_key: str = Security(mist_api_key)):
    """List all WLANs."""
    return {"wlans": [], "count": 0}


@router.get("/labels", summary="List labels")
async def list_labels(api_key: str = Security(mist_api_key)):
    """List all labels."""
    return {"labels": [], "count": 0}


@router.get("/org-psks", summary="List Org PSKs")
async def list_org_psks(api_key: str = Security(mist_api_key)):
    """List all organization PSKs."""
    return {"psks": [], "count": 0}
