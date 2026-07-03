# Campus Compass AI

An AI-powered recommendation system that helps IGDTUW students discover the most suitable college societies based on their skills, interests, academic profile, and available time.

The system combines a rule-based recommendation engine with AWS Bedrock's OpenAI-compatible Responses API to generate personalized explanations, skill-gap analysis, and learning roadmaps.

---

## Features

- Personalized society recommendations
- Skill matching
- Domain matching
- Activity matching
- Time commitment analysis
- Skill gap identification
- AI-generated society summaries
- Personalized 4-week learning roadmap
- Structured JSON responses
- AWS Bedrock integration
- OpenAI-compatible Responses API

---

## Project Structure

```text
campus_compass_AI/
│
├── ai_engine/
│   ├── __init__.py
│   ├── bedrock.py                 # Handles AWS Bedrock API communication
│   ├── config.py                  # Configuration and environment variables
│   ├── models.py                  # Student profile data model
│   ├── prompt_builder.py          # Builds prompts for the AI model
│   ├── recommendation_engine.py   # Society recommendation logic
│   ├── skill_gap.py               # Skill gap analysis
│   └── utils.py                   # Utility functions
│
├── data/
│   └── igdtuw_societies_final.xlsx
│
├── .env
├── main.py
├── requirements.txt
└── README.md
```

---

## AI Workflow

```text
Student Profile
       │
       ▼
Recommendation Engine
       │
       ▼
Best Society Selection
       │
       ▼
Prompt Builder
       │
       ▼
AWS Bedrock
(OpenAI-Compatible Responses API)
       │
       ▼
AI Generated JSON Response
       │
       ▼
Frontend / User
```

---

## Technologies Used

| Category              | Technology                                     |
| --------------------- | ---------------------------------------------- |
| Language              | Python 3                                       |
| AI Model              | OpenAI-Compatible Responses API on AWS Bedrock |
| AI Integration        | OpenAI Python SDK                              |
| Data Processing       | Pandas                                         |
| Dataset               | Excel (.xlsx)                                  |
| Environment Variables | python-dotenv                                  |
| Version Control       | Git & GitHub                                   |

---

## Installation

### Clone the repository

```bash
git clone <repository-url>
```

### Navigate to the project

```bash
cd campus_compass_AI
```

### Create a virtual environment

```bash
python -m venv venv
```

### Activate the virtual environment

Windows

```bash
venv\Scripts\activate
```

Linux / macOS

```bash
source venv/bin/activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Configure environment variables

Create a `.env` file and add:

```env
OPENAI_API_KEY=your_bedrock_api_key
OPENAI_BASE_URL=your_bedrock_base_url
MODEL_ID=openai.gpt-oss-120b
```

### Run the project

```bash
python main.py
```

---

## Recommendation Pipeline

The recommendation engine analyzes each society by comparing it with the student's profile. A weighted scoring approach is used to identify the most suitable society.

The recommendation process consists of the following steps:

1. Load the society dataset from the Excel file.
2. Extract the student's skills, interests, branch, and available weekly hours.
3. Calculate individual scores based on:
   - Skill Matching
   - Domain Matching
   - Activity Matching
   - Time Commitment
   - Branch Bonus
4. Combine the individual scores using predefined weights to generate a final recommendation score.
5. Rank all societies in descending order of their scores.
6. Select the highest-ranked society.
7. Pass the recommendation details to the Prompt Builder.
8. Send the generated prompt to the AWS Bedrock model.
9. Receive a structured JSON response containing:
   - Society summary
   - Benefits of joining
   - Expected contributions
   - Matched skills
   - Missing skills
   - Personalized 4-week learning roadmap

   ***

## AI Output

After identifying the most suitable society, the recommendation details are passed to the AI model through AWS Bedrock.

The AI analyzes the student's profile along with the recommended society and generates a structured JSON response containing:

- Society Summary
- Benefits of Joining
- Expected Contributions
- Matched Skills
- Missing Skills
- Personalized 4-Week Learning Roadmap

The JSON response is designed to be easily consumed by frontend applications, enabling dynamic rendering of recommendations without additional text processing.
