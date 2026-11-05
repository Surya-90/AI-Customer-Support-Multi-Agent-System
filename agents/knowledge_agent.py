
from pathlib import Path
import re

# Locate the knowledge_base folder from the project root
BASE_DIR = Path(__file__).resolve().parent.parent
KNOWLEDGE_BASE_DIR = BASE_DIR / "knowledge_base"

STOP_WORDS = {
    "the", "is", "a", "an", "i", "my", "me", "we",
    "to", "and", "or", "of", "for", "in", "on",
    "it", "was", "what", "how", "can", "do", "does",
    "you", "your", "this", "that", "have", "has",
    "with", "please", "want", "get", "received",
    "customer", "order", "issue", "help"
}

# Connect common customer wording with policy terminology
SEARCH_SYNONYMS = {
    "broken": {"defective", "damaged", "faulty", "malfunctioning"},
    "broke": {"defective", "damaged", "faulty", "malfunctioning"},
    "damaged": {"broken", "defective", "faulty"},
    "defective": {"broken", "damaged", "faulty"},
    "replacement": {"replace", "exchange"},
    "replace": {"replacement", "exchange"},
    "exchange": {"replacement", "replace"},
    "money": {"refund", "payment"},
    "refund": {"money", "reimbursement"},
    "return": {"returns", "refund"},
    "returns": {"return", "refund"},
    "late": {"delayed", "delay"},
    "delayed": {"late", "delay"},
    "delay": {"late", "delayed"},
    "login": {"password", "account", "signin"},
    "signin": {"login", "password"},
    "password": {"login", "reset"},
    "shipping": {"delivery", "shipment"},
    "delivery": {"shipping", "shipment"},
    "shipment": {"shipping", "delivery"}
}


def tokenize(text):
    """Convert text into useful lowercase search words."""
    words = re.findall(r"[a-z0-9]+", text.lower())

    return {
        word for word in words
        if word not in STOP_WORDS and len(word) > 1
    }


def load_documents():
    """Read all Markdown documents from the knowledge base."""
    documents = []

    for file_path in KNOWLEDGE_BASE_DIR.glob("*.md"):
        content = file_path.read_text(encoding="utf-8")

        documents.append({
            "source": file_path.name,
            "content": content
        })

    return documents


def expand_query(query_words):
    """Build search groups containing original words and synonyms."""
    groups = []

    for word in query_words:
        related_words = SEARCH_SYNONYMS.get(word, set())
        groups.append({word} | related_words)

    return groups


def search_kb(query, top_k=3):
    """
    Search company documents using exact words and synonyms.
    Return the most relevant Markdown sections with source filenames.
    """

    query_words = tokenize(query)

    if not query_words:
        return []

    search_groups = expand_query(query_words)
    documents = load_documents()
    results = []

    for document in documents:

        # Split documents into Markdown sections
        sections = re.split(
            r"(?=^#{1,3}\s)",
            document["content"],
            flags=re.MULTILINE
        )

        for section in sections:
            section = section.strip()

            if not section:
                continue

            section_words = tokenize(section)

            score = 0
            matched_words = []

            for group in search_groups:
                matches = group.intersection(section_words)

                if matches:
                    matched_words.extend(sorted(matches))

                    # Exact query-word match gets a higher score
                    if any(word in section_words for word in group):
                        score += 2

            # Give a small bonus when matching words appear in headings
            heading = section.split("\n", 1)[0]
            heading_words = tokenize(heading)

            if heading_words.intersection(query_words):
                score += 1

            if score > 0:
                results.append({
                    "source": document["source"],
                    "passage": section,
                    "score": score,
                    "matched_words": list(dict.fromkeys(matched_words))
                })

    # Rank highest-scoring sections first
    results.sort(
        key=lambda item: (
            item["score"],
            len(item["matched_words"])
        ),
        reverse=True
    )

    return results[:top_k]


if __name__ == "__main__":

    questions = [
        "My NestCam arrived broken. Can I get a replacement?",
        "My order has not arrived and delivery is delayed.",
        "I forgot my password and cannot log in."
    ]

    for question in questions:
        matches = search_kb(question)

        print("\n" + "=" * 60)
        print("CUSTOMER QUESTION:", question)
        print("=" * 60)

        if not matches:
            print("No matching documents found.")

        for result in matches:
            print("\nSource:", result["source"])
            print("Score:", result["score"])
            print("Matched words:", result["matched_words"])
            print("Passage:\n", result["passage"])
