import re

import pandas as pd

from supabase_client import get_supabase_client

from ai_engine.models import StudentProfile
from ai_engine.utils import extract_keywords, canonicalize


class RecommendationEngine:
    """
    Generates personalized society recommendations
    based on a student's profile.

    Matching design (per Muskan's request):
    - ALL known information about a society (domain, skills required,
      description, activities, other_aspects) is combined into a single
      text blob and reduced to a set of recognized keywords.
    - The student's skills + interests are combined into a single set too
      (previously these were two separate silos: skills only matched
      against `skills_preferred_required`, interests only matched against
      `domain`/`activities` — so a trait like "public speaking" entered
      as a *skill* would never match a society whose *domain* was public
      speaking. That silo is gone now.)
    - Each matched keyword is worth a weight based on how rare it is
      across all societies (see _build_keyword_weights) — a specific,
      uncommon match (e.g. "public speaking") counts for much more than
      a generic one that half the societies share (e.g. "technology").
      This is what lets 2-3 genuine, specific matches land you in
      Excellent territory without everyone clustering at the same score
      just because they all share common tech buzzwords.
    - Time commitment is intentionally NOT part of this score — that's
      handled separately by the burnout calculator / best_combinations
      in analytics.py.
    """

    def __init__(self, student: StudentProfile):
        self.student = student
        self.societies = self.load_societies()
        self.keyword_weights = self._build_keyword_weights()

    # -------------------------------------------------
    # Load Society Data
    # -------------------------------------------------

    def load_societies(self):
        """
        Loads society data from the Supabase societies table.
        """

        response = (
            get_supabase_client()
            .table("societies")
            .select("*")
            .execute()
        )

        return pd.DataFrame(response.data)

    # -------------------------------------------------
    # Keyword Rarity Weights (IDF-style)
    # -------------------------------------------------

    def _build_keyword_weights(self):
        """
        Weighs each keyword by how rare it is across all societies.
        A keyword that appears in almost every society (e.g.
        "technology") is not very distinguishing, so it's worth little.
        A keyword that appears in only 1-2 societies (e.g. "public
        speaking") is highly distinguishing, so it's worth a lot.
        """

        total_societies = len(self.societies)

        if total_societies == 0:
            return {}

        doc_freq = {}

        for _, society in self.societies.iterrows():
            society_keywords = extract_keywords(
                self.build_society_text(society)
            )
            for kw in society_keywords:
                doc_freq[kw] = doc_freq.get(kw, 0) + 1

        weights = {}

        for kw, freq in doc_freq.items():
            share = freq / total_societies

            if share <= 0.15:
                weights[kw] = 40   # rare, highly specific
            elif share <= 0.30:
                weights[kw] = 25   # moderately specific
            elif share <= 0.50:
                weights[kw] = 15   # fairly common
            else:
                weights[kw] = 8    # generic, shared by most societies

        return weights

    def get_keyword_weight(self, keyword):
        return self.keyword_weights.get(keyword, 20)

    # -------------------------------------------------
    # Student Keywords (skills + interests, combined)
    # -------------------------------------------------

    def get_student_skills(self):
        """
        Returns student skills, canonicalized + with distinct
        cross-concept inference (e.g. knowing Python implies
        "programming" — a related but genuinely different concept,
        not a synonym of "python" itself).
        """

        skills = {
            canonicalize(skill.lower().strip())
            for skill in self.student.skills
        }

        expanded = set(skills)

        if "python" in skills:
            expanded.update(["programming", "coding"])

        if "git" in skills:
            expanded.update(["github", "version control"])

        if "aws" in skills:
            expanded.update(["cloud", "programming", "coding"])

        if "ai" in skills:
            expanded.update(["research"])

        return expanded

    def get_student_interests(self):
        """
        Returns student interests, canonicalized + with distinct
        cross-concept inference.
        """

        interests = {
            canonicalize(interest.lower().strip())
            for interest in self.student.interests
        }

        expanded = set(interests)

        if "ai" in interests:
            expanded.update(["research"])

        if "web development" in interests:
            expanded.update(["coding", "programming"])

        return expanded

    def get_student_keywords(self):
        """
        Union of skills + interests. A trait like "public speaking"
        counts the same whether the student listed it as a skill or
        an interest.
        """

        return self.get_student_skills() | self.get_student_interests()

    # -------------------------------------------------
    # Society Text (all known info combined into one blob)
    # -------------------------------------------------

    def build_society_text(self, society):
        """
        Combines every field describing the society into one paragraph
        so keyword matching isn't restricted to a single narrow field.
        """

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

    # -------------------------------------------------
    # Match Score
    # -------------------------------------------------

    def calculate_match_score(self, society):
        """
        Flat-weight keyword overlap between the student's combined
        skills+interests and the society's combined text.
        """

        student_keywords = self.get_student_keywords()

        society_text = self.build_society_text(society)
        society_keywords = extract_keywords(society_text)

        if not society_keywords:
            return {
                "score": 0,
                "matched": [],
                "missing": []
            }

        matched = student_keywords.intersection(society_keywords)
        missing = society_keywords - student_keywords

        score = sum(
            self.get_keyword_weight(kw) for kw in matched
        )
        score = min(score, 100)

        return {
            "score": score,
            "matched": sorted(matched),
            "missing": sorted(missing)
        }

    # -------------------------------------------------
    # Bonus Score (branch relevance)
    # -------------------------------------------------

    def calculate_bonus_score(self, society):
        """
        Awards bonus score if the student's
        branch aligns with the society.
        """

        bonus = 0

        branch_raw = self.student.branch.strip()

        if not branch_raw:
            return bonus

        description_raw = str(society.get("description", ""))
        other_aspects_raw = str(society.get("other_aspects", ""))

        # Short abbreviations (IT, CS, ME, ECE...) collide with common
        # English words ("it", "me") when lowercased — "...it is a great
        # society..." would otherwise match branch "IT". For anything
        # 4 characters or shorter, require an exact-case match, since
        # branch codes are almost always written uppercase in society
        # text, unlike ordinary lowercase English words.
        if len(branch_raw) <= 4:
            branch = branch_raw.upper()
            description = description_raw
            other_aspects = other_aspects_raw
        else:
            branch = branch_raw.lower()
            description = description_raw.lower()
            other_aspects = other_aspects_raw.lower()

        pattern = r"(?<![a-zA-Z0-9])" + re.escape(branch) + r"(?![a-zA-Z0-9])"

        if re.search(pattern, description):
            bonus += 5

        if re.search(pattern, other_aspects):
            bonus += 5

        return bonus

    # -------------------------------------------------
    # Final Score
    # -------------------------------------------------

    def calculate_final_score(self, match_score, bonus_score):
        return round(min(match_score + bonus_score, 100), 2)

    # -------------------------------------------------
    # Recommendation Level
    # -------------------------------------------------

    def get_recommendation_level(self, score):
        # With flat +10-per-keyword scoring: 1 strong match = 10,
        # 3+ genuine matches = 30-40+, 5+ = Excellent territory.
        if score >= 50:
            return "Excellent Match ⭐"

        elif score >= 30:
            return "Strong Match ✅"

        elif score >= 10:
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

            match_result = self.calculate_match_score(society)

            bonus_score = self.calculate_bonus_score(society)

            final_score = self.calculate_final_score(
                match_result["score"],
                bonus_score
            )

            level = self.get_recommendation_level(final_score)

            reason = []

            if match_result["matched"]:
                reason.append(
                    f"Matched: {', '.join(match_result['matched'])}"
                )

            if bonus_score:
                reason.append(
                    "Your academic background is relevant for this society."
                )

            recommendations.append({
                "society_id": society["id"],
                "society_name": society["society_name"],

                "domain": society["domain"],
                "description": society["description"],
                "activities": society["activities"],
                "other_aspects": society.get("other_aspects"),
                "ai_about": society.get("ai_about"),

                "instagram": society.get("contacts_instagram"),
                "website": society.get("website"),

                "commitment_per_week": society.get("commitment_per_week_num"),
                "commitment_text": society.get("commitment_text"),
                "recruitment_month": society.get("recruitment_month"),

                "score": final_score,
                "recommendation_level": level,

                "matched_skills": match_result["matched"],
                "missing_skills": match_result["missing"],

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