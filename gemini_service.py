import json
import os
from pathlib import Path
from dotenv import load_dotenv
from google import genai
from google.genai import types

BASE = Path(__file__).resolve().parent
load_dotenv(BASE / ".env")
KEY = os.getenv("GEMINI_API_KEY")
MODEL = os.getenv("GEMINI_MODEL", "gemini-3.6-flash")
if not KEY:
    raise ValueError("GEMINI_API_KEY missing in .env")
client = genai.Client(api_key=KEY)


def identify_foods(image_path):
    prompt = """
    Identify visible food items. Return JSON only:
    {"foods":[{"name":"food name","estimated_edible_grams":150}]}
    List each food component on a plate separately so their nutrients can be added.
    Include fruits and Indian foods such as rice, roti/chapati, dal, idli, dosa,
    chicken, meat, fish, sandwich and burger.
    Estimate edible weight in grams. Exclude bones, pits, shells and discarded parts.
    Do not return explanations. If no food is visible, return {"foods":[]}.
    """
    suffix = Path(image_path).suffix.lower()
    mime = {".jpg":"image/jpeg", ".jpeg":"image/jpeg", ".png":"image/png", ".webp":"image/webp"}.get(suffix, "image/jpeg")
    response = client.models.generate_content(
        model=MODEL,
        contents=[prompt, types.Part.from_bytes(data=Path(image_path).read_bytes(), mime_type=mime)],
        config=types.GenerateContentConfig(response_mime_type="application/json", temperature=0.1, max_output_tokens=700)
    )
    foods = json.loads(response.text).get("foods", [])
    clean = []
    for food in foods:
        try:
            name = str(food.get("name", "")).strip()
            grams = float(food.get("estimated_edible_grams"))
            if name and grams > 0:
                clean.append({"name": name, "estimated_edible_grams": grams})
        except (TypeError, ValueError):
            pass
    return clean
