from ai_engine.models import StudentProfile
from ai_engine.recommendation_engine import RecommendationEngine
from ai_engine.prompt_builder import PromptBuilder
from ai_engine.bedrock import BedrockClient


# -------------------------------------------------
# Student Profile
# -------------------------------------------------

student = StudentProfile(
    name="Nancy",
    branch="CSE",
    year="2nd Year",
    skills=["Python", "Git", "AWS"],
    interests=["Artificial Intelligence", "Machine Learning"],
    hours_per_week=6
)


# -------------------------------------------------
# Get Best Society Recommendation
# -------------------------------------------------

engine = RecommendationEngine(student)

recommendation = engine.get_best_recommendation()

if recommendation is None:
    print("No recommendation found.")
    exit()


# -------------------------------------------------
# Build AI Prompt
# -------------------------------------------------

prompt = PromptBuilder.build_society_summary(
    student,
    recommendation
)


# -------------------------------------------------
# Generate AI Response
# -------------------------------------------------

client = BedrockClient()

response = client.generate(prompt)
if "error" in response:
    print("\n============================")
    print("AI ERROR")
    print("============================")
    print(response["error"])
    exit()


# -------------------------------------------------
# Display Results
# -------------------------------------------------
if "error" in response:  #Message--> API key expired
    print("\nAI ERROR")
    print(response["error"])
    exit()
print("\n============================")
print("TOP RECOMMENDED SOCIETY")
print("============================\n")

print(f"Society : {recommendation['society_name']}")
print(f"Score   : {recommendation['score']}%")

print("\n============================")
print("AI RESPONSE")
print("============================\n")

print("Society Summary:")
for point in response["society_summary"]:
    print(f"• {point}")

print("\nBenefits:")
for point in response["benefits"]:
    print(f"• {point}")

print("\nExpected Work:")
for point in response["expected_work"]:
    print(f"• {point}")

print("\nMatched Skills:")
for skill in response["matched_skills"]:
    print(f"• {skill}")

print("\nMissing Skills:")
for skill in response["missing_skills"]:
    print(f"• {skill}")

print("\n4-Week Roadmap:")
print(f"Week 1 : {response['roadmap']['week1']}")
print(f"Week 2 : {response['roadmap']['week2']}")
print(f"Week 3 : {response['roadmap']['week3']}")
print(f"Week 4 : {response['roadmap']['week4']}")