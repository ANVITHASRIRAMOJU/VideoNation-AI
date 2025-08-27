
import pytest
from httpx import AsyncClient
from main import app

@pytest.mark.asyncio
async def test_generate_mock():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        resp = await ac.post("/generate", json={"prompt": "sunset"})
        assert resp.status_code == 200
        data = resp.json()
        print("Response:", data)
        assert "job_id" in data
        assert "video_url" in data

