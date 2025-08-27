#adapters/fal_adapter.py
import os
import uuid
import asyncio
from dotenv import load_dotenv

# Optional: import the fal client. If it's not installed, the adapter will raise at call time.
try:
    import fal_client as fal
    FAL_CLIENT_AVAILABLE = True
except Exception:
    FAL_CLIENT_AVAILABLE = False

load_dotenv()
FAL_KEY = os.getenv("FAL_KEY")  # don't raise at import time

class FalAdapter:
    """
    Adapter for FAL text->video. This file does not raise at import time if FAL_KEY missing.
    The generate method will raise if the key or client is not available, so callers can fallback.
    """

    async def generate(self, prompt: str, aspect: str = "16:9"):
        # Check runtime availability
        if not FAL_KEY:
            raise RuntimeError("FAL_KEY not set in environment")

        if not FAL_CLIENT_AVAILABLE:
            raise RuntimeError("fal_client package not available")

        # fal.subscribe might be blocking — run in thread
        def call_subscribe():
            return fal.subscribe(
                "fal-ai/bytedance/seedance/v1/lite/text-to-video",
                arguments={
                    "prompt": prompt,
                    "aspect_ratio": aspect or "16:9",
                    "resolution": "720p",
                    "duration": "5"
                },
                with_logs=False
            )

        try:
            result = await asyncio.to_thread(call_subscribe)
            # Expecting result dict from fal client
            video_url = result.get("video", {}).get("url")
            if not video_url:
                raise RuntimeError("FAL response missing video url")

            return {
                "job_id": str(uuid.uuid4()),
                "status": "succeeded",
                "video_url": video_url,
                "provider": "fal",
                "meta": {"prompt": prompt, "aspect": aspect}
            }
        except Exception as e:
            # bubble error up to let the caller fallback to mock
            raise RuntimeError(f"FAL API Error: {e}")
