"""
Day 0: Site Provisioning.

Orchestrates the creation and initialization of new physical sites via the Mist API.
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from src.services.mist_engine import MistEngine
from src.services.redis import get_redis_client


router = APIRouter(prefix="/sites", tags=["day 0 - site provisioning"])


# =============================================================================
# Models
# =============================================================================

class SiteCreateRequest(BaseModel):
    """Request payload for creating a new Mist site."""
    name: str = Field(..., description="Site display name", examples=["Branch-Austin-001"])
    address: str | None = Field(None, description="Physical street address", examples=["123 Main St, Austin, TX"])
    timezone: str = Field(default="America/Chicago", description="IANA timezone", examples=["America/Chicago"])
    country_code: str = Field(default="US", description="ISO 3166-1 alpha-2 country code", examples=["US"])
    notes: str | None = Field(None, description="Optional notes for the site")


class SiteResponse(BaseModel):
    """Response after site creation."""
    id: str
    name: str
    address: str | None
    timezone: str
    country_code: str
    status: str


# =============================================================================
# Endpoints
# =============================================================================

@router.post("/", response_model=SiteResponse, summary="Create a new site in Mist.")
async def create_site(request: SiteCreateRequest):
    """
    Creates a new site container in the Mist organization.

    Retrieves `api_host` and `org_id` from Redis (set by /org/self).
    Sends POST to Mist API /api/v1/orgs/{org_id}/sites.
    """
    redis_client = get_redis_client()

    # Get stored API context from Redis
    api_host = redis_client.get("api_host")
    org_id = redis_client.get("org_id")

    if not api_host or not org_id:
        raise HTTPException(
            status_code=400,
            detail="Missing api_host or org_id. Call POST /org/self first."
        )

    engine = MistEngine(host=api_host)
    payload = {
        "name": request.name,
        "address": request.address,
        "timezone": request.timezone,
        "country_code": request.country_code,
        "notes": request.notes,
    }

    result = await engine.post(f"/api/v1/orgs/{org_id}/sites", json=payload)

    return SiteResponse(
        id=result.get("id", ""),
        name=result.get("name", request.name),
        address=result.get("address"),
        timezone=result.get("timezone", request.timezone),
        country_code=result.get("country_code", request.country_code),
        status="created"
    )


@router.get("/", summary="List all sites in the organization.")
async def list_sites():
    """Retrieves all sites from the Mist organization."""
    redis_client = get_redis_client()

    api_host = redis_client.get("api_host")
    org_id = redis_client.get("org_id")

    if not api_host or not org_id:
        raise HTTPException(
            status_code=400,
            detail="Missing api_host or org_id. Call POST /org/self first."
        )

    engine = MistEngine(host=api_host)
    sites = await engine.get(f"/api/v1/orgs/{org_id}/sites")

    return {"sites": sites, "count": len(sites)}
