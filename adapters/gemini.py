# adapters/gemini.py
import os
import asyncio
import logging
from dotenv import load_dotenv

# Try importing google genai SDK; if not installed we will fallback.
try:
    from google import genai
    from google.genai import types
    from google.genai.errors import ClientError
    GENAI_AVAILABLE = True
except Exception:
    GENAI_AVAILABLE = False

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def _local_refine(user_input: str) -> str:
    """Local fallback that extracts Style/Aspect if present and composes a concise cinematic prompt."""
    lines = [l.strip() for l in user_input.splitlines() if l.strip()]
    style = None
    aspect = None
    core_lines = []

    for ln in lines:
        low = ln.lower()
        if low.startswith("style:"):
            style = ln.split(":", 1)[1].strip()
        elif low.startswith("aspect:"):
            aspect = ln.split(":", 1)[1].strip()
        else:
            core_lines.append(ln)

    core = " ".join(core_lines).strip() or user_input.strip()

    parts = []
    parts.append(core.rstrip("."))
    if style:
        parts.append(f"Rendered in a {style} style")
    parts.append("with cinematic lighting, shallow depth of field, and fluid camera movement")
    if aspect:
        parts.append(f"framed for {aspect} aspect ratio")
    parts.append("conveying a moody, immersive atmosphere.")

    refined = ". ".join(parts)
    if not refined.endswith("."):
        refined += "."
    words = refined.split()
    if len(words) > 100:
        refined = " ".join(words[:100]).rstrip() + "."

    return refined


def _generate_text_sync(text_prompt: str) -> str:
    """
    Blocking call to genai if available; otherwise a local fallback.
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key or not GENAI_AVAILABLE:
        logger.info("genai not available or GOOGLE_API_KEY missing — using local fallback for refinement.")
        try:
            return _local_refine(text_prompt)
        except Exception:
            return text_prompt + " (refined)"

    instruction = (
        "Refine the following user input into a highly descriptive, cinematic video generation prompt. "
        "Include subject, environment, lighting, mood, camera angles, camera movement, colors, and style. "
        "If the user included a 'Style:' or 'Aspect:' line in their input, integrate that style and aspect "
        "ratio naturally into the output. Do not explain or add commentary. Only output the refined prompt, "
        "and keep it under 100 words.\n\n"
        f"User input: {text_prompt}"
    )

    try:
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model="gemini-2.5-flash-preview-05-20",
            contents=[types.Part(text=instruction)]
        )

        cand = None
        try:
            cand = response.candidates[0]
        except Exception:
            cand = None

        if cand is None:
            if hasattr(response, "output_text") and isinstance(response.output_text, str):
                return response.output_text.strip()
            return str(response)[:4000].strip()

        if hasattr(cand, "content") and isinstance(cand.content, str):
            return cand.content.strip()

        try:
            parts = getattr(cand.content, "parts", None)
            if parts and len(parts) > 0:
                first = parts[0]
                text = getattr(first, "text", None) or getattr(first, "content", None)
                if isinstance(text, str):
                    return text.strip()
        except Exception:
            pass

        if hasattr(cand, "text") and isinstance(cand.text, str):
            return cand.text.strip()
        if hasattr(cand, "message") and isinstance(cand.message, str):
            return cand.message.strip()

        if hasattr(response, "output_text") and isinstance(response.output_text, str):
            return response.output_text.strip()

        return str(cand)[:4000].strip()
    except ClientError as e:
        logger.exception("GenAI client error during refine")
        return f"API Error: {e}"
    except Exception:
        logger.exception("Unexpected error while refining with genai; falling back to local refine.")
        try:
            return _local_refine(text_prompt)
        except Exception:
            return text_prompt + " (refined)"


class GeminiAdapter:
    """Async wrapper around the blocking genai call."""

    async def refine_prompt(self, prompt: str) -> str:
        refined = await asyncio.to_thread(_generate_text_sync, prompt)
        return refined
