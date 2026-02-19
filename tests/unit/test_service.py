from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi import HTTPException

from api.internal.services.organizations import OrganizationsService


def _make_service(repo_mock: MagicMock) -> OrganizationsService:
    service = OrganizationsService()
    service.repo = repo_mock
    return service


async def test_get_by_id_raises_404_when_not_found():
    repo = MagicMock()
    repo.get_by_id = AsyncMock(return_value=None)
    service = _make_service(repo)

    with pytest.raises(HTTPException) as exc_info:
        await service.get_by_id(MagicMock(), org_id=999)

    assert exc_info.value.status_code == 404
    repo.get_by_id.assert_awaited_once()


async def test_get_by_id_returns_org_when_found():
    mock_org = MagicMock()
    repo = MagicMock()
    repo.get_by_id = AsyncMock(return_value=mock_org)
    service = _make_service(repo)

    result = await service.get_by_id(MagicMock(), org_id=1)

    assert result is mock_org


async def test_get_by_activity_delegates_without_descendants_by_default():
    repo = MagicMock()
    repo.get_by_activity = AsyncMock(return_value=[])
    service = _make_service(repo)

    await service.get_by_activity(MagicMock(), activity_id=5)

    repo.get_by_activity.assert_awaited_once()
    _, kwargs = repo.get_by_activity.call_args
    assert kwargs["include_descendants"] is False


async def test_get_by_activity_tree_passes_include_descendants_true():
    repo = MagicMock()
    repo.get_by_activity = AsyncMock(return_value=[])
    service = _make_service(repo)

    await service.get_by_activity(MagicMock(), activity_id=5, include_descendants=True)

    _, kwargs = repo.get_by_activity.call_args
    assert kwargs["include_descendants"] is True


async def test_get_by_radius_delegates_all_params():
    repo = MagicMock()
    repo.get_by_radius = AsyncMock(return_value=[])
    service = _make_service(repo)
    session = MagicMock()

    await service.get_by_radius(session, lat=55.7, lon=37.6, radius=500.0)

    repo.get_by_radius.assert_awaited_once_with(session, lat=55.7, lon=37.6, radius=500.0)
