import pandas as pd

from supabase_client import supabase

from ai_engine.config import (
    DOMAIN_WEIGHT,
    SKILL_WEIGHT,
    TIME_WEIGHT,
    BONUS_WEIGHT,
)

from ai_engine.models import StudentProfile
from ai_engine.utils import extract_keywords


class RecommendationEngine:
    """
    Generates personalized society recommendations
    based on a student's profile.
    """

    def __init__(self, student: StudentProfile):
        self.student = student
        self.societies = self.load_societies()

    # -------------------------------------------------
    # Load Society Data
    # -------------------------------------------------

    def load_societies(self):
        """
        Loads society data from the Supabase societies table.
        """

        response = (
            supabase
            .table("societies")
            .select("*")
            .execute()
        )

        return pd.DataFrame(response.data)

    # -------------------------------------------------
    # Student Keywords
    # -------------------------------------------------

    def get_student_skills(self):
        """
        Returns student skills in lowercase.
        """

        return {
            skill.lower().strip()
            for skill in self.student.skills
        }

    def get_student_interests(self):
        """
        Returns student interests in lowercase.
        """

        return {
            interest.lower().strip()
            for interest in self.student.interests
        }

    # -------------------------------------------------
    # Skill Matching
    # -------------------------------------------------

    def calculate_skill_score(self, society_skills):
        """
        Calculates skill match score.
        """

        student_skills = self.get_student_skills()
        society_keywords = extract_keywords(society_skills)

        if not society_keywords:
            return {
                "score": 0,
                "matched": [],
                "missing": []
            }

        matched = student_skills.intersection(society_keywords)
        missing = society_keywords - student_skills

        score = (
            len(matched)
            / len(society_keywords)
        ) * 100

        return {
            "score": round(score, 2),
            "matched": sorted(list(matched)),
            "missing": sorted(list(missing))
        }

    # -------------------------------------------------
    # Domain Matching
    # -------------------------------------------------

    def calculate_domain_score(self, domain):
        """
        Calculates domain match score.
        """

        student_interests = self.get_student_interests()
        domain_keywords = extract_keywords(domain)

        if not domain_keywords:
            return {
                "score": 0,
                "matched": []
            }

        matched = student_interests.intersection(domain_keywords)

        score = (
            len(matched)
            / len(domain_keywords)
        ) * 100

        return {
            "score": round(score, 2),
            "matched": sorted(list(matched))
        }

    # -------------------------------------------------
    # Activity Matching
    # -------------------------------------------------

    def calculate_activity_score(self, activities):
        """
        Calculates activity match score.
        """

        student_interests = self.get_student_interests()
        activity_keywords = extract_keywords(activities)

        if not activity_keywords:
            return {
                "score": 0,
                "matched": []
            }

        matched = student_interests.intersection(activity_keywords)

        score = (
            len(matched)
            / len(activity_keywords)
        ) * 100

        return {
            "score": round(score, 2),
            "matched": sorted(list(matched))
        }

    # -------------------------------------------------
    # Time Commitment
    # -------------------------------------------------

    def calculate_time_score(self, commitment):
        """
        Calculates time compatibility score.
        """

        if pd.isna(commitment):
            return 100

        try:
            commitment = float(commitment)
        except (TypeError, ValueError):
            return 100

        difference = abs(
            self.student.hours_per_week - commitment
        )

        if difference <= 1:
            return 100

        if difference <= 3:
            return 70

        return 40

    # -------------------------------------------------
    # Bonus Score
    # -------------------------------------------------

    def calculate_bonus_score(self, society):
        """
        Awards bonus score if the student's
        branch aligns with the society.
        """

        bonus = 0

        description = str(
            society["description"]
        ).lower()

        other_aspects = str(
            society["other_aspects"]
        ).lower()

        if self.student.branch.lower() in description:
            bonus += 5

        if self.student.branch.lower() in other_aspects:
            bonus += 5

        return bonus

    # -------------------------------------------------
    # Final Score
    # -------------------------------------------------

    def calculate_final_score(
        self,
        skill_score,
        domain_score,
        activity_score,
        time_score,
        bonus_score
    ):
        """
        Calculates the final recommendation score.
        """

        final_score = (
            skill_score * (SKILL_WEIGHT / 100)
            + domain_score * (DOMAIN_WEIGHT / 100)
            + activity_score * 0.20
            + time_score * (TIME_WEIGHT / 100)
            + bonus_score
        )

        return round(final_score, 2)

    # -------------------------------------------------
    # Recommendation Level
    # -------------------------------------------------

    def get_recommendation_level(self, score):
        """
        Returns a confidence level for the recommendation.
        """

        if score >= 80:
            return "Excellent Match 🌟"

        if score >= 60:
            return "Strong Match ✅"

        if score >= 40:
            return "Good Match 👍"

        return "Explore if Interested 📘"

    # -------------------------------------------------
    # Recommendation Engine
    # -------------------------------------------------

    def recommend(self):
        """
        Generates and ranks society recommendations.
        """

        recommendations = []

        for _, society in self.societies.iterrows():

            skill_result = self.calculate_skill_score(
                society["skills_preferred_required"]
            )

            domain_result = self.calculate_domain_score(
                society["domain"]
            )

            activity_result = self.calculate_activity_score(
                society["activities"]
            )

            time_score = self.calculate_time_score(
                society["commitment_per_week_num"]
            )

            bonus_score = self.calculate_bonus_score(
                society
            )

            final_score = self.calculate_final_score(
                skill_result["score"],
                domain_result["score"],
                activity_result["score"],
                time_score,
                bonus_score
            )

            level = self.get_recommendation_level(
                final_score
            )

            reason = []

            if skill_result["matched"]:
                reason.append("Skill match")

            if domain_result["matched"]:
                reason.append("Interest alignment")

            if time_score >= 70:
                reason.append("Suitable commitment")

            recommendations.append({
    "society_id": society["id"],
    "society_name": society["society_name"],

    "domain": society["domain"],
    "description": society["description"],
    "activities": society["activities"],

    "instagram": society.get("contacts_instagram"),
    "website": society.get("website"),

    "commitment_per_week": society.get("commitment_per_week_num"),
    "commitment_text": society.get("commitment_text"),
    "recruitment_month": society.get("recruitment_month"),

    "score": final_score,
    "recommendation_level": level,

    "matched_skills": skill_result["matched"],
    "missing_skills": skill_result["missing"],
    "matched_interests": domain_result["matched"],

    "reason": (
        ", ".join(reason)
        if reason
        else "General Recommendation"
    )
})

        recommendations.sort(
            key=lambda x: x["score"],
            reverse=True
        )

        return recommendations

    # -------------------------------------------------
    # Best Recommendation
    # -------------------------------------------------

    def get_best_recommendation(self):
        """
        Returns the highest-ranked recommendation.
        """

        recommendations = self.recommend()

        if not recommendations:
            return None

        return recommendations[0]

    # -------------------------------------------------
    # Top Recommendations
    # -------------------------------------------------

    def get_top_recommendations(self, limit=5):
        """
        Returns the highest-ranked Top N society recommendations.
        """

        if limit <= 0:
            return []

        recommendations = self.recommend()

        return recommendations[:limit]