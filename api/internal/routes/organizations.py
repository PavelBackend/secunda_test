from fastapi import APIRouter, Depends, Security
from sqlalchemy.ext.asyncio import AsyncSession

from ...database import get_async_session
from ...depends import get_organizations_service
from ...security import require_api_key
from ..services.organizations import OrganizationsService

router = APIRouter(
    prefix="/organizations",
    tags=["organizations"],
    dependencies=[Security(require_api_key)],
)


@router.get("/buildings/{building_id}/organizations")
async def get_organizations_by_building(
    building_id: int,
    organizations_service: OrganizationsService = Depends(get_organizations_service),
    session: AsyncSession = Depends(get_async_session),
):
    filters = {"building_id": building_id}
    return await organizations_service.get_all_organizations_by_filters(
        filters=filters, session=session
    )


@router.get("/activities/{activity_id}/organizations")
async def get_organizations_by_activity_exact(
    activity_id: int,
    organizations_service: OrganizationsService = Depends(get_organizations_service),
    session: AsyncSession = Depends(get_async_session),
):
    filters = {"activity_id": activity_id, "activity_scope": "exact"}
    return await organizations_service.get_all_organizations_by_filters(
        filters=filters, session=session
    )


@router.get("/activities/{activity_id}/organizations/tree")
async def get_organizations_by_activity_tree(
    activity_id: int,
    organizations_service: OrganizationsService = Depends(get_organizations_service),
    session: AsyncSession = Depends(get_async_session),
):
    filters = {"activity_id": activity_id, "activity_scope": "tree"}
    return await organizations_service.get_all_organizations_by_filters(
        filters=filters, session=session
    )


@router.get("/by_radius")
async def get_organizations_by_radius(
    lat: float,
    lon: float,
    radius: float,
    organizations_service: OrganizationsService = Depends(get_organizations_service),
    session: AsyncSession = Depends(get_async_session),
):
    filters = {"lat": lat, "lon": lon, "radius": radius}
    return await organizations_service.get_all_organizations_by_filters(
        filters=filters, session=session
    )


@router.get("/id/{org_id}")
async def get_organization_by_id(
    org_id: int,
    organizations_service: OrganizationsService = Depends(get_organizations_service),
    session: AsyncSession = Depends(get_async_session),
):
    filters = {"org_id": org_id}
    return await organizations_service.get_all_organizations_by_filters(
        filters=filters, session=session
    )


@router.get("/by_name")
async def get_organization_by_name(
    name: str,
    organizations_service: OrganizationsService = Depends(get_organizations_service),
    session: AsyncSession = Depends(get_async_session),
):
    filters = {"name": name}
    return await organizations_service.get_all_organizations_by_filters(
        filters=filters, session=session
    )
