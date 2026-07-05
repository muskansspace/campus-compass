from ai_engine.utils import extract_keywords


class SkillGapAnalyzer:

    @staticmethod
    def analyze(student_skills, society_skills):

        student_skills = {
            skill.lower().strip()
            for skill in student_skills
        }

        society_skills = extract_keywords(society_skills)

        if not society_skills:
            return {
                "matched": [],
                "missing": [],
                "score": 0
            }

        matched = student_skills.intersection(society_skills)

        missing = society_skills - student_skills

        score = (len(matched) / len(society_skills)) * 100

        return {
            "matched": sorted(list(matched)),
            "missing": sorted(list(missing)),
            "score": round(score, 2)
        }