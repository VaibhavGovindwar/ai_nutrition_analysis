
from pathlib import Path
from difflib import get_close_matches


class FoodRAG:

    def __init__(self, knowledge_file):
        self.food_mappings = {}

        path = Path(knowledge_file)

        lines = path.read_text(encoding="utf-8").splitlines()

        for line in lines:
            line = line.strip()

            if not line or line.startswith("#") or "=>" not in line:
                continue

            alias, usda_name = line.split("=>", 1)

            self.food_mappings[alias.strip().lower()] = usda_name.strip()

    def get_search_name(self, detected_name):

        detected_name = detected_name.strip().lower()

        # Exact matching
        if detected_name in self.food_mappings:
            return self.food_mappings[detected_name]

        # Similar-name matching
        matches = get_close_matches(
            detected_name,
            self.food_mappings.keys(),
            n=1,
            cutoff=0.6
        )

        if matches:
            return self.food_mappings[matches[0]]

        # If no mapping is found, use the original food name
        return detected_name
