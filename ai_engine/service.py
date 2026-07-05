from ai_engine.models import StudentProfile
from ai_engine.recommendation_engine import RecommendationEngine


def get_society_recommendations(profile: dict, limit: int = 5):
    """
    Receives a complete student profile from the backend
    and returns Top N ranked society recommendations.
    """

    if not isinstance(profile, dict):
        raise TypeError("profile must be a dictionary")

    student = StudentProfile(
        name=profile.get("name", ""),
        branch=profile.get("branch", ""),
        year=profile.get("year", ""),
        skills=profile.get("skills") or [],
        interests=profile.get("interests") or [],
        hours_per_week=profile.get("hours_per_week", 0),
    )

    engine = RecommendationEngine(student)

    return engine.get_top_recommendations(limit)