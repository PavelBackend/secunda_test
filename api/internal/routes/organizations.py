from fastapi import APIRouter, Depends, Security
from sqlalchemy.ext.asyncio import AsyncSession

from ...database import get_async_session
from ...depends import get_organizations_service
from ...security import require_api_key
from ..models.organizations import OrganizationOut
from ..services.organizations import OrganizationsService

router = APIRouter(
    tags=["organizations"],
    dependencies=[Security(require_api_key)],
)


@router.get("/buildings/{building_id}/organizations", response_model=list[OrganizationOut])
async def get_organizations_by_building(
    building_id: int,
    session: AsyncSession = Depends(get_async_session),
    service: OrganizationsService = Depends(get_organizations_service),
):
    return await service.get_by_building(session, building_id)


@router.get("/activities/{activity_id}/organizations", response_model=list[OrganizationOut])
async def get_organizations_by_activity(
    activity_id: int,
    session: AsyncSession = Depends(get_async_session),
    service: OrganizationsService = Depends(get_organizations_service),
):
    return await service.get_by_activity(session, activity_id)


@router.get("/activities/{activity_id}/organizations/tree", response_model=list[OrganizationOut])
async def get_organizations_by_activity_tree(
    activity_id: int,
    session: AsyncSession = Depends(get_async_session),
    service: OrganizationsService = Depends(get_organizations_service),
):
    return await service.get_by_activity(session, activity_id, include_descendants=True)


@router.get("/organizations/by_radius", response_model=list[OrganizationOut])
async def get_organizations_by_radius(
    lat: float,
    lon: float,
    radius: float,
    session: AsyncSession = Depends(get_async_session),
    service: OrganizationsService = Depends(get_organizations_service),
):
    return await service.get_by_radius(session, lat=lat, lon=lon, radius=radius)


@router.get("/organizations/by_rectangle", response_model=list[OrganizationOut])
async def get_organizations_by_rectangle(
    lat_min: float,
    lat_max: float,
    lon_min: float,
    lon_max: float,
    session: AsyncSession = Depends(get_async_session),
    service: OrganizationsService = Depends(get_organizations_service),
):
    return await service.get_by_rectangle(
        session,
        lat_min=lat_min,
        lat_max=lat_max,
        lon_min=lon_min,
        lon_max=lon_max,
    )


@router.get("/organizations", response_model=list[OrganizationOut])
async def search_organizations_by_name(
    name: str,
    session: AsyncSession = Depends(get_async_session),
    service: OrganizationsService = Depends(get_organizations_service),
):
    return await service.get_by_name(session, name)


@router.get("/organizations/{org_id}", response_model=OrganizationOut)
async def get_organization_by_id(
    org_id: int,
    session: AsyncSession = Depends(get_async_session),
    service: OrganizationsService = Depends(get_organizations_service),
):
    return await service.get_by_id(session, org_id)
