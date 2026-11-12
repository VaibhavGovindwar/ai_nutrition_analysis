
import uuid
import tempfile
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask, render_template, request, send_from_directory
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge

from gemini_service import identify_foods
from rag import FoodRAG
from usda_api import get_food_nutrition, calculate_portion


BASE = Path(__file__).resolve().parent

load_dotenv(BASE / ".env")

app = Flask(__name__)

# Keep the complete request below Vercel's 4.5 MB limit.
app.config["MAX_CONTENT_LENGTH"] = 4 * 1024 * 1024

# Temporary image storage for Vercel.
UPLOADS = Path("/tmp/ai_nutrition_uploads")
UPLOADS.mkdir(parents=True, exist_ok=True)

rag = FoodRAG(BASE / "knowledge" / "food_aliases.txt")

ALLOWED = {"jpg", "jpeg", "png", "webp"}


def meal_totals(items):
    keys = [
        "calories_kcal",
        "protein_g",
        "carbohydrates_g",
        "fat_g",
        "fiber_g"
    ]

    totals = {}

    for key in keys:
        values = [item.get(key) for item in items]

        totals[key] = (
            round(sum(values), 2)
            if values and all(value is not None for value in values)
            else None
        )

    return totals


@app.errorhandler(RequestEntityTooLarge)
def handle_large_file(error):
    return render_template(
        "index.html",
        totals=None,
        food_names=[],
        error="Image upload is too large. Please upload smaller images."
    ), 413


@app.route("/", methods=["GET", "POST"])
def index():

    error = None
    totals = None
    food_names = []
    uploaded_paths = []

    if request.method == "POST":

        images = [
            image
            for image in request.files.getlist("food_images")
            if image and image.filename
        ]

        if not images:
            error = "Please select at least one food image."

        elif len(images) > 2:
            error = (
                "you limit has exceeded thank you for using AI nutrition."
            )

        elif any(
            "." not in image.filename
            or image.filename.rsplit(".", 1)[1].lower() not in ALLOWED
            for image in images
        ):
            error = "Please upload JPG, PNG or WEBP images only."

        else:

            try:
                nutrition_items = []

                for image in images:

                    extension = Path(
                        secure_filename(image.filename)
                    ).suffix.lower()

                    filename = f"{uuid.uuid4().hex}{extension}"
                    path = UPLOADS / filename

                    image.save(path)
                    uploaded_paths.append(path)

                    detected_foods = identify_foods(path)

                    for food in detected_foods:

                        food_name = food["name"]

                        if food_name not in food_names:
                            food_names.append(food_name)

                        search_name = rag.get_search_name(food_name)

                        data = get_food_nutrition(search_name)

                        grams = food.get("estimated_edible_grams")

                        if data and grams and grams > 0:
                            nutrition_items.append(
                                calculate_portion(data, grams)
                            )

                if not nutrition_items:

                    error = (
                        "No matching food nutrition data found. "
                        "Please try another image."
                    )

                else:
                    totals = meal_totals(nutrition_items)

            except Exception as exc:

                message = str(exc)

                if "429" in message or "RESOURCE_EXHAUSTED" in message:
                    error = (
                        "Gemini daily free-tier limit reached. "
                        "Please try again after the quota resets."
                    )

                elif "503" in message or "UNAVAILABLE" in message:
                    error = (
                        "The AI service is temporarily busy. "
                        "Please try again later."
                    )

                else:
                    app.logger.exception("Analysis failed")
                    error = (
                        "Analysis failed. Check your API keys and try again."
                    )

            finally:

                # Remove uploaded images after processing.
                for path in uploaded_paths:
                    try:
                        path.unlink(missing_ok=True)
                    except OSError:
                        app.logger.warning(
                            "Could not remove temporary upload: %s",
                            path
                        )

    return render_template(
        "index.html",
        totals=totals,
        food_names=food_names,
        error=error
    )

@app.route("/favicon.png")
def favicon():
    return send_from_directory(
        BASE / "public",
        "favicon.png"
    )

if __name__ == "__main__":
    app.run(debug=True)
