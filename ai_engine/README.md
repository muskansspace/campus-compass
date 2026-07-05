# Campus Compass AI Engine

The AI Engine powers personalized society recommendations and AI-generated guidance for Campus Compass.

It combines a rule-based recommendation system with Supabase society data and an AI model accessed through AWS Bedrock's OpenAI-compatible API.

## Features

- Fetches society data directly from Supabase
- Matches student skills with society requirements
- Matches student interests with society domains
- Matches student interests with society activities
- Evaluates weekly time commitment compatibility
- Applies branch-based bonus scoring
- Calculates weighted recommendation scores
- Ranks societies by recommendation score
- Identifies matched and missing skills
- Generates personalized AI guidance
- Generates a 4-week learning roadmap
- Returns structured JSON responses

## AI Engine Structure

```text
ai_engine/
|
|-- __init__.py
|-- bedrock.py
|-- config.py
|-- models.py
|-- prompt_builder.py
|-- recommendation_engine.py
|-- skill_gap.py
|-- utils.py
`-- README.md
```

## File Responsibilities

### `bedrock.py`

Handles communication with the AI model.

Responsibilities:

- Creates the OpenAI-compatible API client
- Uses the configured AWS Bedrock endpoint
- Sends prompts to the model
- Receives model responses
- Parses the response as JSON
- Returns errors in a structured format

### `config.py`

Loads AI configuration and environment variables.

Responsibilities:

- Loads the project-level `.env` file
- Reads recommendation weights
- Reads the AI API key
- Reads the API base URL
- Reads the model ID

### `models.py`

Defines the student profile data model used by the recommendation engine.

The profile contains information such as:

- Name
- Branch
- Academic year
- Skills
- Interests
- Available hours per week

### `prompt_builder.py`

Builds the structured prompt sent to the AI model.

The prompt contains:

- Student profile
- Recommended society
- Society domain
- Society description
- Society activities
- Matched skills
- Missing skills
- Recommendation score
- Recommendation level

The model is instructed to return valid JSON containing:

- Society summary
- Benefits
- Expected work
- Matched skills
- Missing skills
- Personalized 4-week roadmap

### `recommendation_engine.py`

Contains the core recommendation logic.

Responsibilities:

- Fetches societies from Supabase
- Processes student skills and interests
- Calculates individual matching scores
- Calculates the final weighted score
- Assigns a recommendation level
- Ranks societies by final score
- Returns recommendation results

### `skill_gap.py`

Contains reusable skill-gap analysis logic.

It compares the student's current skills with society skill requirements and identifies:

- Matched skills
- Missing skills

### `utils.py`

Contains keyword extraction utilities used by the recommendation engine.

It normalizes text and detects known skills, domains, tools, and activities.

## Recommendation Workflow

```text
Student Profile
       |
       v
Recommendation Engine
       |
       v
Fetch Societies from Supabase
       |
       v
Keyword Extraction
       |
       v
Skill Matching
       |
       v
Domain Matching
       |
       v
Activity Matching
       |
       v
Time Compatibility
       |
       v
Branch Bonus
       |
       v
Weighted Final Score
       |
       v
Rank Societies
       |
       v
Recommended Society
       |
       v
Prompt Builder
       |
       v
AWS Bedrock
(OpenAI-Compatible Responses API)
       |
       v
Structured JSON Guidance
```

## Recommendation Scoring

The recommendation engine currently evaluates societies using:

- Skill score
- Domain score
- Activity score
- Time compatibility score
- Branch bonus

The current weighted formula is:

```text
Final Score =
Skill Score × Skill Weight
+ Domain Score × Domain Weight
+ Activity Score × 0.20
+ Time Score × Time Weight
+ Branch Bonus
```

Recommendation weights are configured in `config.py`.

## Supabase Integration

Society data is loaded from the Supabase `societies` table.

The recommendation engine executes a query equivalent to:

```python
response = (
    supabase
    .table("societies")
    .select("*")
    .execute()
)
```

The returned records are converted into a Pandas DataFrame before recommendation processing.

The Excel dataset previously used by the AI module is no longer required.

## Environment Variables

The AI Engine uses the project-level `.env` file.

Required AI variables:

```env
OPENAI_API_KEY=your_bedrock_api_key
OPENAI_BASE_URL=your_bedrock_base_url
MODEL_ID=your_model_id
```

The Supabase client also requires:

```env
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
```

Do not commit the `.env` file.

## Install Dependencies

Run from the project root:

```bash
pip install -r requirements.txt
```

The AI Engine uses the shared project-level `requirements.txt`.

## Run the AI Pipeline

Run commands from the project root.

Activate the virtual environment.

Windows:

```bash
venv\Scripts\activate
```

Run the AI demo:

```bash
python ai_demo.py
```

The demo:

1. Creates a sample `StudentProfile`.
2. Fetches societies from Supabase.
3. Calculates recommendation scores.
4. Ranks the societies.
5. Selects the highest-ranked society.
6. Builds the AI prompt.
7. Sends the prompt to the configured model.
8. Parses the JSON response.
9. Displays personalized AI guidance.

## Using the Recommendation Engine

```python
from ai_engine.models import StudentProfile
from ai_engine.recommendation_engine import RecommendationEngine

student = StudentProfile(
    name="Student Name",
    branch="CSE",
    year="2nd Year",
    skills=["Python", "Git", "AWS"],
    interests=["AI", "Machine Learning"],
    hours_per_week=5,
)

engine = RecommendationEngine(student)

recommendations = engine.recommend()

best_recommendation = engine.get_best_recommendation()
```

## Using the AI Guidance Pipeline

```python
from ai_engine.bedrock import BedrockClient
from ai_engine.prompt_builder import PromptBuilder

prompt = PromptBuilder.build_society_summary(
    student,
    best_recommendation,
)

client = BedrockClient()

ai_response = client.generate(prompt)
```

## Backend Integration Contract

The intended application flow is:

```text
Backend
   |
   | Complete Student Profile
   v
AI Recommendation Module
   |
   | Top N Recommendations
   v
Backend
   |
   | Delete Existing Recommendations
   v
Supabase Recommendations Table
   |
   | Save New Recommendations
   v
Frontend
```

The backend is responsible for:

- Receiving the complete student profile
- Creating the `StudentProfile` object
- Calling the recommendation module
- Receiving Top N recommendation results
- Deleting previous recommendations for the user
- Saving new recommendations in Supabase
- Returning results to the frontend

The AI module should not directly manage user recommendation records.

## Current Status

Completed:

- Rule-based recommendation engine
- Skill matching
- Domain matching
- Activity matching
- Time compatibility analysis
- Branch bonus scoring
- Weighted ranking
- Recommendation levels
- Supabase society data integration
- AWS Bedrock integration
- Structured JSON parsing
- Personalized AI guidance
- Skill-gap output
- 4-week learning roadmap generation
- Shared project structure
- Shared project-level environment configuration
- Shared project-level dependencies

## Next Integration Tasks

- Return Top N recommendations instead of only one recommendation
- Include `society_id` in every recommendation result
- Accept the complete profile object from the backend
- Return recommendation results to the backend
- Improve keyword normalization and matching quality
- Add tests for recommendation scoring and ranking

## Security

Never commit:

- `.env`
- Supabase keys
- AWS Bedrock API keys
- API tokens
- Other credentials

Keep all secrets in the project-level `.env` file.
