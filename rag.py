
import os
from pathlib import Path

# ChromaDB may download its default embedding model.
# Vercel's /tmp directory is writable.
if os.getenv("VERCEL"):
    os.environ["HOME"] = "/tmp"

import chromadb


class FoodRAG:
    """Retrieve food-name mappings; USDA supplies nutrient values."""

    def __init__(self, knowledge_file):
        self.client = chromadb.Client()

        self.collection = self.client.get_or_create_collection(
            "food_name_aliases"
        )

        path = Path(knowledge_file)

        lines = [
            line.strip()
            for line in path.read_text(encoding="utf-8").splitlines()
            if line.strip() and not line.lstrip().startswith("#")
        ]

        if lines:
            self.collection.upsert(
                ids=[f"food-{i}" for i in range(len(lines))],
                documents=lines
            )

    def get_search_name(self, detected_name):

        if self.collection.count() == 0:
            return detected_name

        match = self.collection.query(
            query_texts=[detected_name],
            n_results=1
        )

        documents = match.get("documents", [[]])[0]

        if documents and "=>" in documents[0]:
            return documents[0].split("=>", 1)[1].strip()

        return detected_name
