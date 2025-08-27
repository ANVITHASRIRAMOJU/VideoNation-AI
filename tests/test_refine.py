# tests/test_refine.py
import pytest
from httpx import AsyncClient
from main import app
import adapters.gemini as gemini_module

@pytest.mark.asyncio
async def test_refine_endpoint_monkeypatched(monkeypatch):
    async def fake_refine(self, prompt):
        return prompt + " (unit-refined)"

    monkeypatch.setattr(gemini_module.GeminiAdapter, "refine_prompt", fake_refine)

    async with AsyncClient(app=app, base_url="http://test") as ac:
        resp = await ac.post("/refine", json={"prompt": "sunset"})
        assert resp.status_code == 200
        data = resp.json()
        assert data["refined_prompt"] == "sunset (unit-refined)"
