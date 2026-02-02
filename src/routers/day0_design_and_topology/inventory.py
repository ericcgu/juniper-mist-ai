"""
Inventory Router - Day 0: Supply Chain Logistics
Handles device assignment and claim operations.
"""
from fastapi import APIRouter, Security
from fastapi.security import APIKeyHeader
from pydantic import BaseModel, Field

router = APIRouter(prefix="/inventory", tags=["Inventory - Day 0"])

mist_api_key = APIKeyHeader(name="X-Mist-API-Key", description="Your Juniper Mist API token")

# =============================================================================
# Inventory Models
# =============================================================================

class DeviceAssignment(BaseModel):
    """Device assignment request."""
    serial_numbers: list[str] = Field(..., description="List of device serial numbers")
    site_id: str = Field(..., description="Target site ID")
    managed: bool = Field(default=True, description="Enable Mist management")


class ClaimDevice(BaseModel):
    """Claim device request."""
    claim_codes: list[str] = Field(..., description="Device claim codes")
    org_id: str = Field(..., description="Organization ID")


class DeviceResponse(BaseModel):
    """Device information response."""
    serial: str
    site_id: str | None = None
    model: str | None = None
    status: str



@router.post("/assign", summary="Step 2: Assign Devices to Sites")
async def assign_devices(
    request: DeviceAssignment,
    api_key: str = Security(mist_api_key)
):
    """
    **Step 2: Assign Devices to Sites (Day 0)**
    
    Assigns claimed devices to a specific site. Requires the Site ID
    from Step 1. Devices will adopt site-specific configurations
    once assigned.
    """
    # TODO: Call Mist API to assign devices
    # for serial in request.serial_numbers:
    #     mistapi.assign_device_to_site(serial, request.site_id)
    
    return {
        "site_id": request.site_id,
        "devices_assigned": len(request.serial_numbers),
        "serial_numbers": request.serial_numbers,
        "status": "assigned"
    }


@router.post("/claim", summary="Claim devices to organization")
async def claim_devices(
    request: ClaimDevice,
    api_key: str = Security(mist_api_key)
):
    """
    Claim devices to the organization using claim codes.
    Devices must be claimed before they can be assigned to sites.
    """
    # TODO: Call Mist API to claim devices
    return {
        "org_id": request.org_id,
        "claimed_count": len(request.claim_codes),
        "status": "claimed"
    }


@router.get("/devices", summary="List inventory devices")
async def list_inventory(
    api_key: str = Security(mist_api_key),
    unassigned: bool = False
):
    """
    List all devices in the organization inventory.
    Filter by unassigned to find devices ready for site assignment.
    """
    # TODO: Call Mist API
    return {"devices": [], "count": 0}


@router.get("/devices/{serial}", summary="Get device details")
async def get_device(
    serial: str,
    api_key: str = Security(mist_api_key)
):
    """Get detailed information about a specific device."""
    # TODO: Call Mist API
    return {"serial": serial, "status": "unknown"}
