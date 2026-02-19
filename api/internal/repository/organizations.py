from geoalchemy2 import Geography
from sqlalchemy import and_, cast, func, literal, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased, selectinload

from ..orm_models.dao import Activity, Building, Organization


def _base_query():
    return select(Organization).options(
        selectinload(Organization.phones),
        selectinload(Organization.building),
        selectinload(Organization.activities),
    )


class OrganizationsRepo:
    async def get_by_id(self, session: AsyncSession, org_id: int) -> Organization | None:
        stmt = _base_query().where(Organization.id == org_id)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_name(self, session: AsyncSession, name: str) -> list[Organization]:
        stmt = _base_query().where(Organization.name.ilike(f"%{name}%"))
        result = await session.execute(stmt)
        return list(result.scalars().unique().all())

    async def get_by_building(self, session: AsyncSession, building_id: int) -> list[Organization]:
        stmt = _base_query().where(Organization.building_id == building_id)
        result = await session.execute(stmt)
        return list(result.scalars().unique().all())

    async def get_by_activity(
        self, session: AsyncSession, activity_id: int, *, include_descendants: bool = False
    ) -> list[Organization]:
        if not include_descendants:
            stmt = _base_query().join(Organization.activities).where(Activity.id == activity_id)
        else:
            cte = (
                select(Activity.id.label("id"), literal(0).label("lvl"))
                .where(Activity.id == activity_id)
                .cte("activity_tree", recursive=True)
            )
            a2 = aliased(Activity)
            cte = cte.union_all(select(a2.id, cte.c.lvl + 1).where(and_(a2.parent_id == cte.c.id, cte.c.lvl < 2)))
            stmt = _base_query().join(Organization.activities).where(Activity.id.in_(select(cte.c.id)))
        result = await session.execute(stmt)
        return list(result.scalars().unique().all())

    async def get_by_radius(
        self, session: AsyncSession, *, lat: float, lon: float, radius: float
    ) -> list[Organization]:
        point = cast(func.ST_SetSRID(func.ST_MakePoint(lon, lat), 4326), Geography)
        stmt = (
            _base_query()
            .join(Building, Building.id == Organization.building_id)
            .where(func.ST_DWithin(cast(Building.location, Geography), point, radius))
        )
        result = await session.execute(stmt)
        return list(result.scalars().unique().all())

    async def get_by_rectangle(
        self,
        session: AsyncSession,
        *,
        lat_min: float,
        lat_max: float,
        lon_min: float,
        lon_max: float,
    ) -> list[Organization]:
        envelope = func.ST_MakeEnvelope(lon_min, lat_min, lon_max, lat_max, 4326)
        stmt = (
            _base_query()
            .join(Building, Building.id == Organization.building_id)
            .where(func.ST_Intersects(Building.location, envelope))
        )
        result = await session.execute(stmt)
        return list(result.scalars().unique().all())
