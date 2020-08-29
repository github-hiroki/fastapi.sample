# Copyright 2020- hiroki.h Inc.

import pytest
from httpx import AsyncClient

from main import app


@pytest.mark.asyncio
async def test_get_root():
    async with AsyncClient(app=app, base_url='http://test') as ac:
        response = await ac.get('/')
        pass
    assert response.status_code == 200
    return
