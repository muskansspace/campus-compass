from ai_engine.models import StudentProfile


class PromptBuilder:

    @staticmethod
    def build_society_summary(student: StudentProfile, recommendation: dict):

        prompt = f"""
You are an AI Career Mentor.

Analyze the student's profile and the recommended society.

Return ONLY valid JSON.

Student Profile

Name: {student.name}
Branch: {student.branch}
Year: {student.year}

Skills:
{", ".join(student.skills)}

Interests:
{", ".join(student.interests)}

Available Hours Per Week:
{student.hours_per_week}

Recommended Society:
{recommendation['society_name']}

Domain:
{recommendation['domain']}

Description:
{recommendation['description']}

Activities:
{recommendation['activities']}

Matched Skills:
{", ".join(recommendation['matched_skills'])}

Missing Skills:
{", ".join(recommendation['missing_skills'])}

Match Score:
{recommendation['score']}%

Return EXACTLY this JSON format.

{{
    "society_summary":[
        "...",
        "...",
        "...",
        "..."
    ],

    "benefits":[
        "...",
        "...",
        "...",
        "...",
        "..."
    ],

    "expected_work":[
        "...",
        "...",
        "..."
    ],

    "matched_skills":[
        "...",
        "..."
    ],

    "missing_skills":[
        "...",
        "..."
    ],

    "roadmap": {{
        "week1":"...",
        "week2":"...",
        "week3":"...",
        "week4":"..."
    }}
}}

Return ONLY JSON.
Do not add markdown.
Do not use ```json.
Do not explain anything outside the JSON.
"""

        return prompt