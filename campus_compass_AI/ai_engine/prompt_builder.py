from ai_engine.models import StudentProfile


class PromptBuilder:

    @staticmethod
    def build_society_summary(student: StudentProfile, recommendation: dict):

        prompt = f"""
You are an AI Career Mentor for Campus Compass.

Analyze the student's profile and the recommended society carefully.

Your goal is to provide personalized, practical, and realistic career guidance.

Follow these rules:

- Base every recommendation ONLY on the information provided.
- Explain why this society matches the student's profile.
- Mention the student's existing strengths.
- Explain how the matched skills helped in the recommendation.
- Clearly identify the missing skills.
- Suggest practical ways to improve the missing skills.
- Explain what the student can contribute if they join this society.
- Generate a realistic 4-week learning roadmap.
- If the recommendation score is high, confidently recommend joining.
- If the recommendation score is moderate, explain both strengths and areas for improvement.
- If the recommendation score is low, honestly explain why it is currently a weak match and encourage the student by suggesting how they can improve.
- Do not exaggerate recommendations.
- Do not invent skills, activities, or achievements that are not provided.
- Keep every point concise and actionable.

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

Recommendation Level:
{recommendation.get('recommendation_level', 'Not Available')}

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