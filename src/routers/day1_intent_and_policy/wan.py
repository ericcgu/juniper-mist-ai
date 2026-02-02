"""
WAN Router - Day 1: SD-WAN & AppQoE
Handles applications, hub profiles, and gateway templates.
"""
from fastapi import APIRouter, Security
from fastapi.security import APIKeyHeader

from src.routers.day1_intent_and_policy.models import ApplicationCreate, HubProfileCreate, GatewayTemplateCreate

router = APIRouter(prefix="/wan", tags=["WAN - Day 1"])

mist_api_key = APIKeyHeader(name="X-Mist-API-Key", description="Your Juniper Mist API token")


@router.post("/applications", summary="Step 3: Create Applications")
async def create_applications(
    request: ApplicationCreate,
    api_key: str = Security(mist_api_key)
):
    """
    **Step 3: Create Applications (Day 1 - WAN)**
    
    Defines application signatures for traffic classification and
    AppQoE steering. These are referenced by Gateway Templates.
    """
    # TODO: Call Mist API to create application
    return {
        "id": f"app-{request.name.lower().replace(' ', '-')}",
        "name": request.name,
        "app_type": request.app_type,
        "traffic_class": request.traffic_class,
        "status": "created"
    }


@router.post("/hub-profiles", summary="Step 5: Deploy Hub Profiles")
async def create_hub_profiles(
    request: HubProfileCreate,
    api_key: str = Security(mist_api_key)
):
    """
    **Step 5: Deploy Hub Profiles (Day 1 - WAN)**
    
    Creates hub profiles that define the SD-WAN overlay topology.
    Hub sites act as aggregation points for spoke-to-spoke traffic.
    """
    # TODO: Call Mist API to create hub profile
    return {
        "id": f"hub-profile-{request.name.lower().replace(' ', '-')}",
        "name": request.name,
        "hub_count": len(request.hub_site_ids),
        "status": "created"
    }


@router.post("/gateway-templates", summary="Step 6: Deploy WAN Edge Templates")
async def create_gateway_template(
    request: GatewayTemplateCreate,
    api_key: str = Security(mist_api_key)
):
    """
    **Step 6: Deploy WAN Edge Templates (Day 1 - WAN)**
    
    Creates gateway configuration templates for SSR/SRX devices.
    References Applications (Step 3) and Networks (Step 4).
    Uses "Late Binding" to attach to sites after creation.
    """
    # TODO: Call Mist API to create gateway template
    return {
        "id": f"gw-tmpl-{request.name.lower().replace(' ', '-')}",
        "name": request.name,
        "tunnel_provider": request.tunnel_provider,
        "status": "created"
    }


@router.get("/applications", summary="List applications")
async def list_applications(
    api_key: str = Security(mist_api_key)
):
    """List all defined applications."""
    return {"applications": [], "count": 0}


@router.get("/gateway-templates", summary="List gateway templates")
async def list_gateway_templates(
    api_key: str = Security(mist_api_key)
):
    """List all gateway templates."""
    return {"templates": [], "count": 0}


@router.post("/traffic-steering", summary="Create traffic steering policy")
async def create_traffic_steering(
    name: str,
    application_ids: list[str],
    action: str = "allow",
    api_key: str = Security(mist_api_key)
):
    """Create a traffic steering policy for application-aware routing."""
    return {
        "id": f"steering-{name}",
        "name": name,
        "applications": application_ids,
        "action": action,
        "status": "created"
    }
