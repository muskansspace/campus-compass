import streamlit as st
from supabase_client import supabase

st.set_page_config(
    page_title="Campus Compass | Home",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .stApp { background: #2A252A; }
    .block-container { padding-top: 2rem !important; }

    [data-testid="stSidebar"] {
        background: #5E4955 !important;
        border-right: 1px solid #996888 !important;
    }
    [data-testid="stSidebar"] * { color: #C6DDF0 !important; }
    [data-testid="stSidebar"] .stButton > button {
        background: transparent !important;
        color: #C99DA3 !important;
        border: 1px solid #996888 !important;
        border-radius: 8px !important;
        width: 100% !important;
        font-weight: 500 !important;
    }
    [data-testid="stSidebar"] .stButton > button:hover {
        background: #996888 !important;
        color: #ffffff !important;
    }

    h1, h2, h3 { color: #C6DDF0 !important; }

    .intro-card {
        background: #5E4955;
        border: 1px solid #996888;
        border-radius: 16px;
        padding: 2rem;
        margin-bottom: 1.5rem;
    }
    .intro-card h2 {
        color: #C6DDF0 !important;
        font-size: 1.4rem;
        margin-bottom: 0.5rem;
    }
    .intro-card p {
        color: #C99DA3;
        font-size: 0.95rem;
        line-height: 1.6;
        margin: 0;
    }

    .stTextInput label, .stNumberInput label,
    .stMultiSelect label, .stSelectbox label,
    .stRadio label {
        color: #C99DA3 !important;
        font-size: 0.85rem !important;
        font-weight: 500 !important;
    }

    .stTextInput > div > div > input,
    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input {
        background-color: #3d2e38 !important;
        color: #C6DDF0 !important;
        caret-color: #C6DDF0 !important;
        -webkit-text-fill-color: #C6DDF0 !important;
        border: 1px solid #996888 !important;
        border-radius: 8px !important;
        opacity: 1 !important;
    }

    .stMultiSelect > div {
        background: #3d2e38 !important;
        border: 1px solid #996888 !important;
        border-radius: 8px !important;
        color: #C6DDF0 !important;
    }

    .stSelectbox > div > div {
        background: #3d2e38 !important;
        border: 1px solid #996888 !important;
        border-radius: 8px !important;
        color: #C6DDF0 !important;
    }

    .stButton > button {
        background: #996888 !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        padding: 0.6rem 1.5rem !important;
        transition: all 0.2s !important;
    }
    .stButton > button:hover {
        background: #C99DA3 !important;
        color: #2A252A !important;
    }

    .stRadio > div { gap: 1rem !important; }
    .stRadio label p {
        color: #ffffff !important;
        font-size: 0.9rem !important;
    }

    .stMultiSelect span[data-baseweb="tag"] {
        background: #996888 !important;
        color: #ffffff !important;
        border-radius: 20px !important;
    }

    [data-baseweb="select"] > div {
        background: #3d2e38 !important;
        border: 1px solid #996888 !important;
        border-radius: 8px !important;
        color: #C6DDF0 !important;
    }
    [data-baseweb="menu"] { background: #3d2e38 !important; }
    [data-baseweb="option"] {
        background: #3d2e38 !important;
        color: #C6DDF0 !important;
    }
    [data-baseweb="option"]:hover { background: #5E4955 !important; }

    [data-baseweb="select"] svg {
        fill: #C99DA3 !important;
        opacity: 1 !important;
        display: block !important;
    }

    hr { border-color: #996888 !important; }
</style>
""", unsafe_allow_html=True)

# ── Auth check ──
if not st.session_state.get("logged_in"):
    st.switch_page("App.py")

# ── Fetch existing profile ──
existing = None
try:
    result = supabase.table("profiles").select("*").eq(
        "user_id", st.session_state["user_id"]
    ).execute()
    if result.data:
        existing = result.data[0]
        st.session_state["user_name"] = existing["name"]
except:
    pass

# ── Sidebar ──
with st.sidebar:
    st.markdown(f"""
    <div style="padding: 1rem 0; text-align:center;">
        <div style="font-size:1.8rem">🧭</div>
        <p style="color:#C6DDF0; font-weight:600; margin:0.3rem 0;">Campus Compass</p>
        <p style="color:#C99DA3; font-size:0.8rem;">{st.session_state.get('email','')}</p>
    </div>
    <hr style="border-color:#996888; margin-bottom:1rem;">
    """, unsafe_allow_html=True)

    if st.button("Logout"):
        st.session_state.clear()
        st.rerun()

# ── Welcome ──
name_display = st.session_state.get("user_name", "there")
st.markdown(f"""
<h1 style="color:#C6DDF0; margin-bottom:0.2rem;">
    👋 Welcome, {name_display}!
</h1>
<p style="color:#C99DA3; margin-bottom:1.5rem; font-size:0.95rem;">
    Let's find your perfect society match.
</p>
""", unsafe_allow_html=True)

# ── Intro card ──
st.markdown("""
<div class="intro-card">
    <h2>🧭 What is Campus Compass?</h2>
    <p>
        Every student has a society waiting for them. Campus Compass matches you 
        with IGDTUW societies based on what you love, what you know, and how much 
        time you have — so you spend less time searching and more time doing.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("### 📋 Your Profile")

# ── Predefined options ──
SKILLS_OPTIONS = [
    "Python", "Java", "C++", "Web Development",
    "Machine Learning", "UI/UX Design", "Public Speaking",
    "Content Writing", "Photography", "Video Editing",
    "Data Analysis", "DSA", "App Development", "Graphic Design"
]

INTERESTS_OPTIONS = [
    "Technology", "Management", "Cultural", "Sports",
    "Social Impact", "Design", "Literary", "Music", "Dance",
    "Research", "Entrepreneurship", "Photography"
]

# ── Parse saved skills/interests ──
saved_skills = existing["skills"] if existing and existing.get("skills") else []
saved_interests = existing["interests"] if existing and existing.get("interests") else []

# ── Form ──
col1, col2 = st.columns(2)

with col1:
    name = st.text_input(
        "Full Name",
        value=existing["name"] if existing else "",
        placeholder="Your name"
    )
    branch = st.text_input(
        "Branch",
        value=existing["branch"] if existing else "",
        placeholder="e.g. CSE, IT, ECE..."
    )
    hours = st.number_input(
        "Available hours per week for societies",
        min_value=1, max_value=40,
        value=int(existing["hours_per_week"]) if existing and existing.get("hours_per_week") else 5,
        help="Be honest! This helps us suggest realistic combinations."
    )

with col2:
    year = st.selectbox(
        "Year",
        ["1st Year", "2nd Year", "3rd Year", "4th Year"],
        index=["1st Year", "2nd Year", "3rd Year", "4th Year"].index(
            existing["year"]
        ) if existing and existing.get("year") else 0
    )
    selected_skills = st.multiselect(
        "Skills", SKILLS_OPTIONS,
        default=[s for s in saved_skills if s in SKILLS_OPTIONS]
    )
    selected_interests = st.multiselect(
        "Interests", INTERESTS_OPTIONS,
        default=[i for i in saved_interests if i in INTERESTS_OPTIONS]
    )

# ── Extra fields ──
extra_skills = st.text_input(
    "Anything else you're good at?",
    placeholder="e.g. Blender, Public Relations, Robotics..."
)
extra_interests = st.text_input(
    "Any other interests?",
    placeholder="e.g. Astronomy, Finance, Gaming..."
)

linkedin = st.text_input(
    "LinkedIn URL (optional)",
    value=existing["linkedin_url"] if existing and existing.get("linkedin_url") else "",
    placeholder="linkedin.com/in/yourname"
)

if linkedin:
    share_linkedin = st.radio(
        "Comfortable sharing your LinkedIn with other students?",
        ["Yes", "No"],
        index=0 if existing and existing.get("linkedin_share") else 1
    )
else:
    share_linkedin = "No"

st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

# ── Submit ──
if st.button("🔍 Find My Societies", use_container_width=True):
    if not name or not branch or not selected_skills or not selected_interests:
        st.error("Please fill in Name, Branch, Skills and Interests!")
    else:
        all_skills = selected_skills + [
            x.strip() for x in extra_skills.split(",") if x.strip()
        ]
        all_interests = selected_interests + [
            x.strip() for x in extra_interests.split(",") if x.strip()
        ]

        st.session_state["user_name"] = name
        st.session_state["user_profile"] = {
            "name": name,
            "year": year,
            "branch": branch,
            "skills": all_skills,
            "interests": all_interests,
            "hours_per_week": hours
        }

        try:
            supabase.table("profiles").upsert({
                "user_id": st.session_state["user_id"],
                "name": name,
                "year": year,
                "branch": branch,
                "skills": all_skills,
                "interests": all_interests,
                "hours_per_week": int(hours),
                "linkedin_url": linkedin if linkedin else None,
                "linkedin_share": True if share_linkedin == "Yes" else False
            }).execute()
            st.success("Profile saved! Finding your matches...")
            st.switch_page("pages/Recommendation.py")
        except Exception as e:
            st.error(f"Could not save profile: {e}")