"""
Text preprocessing utilities: cleaning and simple skill extraction
"""
import re
from typing import List, Set


def clean_text(text: str) -> str:
    """Lowercase and remove extra whitespace and common punctuation"""
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s-]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def extract_keywords(text: str, keywords: List[str]) -> Set[str]:
    """Return a set of keywords found in the text based on simple substring matching.

    Note: This is intentionally simple and deterministic. For better results, use spaCy
    or a named-entity approach.
    """
    text = clean_text(text)
    found = set()
    # normalize keywords
    normalized = [k.lower().strip() for k in keywords]
    for k in normalized:
        if k in text:
            found.add(k)
    return found


# common utility to tokenize or return just words
def tokenize(text: str) -> List[str]:
    text = clean_text(text)
    return [w for w in text.split(" ") if w]
