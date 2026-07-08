from openai import skills
import pandas as pd

from supabase_client import supabase

from ai_engine.config import (
    DOMAIN_WEIGHT,
    SKILL_WEIGHT,
    TIME_WEIGHT,
    BONUS_WEIGHT,
    ACTIVITY_WEIGHT,
)

from ai_engine.models import StudentProfile
from ai_engine.utils import extract_keywords, expand_keywords

# -------------------------------------------------
# Skill Importance Weights
# -------------------------------------------------
# Used in calculate_skill_score() to weigh how important
# each skill is when computing the match score.
# Any skill not listed here falls back to a default
# weight of 5 (see SKILL_IMPORTANCE.get(skill, 5)).
SKILL_IMPORTANCE = {
    "python": 10,
    "machine learning": 10,
    "ai": 9,
    "artificial intelligence": 9,
    "programming": 8,
    "coding": 8,
    "git": 6,
    "github": 6,
    "version control": 6,
    "aws": 7,
    "cloud": 7,
    "cloud computing": 7,
    "technology": 5,
    "tech": 5,
    "research": 6,
}


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
    # Student Skills
    # -------------------------------------------------

    def get_student_skills(self):
        """
        Returns student skills with AI-friendly expansion.
        """

        skills = {
            skill.lower().strip()
            for skill in self.student.skills
        }

        expanded = set(skills)

        if "python" in skills:
            expanded.update([
                "programming",
                "coding",
                "technology",
                "tech"
            ])

        if "git" in skills:
            expanded.update([
                "github",
                "version control",
                "tech"
            ])

        if "aws" in skills:
            expanded.update([
        "cloud",
        "cloud computing",
        "technology",
        "tech",
        "programming",
        "coding"
    ])

        if "machine learning" in skills:
            expanded.update([
                "ai",
                "artificial intelligence",
                "research"
            ])

        return expanded

    # -------------------------------------------------
    # Student Interests
    # -------------------------------------------------

    def get_student_interests(self):
        """
        Returns student interests with semantic expansion.
        """

        interests = {
            interest.lower().strip()
            for interest in self.student.interests
        }

        expanded = set(interests)

        if "ai" in interests:
            expanded.update([
                "machine learning",
                "research",
                "technology"
            ])

        if "machine learning" in interests:
            expanded.update([
                "ai",
                "technology"
            ])

        if "web development" in interests:
            expanded.update([
                "coding",
                "programming",
                "technology"
            ])

        return expanded

    # -------------------------------------------------
    # Skill Matching
    # -------------------------------------------------

    def calculate_skill_score(self, society_skills):
        """
        Calculates weighted skill match score.
        """

        student_skills = self.get_student_skills()

        society_keywords = extract_keywords(society_skills)

        if not society_keywords:
            return {
                "score": 0,
                "matched": [],
                "missing": []
            }

        print("\n---------------------------")
        print("Student Skills :", student_skills)
        print("Society Skills :", society_keywords)

        matched = student_skills.intersection(
            society_keywords
        )

        missing = society_keywords - student_skills
        missing = {
    skill
    for skill in missing
    if skill not in {
        "mindset",
        "problem",
        "solving",
        "domain"
    }
}
        total_weight = 0
        matched_weight = 0

        for skill in society_keywords:

            weight = SKILL_IMPORTANCE.get(skill, 5)

            total_weight += weight

            if skill in matched:
                matched_weight += weight

        score = (
            matched_weight / total_weight
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

        matched = student_interests.intersection(
            domain_keywords
        )

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

        matched = student_interests.intersection(
            activity_keywords
        )

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
            return 50

        try:
            commitment = float(commitment)
        except (TypeError, ValueError):
            return 50

        diff = abs(
            self.student.hours_per_week - commitment
        )

        if diff <= 1:
            return 100
        elif diff <= 2:
            return 90
        elif diff <= 3:
            return 80
        elif diff <= 4:
            return 70
        elif diff <= 5:
            return 60
        else:
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

        final_score = (
        skill_score * 45 +
        domain_score * 25 +
        activity_score * 20 +
        time_score * 10
) / 100

        return round(final_score, 2)

    # -------------------------------------------------
    # Recommendation Level
    # -------------------------------------------------

    def get_recommendation_level(self,score):

        if score >= 25:
            return "Excellent Match ⭐"

        elif score >= 18:
            return "Strong Match ✅"

        elif score >= 12:
            return "Good Match 👍"

        else:
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
                reason.append(
                    f"Matched skills: {', '.join(skill_result['matched'])}"
                )

            if domain_result["matched"]:
                reason.append(
                    f"Matched interests: {', '.join(domain_result['matched'])}"
                )

            if activity_result["matched"]:
                activities = ", ".join(
                    activity_result["matched"][:2]
                )
                reason.append(
                    f"The society's activities match your interests like {activities}."
                )

            if time_score >= 70:
                reason.append(
                    "Time commitment fits your schedule."
                )

            if bonus_score:
                reason.append(
                    "Your academic background is relevant for this society."
                )
            print(
    f"{society['society_name']}"
    f" | Skill={skill_result['score']}"
    f" | Domain={domain_result['score']}"
    f" | Activity={activity_result['score']}"
    f" | Time={time_score}"
    f" | Bonus={bonus_score}"
    f" | Final={final_score}"
)
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
                    "\n".join(reason)
                    if reason
                    else "A good opportunity to explore new skills and experiences."
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