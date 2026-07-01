import streamlit as st
from supabase_client import supabase
from societies_data import SOCIETIES

st.set_page_config(
    page_title="Campus Compass | Recommendations",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="expanded"
)

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

    /* Expander */
    [data-testid="stExpander"] {
        background: #5E4955 !important;
        border: 1px solid #996888 !important;
        border-radius: 16px !important;
        margin-bottom: 0.8rem !important;
    }
    [data-testid="stExpander"]:hover {
        border-color: #C99DA3 !important;
    }
    [data-testid="stExpander"] summary {
        color: #C6DDF0 !important;
        font-weight: 500 !important;
        font-size: 0.95rem !important;
    }
    [data-testid="stExpander"] summary p,
    [data-testid="stExpander"] summary span {
        color: #C6DDF0 !important;
    }
    /* Fix dim text when expanded */
    [data-testid="stExpander"] div {
        color: #C6DDF0 !important;
    }

    /* Detail section */
    .detail-box {
        background: #3d2e38;
        border-radius: 12px;
        padding: 1.2rem 1.4rem;
        margin-top: 0.8rem;
        margin-bottom: 0.8rem;
    }
    .detail-label {
        color: #C99DA3;
        font-size: 0.72rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        margin-bottom: 0.25rem;
        margin-top: 0.8rem;
    }
    .detail-label:first-child { margin-top: 0; }
    .detail-value {
        color: #C6DDF0;
        font-size: 0.88rem;
        line-height: 1.55;
        margin-bottom: 0;
    }

    /* Progress bar */
    .stProgress > div > div > div {
    background: linear-gradient(90deg, #4CAF50, #81C784) !important;
    border-radius: 10px !important;
    height: 8px !important;
}
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #4CAF50, #81C784) !important;
        border-radius: 10px !important;
    }

    /* Buttons */
    .stButton > button {
        border-radius: 8px !important;
        font-weight: 500 !important;
        font-size: 0.85rem !important;
        padding: 0.5rem 1rem !important;
        transition: all 0.2s !important;
        border: none !important;
        background: #996888 !important;
        color: #ffffff !important;
    }
    .stButton > button:hover {
        background: #C99DA3 !important;
        color: #2A252A !important;
    }

    /* Filter selectbox */
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
    }
    .stSelectbox label {
        color: #C99DA3 !important;
        font-size: 0.85rem !important;
    }

    hr { border-color: #996888 !important; margin: 1.2rem 0 !important; }
            
</style>
""", unsafe_allow_html=True)

# ── Auth check ──
if not st.session_state.get("logged_in"):
    st.switch_page("App.py")

# ── Fetch name if missing ──
if not st.session_state.get("user_name"):
    try:
        result = supabase.table("profiles").select("name").eq(
            "user_id", st.session_state["user_id"]
        ).execute()
        if result.data:
            st.session_state["user_name"] = result.data[0]["name"]
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
        st.switch_page("App.py")

# ── Header ──
name_display = st.session_state.get("user_name", "there")
st.markdown(f"""
<h1 style="color:#C6DDF0; margin-bottom:0.2rem;">
    Recommendations for {name_display}
</h1>
<p style="color:#C99DA3; margin-bottom:1.5rem; font-size:0.95rem;">
    Societies ranked by match with your profile. Click any card to explore more.
</p>
""", unsafe_allow_html=True)

# ── Filter ──
all_domains = sorted(set(
    d.strip()
    for s in SOCIETIES
    for d in s["domain"].split(",")
))
filter_col, _ = st.columns([1, 3])
with filter_col:
    filter_domain = st.selectbox("Filter by domain", ["All"] + all_domains)

st.markdown("---")

# ── Sort + filter ──
sorted_societies = sorted(SOCIETIES, key=lambda x: x["match_pct"], reverse=True)
if filter_domain != "All":
    sorted_societies = [
        s for s in sorted_societies
        if filter_domain.lower() in s["domain"].lower()
    ]

if not sorted_societies:
    st.info("No societies match this filter.")
else:
    for society in sorted_societies:
        with st.expander(
            f"{society['name']}  —  {society['domain'][:45]}{'...' if len(society['domain']) > 45 else ''}  |  {society['match_pct']}% match"
        ):
            # Match % — quarter width
            prog_col, _ = st.columns([1, 3])
            with prog_col:
                st.caption("Match Score")
                st.progress(society["match_pct"] / 100)

            # Detail box
            st.markdown(f"""
<div class="detail-box">
    <div class="detail-label">About</div>
    <div class="detail-value">{society['description']}</div>
    <div class="detail-label">Activities</div>
    <div class="detail-value">{society['activities']}</div>
    <div class="detail-label">Skills Preferred</div>
    <div class="detail-value">{society['skills_required']}</div>
    <div class="detail-label">Commitment</div>
    <div class="detail-value">{society['commitment_text']}  &nbsp;·&nbsp;  Recruitment: {society['recruitment_month']}</div>
</div>
""", unsafe_allow_html=True)

            # Contact links
            st.markdown("<p style='color:#C99DA3; font-size:0.78rem; font-weight:700; text-transform:uppercase; letter-spacing:0.8px; margin-bottom:0.4rem;'>Contact</p>", unsafe_allow_html=True)

            if society.get("instagram"):
                st.markdown(
                    f'<a href="{society["instagram"]}" target="_blank" style="color:#C6DDF0; background:#3d2e38; border:1px solid #996888; border-radius:6px; padding:0.35rem 0.9rem; font-size:0.82rem; text-decoration:none; display:inline-block;">Instagram</a>',
                    unsafe_allow_html=True
                )
            if society.get("website"):
                st.markdown(
                    f'<a href="{society["website"]}" target="_blank" style="color:#C6DDF0; background:#3d2e38; border:1px solid #996888; border-radius:6px; padding:0.35rem 0.9rem; font-size:0.82rem; text-decoration:none; display:inline-block; margin-left:0.5rem;">Website</a>',
                    unsafe_allow_html=True
                )
            if not society.get("instagram") and not society.get("website"):
                st.markdown(
                    '<span style="color:#C99DA3; font-size:0.82rem;">No contact links available</span>',
                    unsafe_allow_html=True
                )

            st.markdown("<div style='height:0.8rem'></div>", unsafe_allow_html=True)

            # Buttons
            btn1, btn2 = st.columns(2)
            with btn1:
                if st.button(
                    "Skill Gap Analysis",
                    key=f"gap_{society['name']}",
                    use_container_width=True
                ):
                    st.session_state["selected_society"] = society
                    st.switch_page("pages/SkillGap.py")

            with btn2:
                if st.button(
                    "Save as Interested",
                    key=f"save_{society['name']}",
                    use_container_width=True
                ):
                    if "saved_societies" not in st.session_state:
                        st.session_state["saved_societies"] = []
                    if society["name"] not in [
                        s["name"] for s in st.session_state["saved_societies"]
                    ]:
                        st.session_state["saved_societies"].append(society)
                        st.success(f"{society['name']} saved to favourites!")
                    else:
                        st.info("Already in your favourites!")