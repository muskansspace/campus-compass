from ai_engine.models import StudentProfile
from ai_engine.recommendation_engine import RecommendationEngine


REQUIRED_PROFILE_FIELDS = (
    "name",
    "year",
    "branch",
    "skills",
    "interests",
    "hours_per_week",
)


def get_society_recommendations(profile: dict, limit: int = 5):
    """
    Receives a complete student profile from the backend
    and returns Top N ranked society recommendations.
    """

    if not isinstance(profile, dict):
        raise TypeError("profile must be a dictionary")

    missing_fields = [
        field
        for field in REQUIRED_PROFILE_FIELDS
        if field not in profile
    ]

    if missing_fields:
        raise ValueError(
            f"Missing required profile fields: {', '.join(missing_fields)}"
        )

    if not isinstance(profile["skills"], list):
        raise TypeError("skills must be a list")

    if not isinstance(profile["interests"], list):
        raise TypeError("interests must be a list")

    try:
        hours_per_week = float(profile["hours_per_week"])
    except (TypeError, ValueError):
        raise ValueError("hours_per_week must be a number")

    if hours_per_week < 0:
        raise ValueError("hours_per_week cannot be negative")

    if not isinstance(limit, int):
        raise TypeError("limit must be an integer")

    if limit <= 0:
        raise ValueError("limit must be greater than 0")

    student = StudentProfile(
        name=str(profile["name"]).strip(),
        branch=str(profile["branch"]).strip(),
        year=str(profile["year"]).strip(),
        skills=profile["skills"],
        interests=profile["interests"],
        hours_per_week=hours_per_week,
    )

    engine = RecommendationEngine(student)

    return engine.get_top_recommendations(limit)