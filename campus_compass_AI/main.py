from ai_engine.models import StudentProfile
from ai_engine.prompt_builder import PromptBuilder
from ai_engine.bedrock import BedrockClient

student = StudentProfile(
    name="Nancy",
    branch="CSE",
    year="2nd Year",
    skills=["Python", "Git", "AWS"],
    interests=["Artificial Intelligence", "Machine Learning"],
    hours_per_week=6
)

recommendation = {
    "society_name": "IEEE IGDTUW",
    "domain": "AI, ML, Robotics",
    "description": "Technical society focusing on innovation.",
    "activities": "Hackathons, Workshops, Research Projects",
    "matched_skills": ["Python", "AWS"],
    "missing_skills": ["Machine Learning"],
    "score": 92
}

prompt = PromptBuilder.build_society_summary(
    student,
    recommendation
)

client = BedrockClient()

response = client.generate(prompt)

print("\n============================")
print("CLAUDE RESPONSE")
print("============================\n")
print(response["society_summary"])

print(response["benefits"])

print(response["roadmap"]["week1"])