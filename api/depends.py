from api.internal.services.organizations import OrganizationsService


async def get_organizations_service() -> "OrganizationsService":
    return OrganizationsService()
