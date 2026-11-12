import os
import requests
from pathlib import Path
from dotenv import load_dotenv

BASE = Path(__file__).resolve().parent
load_dotenv(BASE / ".env")
KEY = os.getenv("USDA_API_KEY")
URL = "https://api.nal.usda.gov/fdc/v1"
if not KEY:
    raise ValueError("USDA_API_KEY missing in .env")


def get_food_nutrition(name):
    response = requests.post(
        f"{URL}/foods/search", params={"api_key": KEY},
        json={"query": name, "pageSize": 8, "dataType": ["Foundation", "SR Legacy", "Survey (FNDDS)"]},
        timeout=30
    )
    response.raise_for_status()
    records = response.json().get("foods", [])
    if not records:
        return None

    terms = [w.lower() for w in name.replace(",", " ").split() if len(w) > 2]
    record = max(records, key=lambda r: sum(w in r.get("description", "").lower() for w in terms))
    detail = requests.get(f"{URL}/food/{record['fdcId']}", params={"api_key": KEY}, timeout=30)
    detail.raise_for_status()
    data = detail.json()

    nutrients = {}
    for row in data.get("foodNutrients", []):
        nutrient = row.get("nutrient", {})
        nid, amount = nutrient.get("id"), row.get("amount")
        if amount is None:
            continue
        if nid == 1003: nutrients["protein_g"] = float(amount)
        elif nid == 1004: nutrients["fat_g"] = float(amount)
        elif nid == 1005: nutrients["carbohydrates_g"] = float(amount)
        elif nid == 1079: nutrients["fiber_g"] = float(amount)
        elif nid in (2048, 2047, 1008) and "calories_kcal" not in nutrients:
            nutrients["calories_kcal"] = float(amount)

    return {"food_name": data.get("description", name), "nutrients_per_100g": nutrients}


def calculate_portion(food, grams):
    per100 = food["nutrients_per_100g"]
    result = {}
    for key in ("calories_kcal", "protein_g", "carbohydrates_g", "fat_g", "fiber_g"):
        value = per100.get(key)
        result[key] = round(value * grams / 100, 2) if value is not None else None
    return result
