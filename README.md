# 🧭 Campus Compass

An AI-powered web application designed for **IGDTUW students** to discover, compare, and choose college societies based on their interests, skills, and availability.

Campus Compass helps students make informed decisions by providing personalized society recommendations, AI-generated skill gap analysis, workload estimation, and opportunities to connect with like-minded peers.

---

## ✨ Features

### 🔐 Authentication

* Secure Sign Up & Login using **Supabase Authentication**
* User profiles securely stored in Supabase

### 👤 Personalized Profile

Each user creates a profile by providing:

* Skills
* Interests
* Academic Year
* Available hours per week
* Optional LinkedIn profile
* Consent to share LinkedIn with other students

---

## 🏠 Home Dashboard

After logging in, users complete their profile, which is used to generate personalized recommendations.

---

## 🎯 Personalized Society Recommendations

Societies are recommended based on the user's profile.

Each recommendation includes:

* Match percentage
* Society description
* Domains
* Activities
* Weekly commitment
* Recruitment timeline
* Instagram/Website links

---

## 🤖 AI Skill Gap Analysis

For every recommended society, Campus Compass generates a personalized roadmap highlighting:

* Current strengths
* Skills to develop
* Suggested learning roadmap
* Preparation strategy for recruitment

---

## ❤️ Favourites

Users can save societies they are interested in.

The favourites page includes:

* Saved societies
* Burnout calculator based on available hours per week
* Recommended society combinations with balanced workload

---

## 🤝 Connect with Peers

Students who opt in can connect with others interested in the same societies through their LinkedIn profiles.

Privacy is respected:

* LinkedIn sharing is completely optional.
* Only users who provide consent are displayed.

---

## 💬 Feedback

Students can submit feedback, which is securely stored in Supabase for future improvements.

---

# 🛠 Tech Stack

| Category        | Technology        |
| --------------- | ----------------- |
| Frontend        | Streamlit         |
| Backend         | Python            |
| Database        | Supabase          |
| Authentication  | Supabase Auth     |
| Version Control | Git & GitHub      |

---

# 📂 Project Workflow

```text
Sign In / Sign Up
        │
        ▼
Home Dashboard
        │
        ▼
Complete Profile
(skills, interests, hours/week,
year, LinkedIn, privacy preference)
        │
        ▼
Personalized Recommendations
        │
        ▼
Select Society
        │
        ├── AI Skill Gap Analysis
        └── Save as Interested
                    │
                    ▼
             Favourites Page
                    │
        ├── Burnout Calculator
        └── Best Society Combination
                    │
                    ▼
             Connect with Peers
                    │
                    ▼
              Submit Feedback
```
---

# 👥 Team

Developed to simplify society exploration and help IGDTUW students discover communities aligned with their interests, skills, and goals.