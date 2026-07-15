from ai_engine.bedrock import BedrockClient


def _clean(value):
    """
    Returns a stripped string, or None if the value is empty/missing/
    a literal placeholder like "N/A" (matches the same empty-detection
    used elsewhere in the app).
    """

    if value is None:
        return None

    text = str(value).strip()

    if text.lower() in ("", "n/a", "na", "none", "nan", "null"):
        return None

    return text


def build_blurb_prompt(society_name, domain, description, activities, other_aspects):
    """
    Builds a prompt asking the model to combine description + activities
    + other_aspects into ONE polished, factual "About" paragraph.
    Recruitment timing is shown separately in the UI, so it's
    intentionally excluded here. Returns None if there's no real
    information to work with at all.
    """

    fields = {
        "About": _clean(description),
        "Activities": _clean(activities),
        "Other details": _clean(other_aspects),
    }

    available = {k: v for k, v in fields.items() if v}

    if not available:
        return None

    raw_info = "\n".join(f"{label}: {value}" for label, value in available.items())

    prompt = f"""You are writing a short, friendly, informative "About" paragraph
about a college society for a society-discovery app used by students.

Society name: {society_name}
Domain: {domain}

Here is all the raw information available about this society:
{raw_info}

Write ONE polished paragraph (3-5 sentences) that naturally combines
ALL of the information above so a student browsing societies gets a
complete picture in one read. Rules:
- Use ONLY the information given above. Do not invent, assume, or add
  any fact, number, or detail that isn't present above.
- Write it as natural flowing prose — do not repeat the field labels
  ("About:", "Activities:" etc) in the output.
- Do NOT mention recruitment timing or dates — that's shown separately.
- Keep the tone warm and inviting, but factual — not salesy or
  exaggerated.
- Return ONLY the paragraph text. No markdown, no headers, no quotes.
"""

    return prompt


def generate_society_blurb(society_name, domain, description, activities, other_aspects):
    """
    Generates one polished "About" paragraph combining description,
    activities, and other_aspects. Returns None if there's no info to
    work with, or if the AI call fails (callers should fall back to
    raw fields in that case).
    """

    prompt = build_blurb_prompt(society_name, domain, description, activities, other_aspects)

    if prompt is None:
        return None

    client = BedrockClient()
    result = client.generate_text(prompt)

    if not result or not result.strip():
        return None

    return result.strip()