#adapters/mock.py
import uuid

PLACEHOLDER_VIDEO_URL = "/mockvideos/pup.mp4"

class MockAdapter:
    async def generate(self, prompt: str):
        return {
            "job_id": str(uuid.uuid4()),
            "status": "succeeded",
            "video_url": PLACEHOLDER_VIDEO_URL,
            "provider": "mock",
            "meta": {"prompt": prompt}
        }

# Quick check
if __name__ == "__main__":
    import asyncio
    adapter = MockAdapter()
    result = asyncio.run(adapter.generate("test prompt"))
    print("Mock result:", result)



    
