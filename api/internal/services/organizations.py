from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..orm_models.dao import Organization
from ..repository.organizations import OrganizationsRepo


class OrganizationsService:
    def __init__(self):
        self.repo = OrganizationsRepo()

    async def get_by_id(self, session: AsyncSession, org_id: int) -> Organization:
        org = await self.repo.get_by_id(session, org_id)
        if org is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Organization with id={org_id} not found",
            )
        return org

    async def get_by_name(self, session: AsyncSession, name: str) -> list[Organization]:
        return await self.repo.get_by_name(session, name)

    async def get_by_building(self, session: AsyncSession, building_id: int) -> list[Organization]:
        return await self.repo.get_by_building(session, building_id)

    async def get_by_activity(
        self, session: AsyncSession, activity_id: int, *, include_descendants: bool = False
    ) -> list[Organization]:
        return await self.repo.get_by_activity(session, activity_id, include_descendants=include_descendants)

    async def get_by_radius(
        self, session: AsyncSession, *, lat: float, lon: float, radius: float
    ) -> list[Organization]:
        return await self.repo.get_by_radius(session, lat=lat, lon=lon, radius=radius)

    async def get_by_rectangle(
        self,
        session: AsyncSession,
        *,
        lat_min: float,
        lat_max: float,
        lon_min: float,
        lon_max: float,
    ) -> list[Organization]:
        return await self.repo.get_by_rectangle(
            session,
            lat_min=lat_min,
            lat_max=lat_max,
            lon_min=lon_min,
            lon_max=lon_max,
        )
