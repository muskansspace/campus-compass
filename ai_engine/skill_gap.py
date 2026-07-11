import streamlit as st
from supabase_client import supabase

st.set_page_config(
    page_title="Campus Compass | Skill Gap",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Custom Styling (matches rest of app) ──
st.markdown("""
<style>
    .stApp { background: #2A252A; }
    .block-container {
        padding-top: 2rem !important;
        max-width: 860px !important;
        margin: 0 auto !important;
    }
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
    p, span, label, div { color: #C6DDF0; }
    hr { border-color: #996888 !important; }
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
    [data-testid="stMetric"] {
        background: #5E4955;
        border: 1px solid #996888;
        border-radius: 12px;
        padding: 1rem;
    }
    [data-testid="stMetricLabel"] { color: #C99DA3 !important; }
    [data-testid="stMetricValue"] { color: #C6DDF0 !important; }
    .stAlert { border-radius: 10px !important; }
</style>
""", unsafe_allow_html=True)

# ── Auth check (was missing — anyone could land here unauthenticated) ──
if not st.session_state.get("logged_in"):
    st.switch_page("App.py")

# ── Sidebar (same nav as rest of app) ──
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
        try:
            supabase.auth.sign_out()
        except:
            pass
        st.session_state.clear()
        st.switch_page("App.py")

# ── Guard: page requires a society to have been selected on Recommendation.py ──
if "selected_society" not in st.session_state:
    st.error("No society selected. Go back to Recommendations first.")
    if st.button("⬅ Back to Recommendations"):
        st.switch_page("pages/Recommendation.py")
    st.stop()

society = st.session_state["selected_society"]

st.title("🎯 Skill Gap Analysis")
st.subheader(society["society_name"])

st.metric("Match Score", f"{round(society['score'])}%")

st.divider()

st.subheader("Matched Skills")
if society["matched_skills"]:
    for skill in society["matched_skills"]:
        st.success(skill)
else:
    st.info("No matched skills")

st.divider()

st.subheader("Skills To Develop")
if society["missing_skills"]:
    for skill in society["missing_skills"]:
        st.warning(skill)
else:
    st.success("No missing skills")

st.divider()

st.subheader("Recommendation")
st.write(society["reason"])

if st.button("⬅ Back"):
    st.switch_page("pages/Recommendation.py")