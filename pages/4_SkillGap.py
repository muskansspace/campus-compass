import streamlit as st
from supabase_client import get_supabase_client
supabase = get_supabase_client()

st.set_page_config(
    page_title="Campus Compass | Skill Gap",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Custom Styling — matches Recommendation.py / rest of app exactly ──
st.markdown("""
<style>
    .stApp { background: #2A252A; }
    .block-container {
        padding-top: 3rem !important;
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

    /* Same detail-box card used on Recommendation.py */
    .detail-box {
        background: #3d2e38;
        border: 1px solid #996888;
        border-radius: 10px;
        padding: 1rem 1.2rem;
        margin-top: 0.5rem;
        margin-bottom: 1.5rem;
    }
    .detail-label {
        color: #C99DA3;
        font-size: 0.78rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        margin-top: 0.8rem;
        margin-bottom: 0.5rem;
    }
    .detail-label:first-child { margin-top: 0; }
    .detail-value {
        color: #C6DDF0;
        font-size: 0.9rem;
        line-height: 1.5;
        margin-bottom: 0.3rem;
    }

    /* Skill pill tags — matches the multiselect tag style on Home.py */
    .skill-tag {
        display: inline-block;
        border-radius: 20px;
        padding: 0.35rem 0.9rem;
        font-size: 0.82rem;
        font-weight: 500;
        margin: 0.2rem 0.4rem 0.2rem 0;
    }
    .skill-tag.matched {
        background: #4a7a5c;
        color: #eafff0;
    }
    .skill-tag.missing {
        background: #996888;
        color: #ffffff;
    }

    [data-testid="stMetric"] {
        background: #5E4955;
        border: 1px solid #996888;
        border-radius: 12px;
        padding: 1rem;
    }
    [data-testid="stMetricLabel"] { color: #C99DA3 !important; }
    [data-testid="stMetricValue"] { color: #C6DDF0 !important; }
</style>
""", unsafe_allow_html=True)

# ── Auth check ──
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
        except Exception:
            pass
        st.session_state.clear()
        st.switch_page("App.py")

# ── Guard: page requires a society to have been selected on Recommendation.py ──
st.markdown("""
<h1 style="margin-bottom:1.5rem;">🎯 Skill Gap Analysis</h1>
""", unsafe_allow_html=True)

if "selected_society" not in st.session_state:
    st.markdown("""
    <div class="detail-box">
        <div class="detail-value">
            No society selected yet. Go to Recommendations and click
            "Skill Gap Analysis" on a society to see its breakdown here.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)

    if st.button("⬅ Back to Recommendations"):
        st.switch_page("pages/2_Recommendation.py")
    st.stop()

society = st.session_state["selected_society"]

st.markdown(f"""
<p style="color:#C99DA3; font-size:1.05rem; margin-bottom:1.5rem; margin-top:-1rem;">
    {society['society_name']}
</p>
""", unsafe_allow_html=True)

# Match score — same layout as Recommendation.py
prog_col, _ = st.columns([1, 3])
with prog_col:
    st.caption("Match Score")
    st.progress(society["score"] / 100)
    st.metric("Match Score", f"{round(society['score'])}%")

matched_tags = "".join(
    f'<span class="skill-tag matched">{s}</span>'
    for s in society["matched_skills"]
) or '<span style="color:#C99DA3;">None yet</span>'

missing_tags = "".join(
    f'<span class="skill-tag missing">{s}</span>'
    for s in society["missing_skills"]
) or '<span style="color:#C99DA3;">Nothing missing 🎉</span>'

st.markdown(f"""
<div class="detail-box">
    <div class="detail-label">Matched Skills</div>
    <div class="detail-value">{matched_tags}</div>
    <div class="detail-label">Skills to Develop</div>
    <div class="detail-value">{missing_tags}</div>
    <div class="detail-label">Recommendation Reason</div>
    <div class="detail-value">{society["reason"]}</div>
</div>
""", unsafe_allow_html=True)

if st.button("⬅ Back to Recommendations"):
    st.switch_page("pages/2_Recommendation.py")