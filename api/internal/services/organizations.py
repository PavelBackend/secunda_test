from ..repository.organizations import OrganizationsRepo

from sqlalchemy.ext.asyncio import AsyncSession


class OrganizationsService:
    def __init__(self):
        self.organizations_repo = OrganizationsRepo()


    async def get_all_organizations_by_filters(self, filters: dict, session: AsyncSession):
        return await self.organizations_repo.get_all_organizations_by_filters(filters=filters, session=session)