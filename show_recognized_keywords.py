"""
Shows exactly which keywords are being recognized (and used for
matching) from each society's combined text — so you can spot gaps
in KNOWN_KEYWORDS (ai_engine/utils.py) and add missing ones.

USAGE:
    python show_recognized_keywords.py
"""

from supabase_client import get_supabase_client
from ai_engine.utils import extract_keywords

supabase = get_supabase_client()

response = supabase.table("societies").select("*").execute()
societies = response.data or []

print(f"Found {len(societies)} societies.\n")
print("=" * 70)


def build_society_text(society):
    fields = [
        "domain",
        "skills_preferred_required",
        "description",
        "activities",
        "other_aspects",
    ]
    parts = []
    for field in fields:
        value = society.get(field)
        if value and str(value).lower() != "nan":
            parts.append(str(value))
    return " . ".join(parts)


for society in societies:
    name = society.get("society_name", "Unknown")
    text = build_society_text(society)
    keywords = extract_keywords(text)

    print(f"\n### {name}")
    if keywords:
        print(", ".join(sorted(keywords)))
    else:
        print("(no keywords recognized at all — check KNOWN_KEYWORDS)")

    print()
    print("=" * 70)