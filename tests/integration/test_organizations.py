import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from api.config import settings
from api.internal.orm_models.dao import Activity, Building, Organization, Phone

API_KEY = settings.API_KEY
HEADERS = {settings.API_KEY_HEADER_NAME: API_KEY}


@pytest_asyncio.fixture
async def seed(db_session: AsyncSession):
    """Insert test data within the current transaction (rolled back after each test)."""
    b_moscow = Building(
        address="Moscow Test Center",
        location="SRID=4326;POINT(37.618423 55.751244)",
    )
    b_spb = Building(
        address="SPb Test Center",
        location="SRID=4326;POINT(30.335099 59.934280)",
    )
    db_session.add_all([b_moscow, b_spb])
    await db_session.flush()
    await db_session.refresh(b_moscow)
    await db_session.refresh(b_spb)

    it = Activity(name="IT Services Test")
    db_session.add(it)
    await db_session.flush()

    web = Activity(name="Web Dev Test", parent_id=it.id)
    db_session.add(web)
    await db_session.flush()

    frontend = Activity(name="Frontend Test", parent_id=web.id)
    db_session.add(frontend)
    await db_session.flush()

    org_moscow = Organization(name="Moscow Test Org", building_id=b_moscow.id)
    org_moscow.phones = [
        Phone(number="+7-111-111-1111"),
        Phone(number="+7-222-222-2222"),
    ]
    org_moscow.activities = [web, frontend]

    org_spb = Organization(name="SPb Test Org", building_id=b_spb.id)
    org_spb.activities = [it]

    db_session.add_all([org_moscow, org_spb])
    await db_session.flush()

    return {
        "buildings": {"moscow": b_moscow, "spb": b_spb},
        "activities": {"it": it, "web": web, "frontend": frontend},
        "orgs": {"moscow": org_moscow, "spb": org_spb},
    }


class TestAuthentication:
    async def test_no_key_returns_401(self, client: AsyncClient, seed):
        response = await client.get(f"/organizations/{seed['orgs']['moscow'].id}")
        assert response.status_code == 401

    async def test_wrong_key_returns_401(self, client: AsyncClient, seed):
        bad_headers = {settings.API_KEY_HEADER_NAME: "bad-key"}
        response = await client.get(f"/organizations/{seed['orgs']['moscow'].id}", headers=bad_headers)
        assert response.status_code == 401


class TestGetById:
    async def test_returns_full_organization(self, client: AsyncClient, seed):
        org_id = seed["orgs"]["moscow"].id
        response = await client.get(f"/organizations/{org_id}", headers=HEADERS)

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == org_id
        assert data["name"] == "Moscow Test Org"
        assert len(data["phones"]) == 2
        assert data["building"]["address"] == "Moscow Test Center"
        assert data["building"]["lat"] is not None
        assert data["building"]["lon"] is not None
        assert len(data["activities"]) == 2

    async def test_returns_404_for_nonexistent_id(self, client: AsyncClient, seed):
        response = await client.get("/organizations/999999", headers=HEADERS)
        assert response.status_code == 404


class TestGetByBuilding:
    async def test_returns_only_orgs_in_that_building(self, client: AsyncClient, seed):
        building_id = seed["buildings"]["moscow"].id
        response = await client.get(f"/buildings/{building_id}/organizations", headers=HEADERS)

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["name"] == "Moscow Test Org"

    async def test_returns_empty_for_building_without_orgs(self, client: AsyncClient, seed, db_session: AsyncSession):
        empty_building = Building(
            address="Empty Building Test",
            location="SRID=4326;POINT(0.0 0.0)",
        )
        db_session.add(empty_building)
        await db_session.flush()

        response = await client.get(f"/buildings/{empty_building.id}/organizations", headers=HEADERS)
        assert response.status_code == 200
        assert response.json() == []


class TestGetByActivity:
    async def test_exact_match_returns_direct_orgs_only(self, client: AsyncClient, seed):
        web_id = seed["activities"]["web"].id
        response = await client.get(f"/activities/{web_id}/organizations", headers=HEADERS)

        assert response.status_code == 200
        names = {o["name"] for o in response.json()}
        assert "Moscow Test Org" in names
        assert "SPb Test Org" not in names

    async def test_tree_returns_orgs_from_all_descendant_levels(self, client: AsyncClient, seed):
        it_id = seed["activities"]["it"].id
        response = await client.get(f"/activities/{it_id}/organizations/tree", headers=HEADERS)

        assert response.status_code == 200
        names = {o["name"] for o in response.json()}
        assert "Moscow Test Org" in names
        assert "SPb Test Org" in names


class TestGetByRadius:
    async def test_finds_nearby_org(self, client: AsyncClient, seed):
        response = await client.get(
            "/organizations/by_radius",
            params={"lat": 55.751244, "lon": 37.618423, "radius": 1000},
            headers=HEADERS,
        )

        assert response.status_code == 200
        names = {o["name"] for o in response.json()}
        assert "Moscow Test Org" in names
        assert "SPb Test Org" not in names

    async def test_excludes_orgs_outside_radius(self, client: AsyncClient, seed):
        response = await client.get(
            "/organizations/by_radius",
            params={"lat": 0.0, "lon": 0.0, "radius": 1},
            headers=HEADERS,
        )

        assert response.status_code == 200
        assert response.json() == []


class TestGetByRectangle:
    async def test_finds_orgs_inside_bbox(self, client: AsyncClient, seed):
        response = await client.get(
            "/organizations/by_rectangle",
            params={
                "lat_min": 55.70,
                "lat_max": 55.80,
                "lon_min": 37.50,
                "lon_max": 37.70,
            },
            headers=HEADERS,
        )

        assert response.status_code == 200
        names = {o["name"] for o in response.json()}
        assert "Moscow Test Org" in names
        assert "SPb Test Org" not in names

    async def test_excludes_orgs_outside_bbox(self, client: AsyncClient, seed):
        response = await client.get(
            "/organizations/by_rectangle",
            params={
                "lat_min": 0.0,
                "lat_max": 1.0,
                "lon_min": 0.0,
                "lon_max": 1.0,
            },
            headers=HEADERS,
        )

        assert response.status_code == 200
        assert response.json() == []


class TestSearchByName:
    async def test_partial_case_insensitive_match(self, client: AsyncClient, seed):
        response = await client.get("/organizations", params={"name": "moscow"}, headers=HEADERS)

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["name"] == "Moscow Test Org"

    async def test_no_results_for_unknown_name(self, client: AsyncClient, seed):
        response = await client.get("/organizations", params={"name": "zzz_not_exists_zzz"}, headers=HEADERS)

        assert response.status_code == 200
        assert response.json() == []
