import pytest
from fastapi import HTTPException

from api.config import settings
from api.security import require_api_key


async def test_valid_api_key_passes():
    result = await require_api_key(settings.API_KEY)
    assert result == settings.API_KEY


async def test_missing_api_key_raises_401():
    with pytest.raises(HTTPException) as exc_info:
        await require_api_key(None)
    assert exc_info.value.status_code == 401


async def test_wrong_api_key_raises_401():
    with pytest.raises(HTTPException) as exc_info:
        await require_api_key("totally-wrong-key")
    assert exc_info.value.status_code == 401


async def test_empty_string_raises_401():
    with pytest.raises(HTTPException) as exc_info:
        await require_api_key("")
    assert exc_info.value.status_code == 401
