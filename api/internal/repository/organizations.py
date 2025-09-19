from typing import Any, Callable, Dict

from geoalchemy2 import Geography
from sqlalchemy import and_, cast, func, literal, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased

from ..orm_models.dao import Activity, Building, Organization


class OrganizationsRepo:
    async def get_all_organizations_by_filters(
        self, filters: Dict[str, Any], session: AsyncSession
    ):
        stmt = select(Organization)

        key = (
            "radius"
            if "radius" in filters
            else next(
                k
                for k in ("org_id", "name", "building_id", "activity_id")
                if k in filters
            )
        )

        handlers: Dict[str, Callable[[Any], Any]] = {
            "org_id": lambda v: self._h_org_id(stmt, int(v)),
            "name": lambda v: self._h_name(stmt, str(v)),
            "building_id": lambda v: self._h_building(stmt, int(v)),
            "activity_id": lambda v: self._h_activity(
                stmt,
                int(v),
                include_descendants=(filters.get("activity_scope") == "tree"),
            ),
            "radius": lambda _: self._h_radius(
                stmt,
                lat=float(filters["lat"]),
                lon=float(filters["lon"]),
                radius=float(filters["radius"]),
            ),
        }

        stmt = handlers[key](filters.get(key))
        result = await session.execute(stmt)
        return result.scalars().unique().all()

    def _h_org_id(self, stmt, org_id: int):
        return stmt.where(Organization.id == org_id)

    def _h_name(self, stmt, name: str):
        return stmt.where(Organization.name.ilike(f"%{name}%"))

    def _h_building(self, stmt, building_id: int):
        return stmt.where(Organization.building_id == building_id)

    def _h_activity(self, stmt, activity_id: int, *, include_descendants: bool):
        if not include_descendants:
            return stmt.join(Organization.activities).where(Activity.id == activity_id)

        cte = (
            select(Activity.id.label("id"), literal(0).label("lvl"))
            .where(Activity.id == activity_id)
            .cte("activity_tree", recursive=True)
        )
        a2 = aliased(Activity)
        cte = cte.union_all(
            select(a2.id, cte.c.lvl + 1).where(
                and_(a2.parent_id == cte.c.id, cte.c.lvl < 2)
            )
        )
        return stmt.join(Organization.activities).where(
            Activity.id.in_(select(cte.c.id))
        )

    def _h_radius(self, stmt, *, lat: float, lon: float, radius: float):
        point = cast(func.ST_SetSRID(func.ST_MakePoint(lon, lat), 4326), Geography)
        return stmt.join(Building, Building.id == Organization.building_id).where(
            func.ST_DWithin(cast(Building.location, Geography), point, radius)
        )
