"""
Wired Router - Day 1: L2 Switching Standards
Handles VLANs, networks, and switch template configuration.
"""
from fastapi import APIRouter, Security
from fastapi.security import APIKeyHeader

from .models import NetworkCreate, SwitchTemplateCreate

router = APIRouter(prefix="/wired", tags=["Wired - Day 1"])

mist_api_key = APIKeyHeader(name="X-Mist-API-Key", description="Your Juniper Mist API token")


@router.post("/networks", summary="Step 4: Create LAN Networks")
async def create_lan_networks(
    request: NetworkCreate,
    api_key: str = Security(mist_api_key)
):
    """
    **Step 4: Create LAN Networks (Day 1 - Wired)**
    
    Creates VLANs that are used by both Switch Templates and WAN Edge
    Templates. These networks form the L2 foundation for the site.
    """
    # TODO: Call Mist API to create network
    return {
        "id": f"network-{request.vlan_id}",
        "name": request.name,
        "vlan_id": request.vlan_id,
        "subnet": request.subnet,
        "status": "created"
    }


@router.post("/templates", summary="Step 7: Deploy Switch Templates")
async def create_switch_template(
    request: SwitchTemplateCreate,
    api_key: str = Security(mist_api_key)
):
    """
    **Step 7: Deploy Switch Templates (Day 1 - Wired)**
    
    Creates switch configuration templates that define port profiles,
    VLAN assignments, and 802.1X policies. References networks from Step 4.
    """
    # TODO: Call Mist API to create switch template
    return {
        "id": f"switch-tmpl-{request.name.lower().replace(' ', '-')}",
        "name": request.name,
        "port_usages": request.port_usages,
        "status": "created"
    }


@router.get("/networks", summary="List all networks")
async def list_networks(
    api_key: str = Security(mist_api_key)
):
    """List all LAN networks in the organization."""
    return {"networks": [], "count": 0}


@router.get("/templates", summary="List switch templates")
async def list_switch_templates(
    api_key: str = Security(mist_api_key)
):
    """List all switch templates in the organization."""
    return {"templates": [], "count": 0}


@router.post("/port-profiles", summary="Create port profile")
async def create_port_profile(
    name: str,
    mode: str = "access",
    vlan_id: int | None = None,
    api_key: str = Security(mist_api_key)
):
    """
    Create a reusable port profile for switch templates.
    Modes: access, trunk, dynamic
    """
    return {
        "id": f"port-profile-{name}",
        "name": name,
        "mode": mode,
        "vlan_id": vlan_id,
        "status": "created"
    }
