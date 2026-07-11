import streamlit as st
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

from supabase_client import supabase
from ai_engine.service import get_society_recommendations

st.set_page_config(
    page_title="Campus Compass | Recommendations",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Custom Styling ──
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
    .stTextInput label, .stNumberInput label,
    .stMultiSelect label, .stSelectbox label,
    .stRadio label {
        color: #C99DA3 !important;
        font-size: 0.85rem !important;
        font-weight: 500 !important;
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
    hr { border-color: #996888 !important; }

    /* Expander (society cards) */
    [data-testid="stExpander"] {
        background: #5E4955 !important;
        border: 1px solid #996888 !important;
        border-radius: 12px !important;
        margin-bottom: 1rem !important;
    }
    [data-testid="stExpander"] summary {
        color: #C6DDF0 !important;
        font-weight: 600 !important;
    }
    [data-testid="stExpander"] p { color: #C6DDF0 !important; }

    /* Detail box inside each society card */
    .detail-box {
        background: #3d2e38;
        border: 1px solid #996888;
        border-radius: 10px;
        padding: 1rem 1.2rem;
        margin-top: 0.5rem;
    }
    .detail-label {
        color: #C99DA3;
        font-size: 0.78rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        margin-top: 0.8rem;
        margin-bottom: 0.2rem;
    }
    .detail-label:first-child { margin-top: 0; }
    .detail-value {
        color: #C6DDF0;
        font-size: 0.9rem;
        line-height: 1.5;
        margin-bottom: 0.3rem;
    }
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
        try:
            supabase.auth.sign_out()
        except:
            pass
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

# ── Fetch complete user profile ──
try:
    result = (
        supabase
        .table("profiles")
        .select("*")
        .eq("user_id", st.session_state["user_id"])
        .single()
        .execute()
    )
    profile = result.data
except Exception as e:
    st.error(f"Could not load profile: {e}")
    st.stop()

# ── Get AI recommendations ──
profile_data = {
    "user_id": profile["user_id"],
    "name": profile["name"],
    "branch": profile["branch"],
    "year": profile["year"],
    "skills": profile["skills"],
    "interests": profile["interests"],
    "hours_per_week": profile["hours_per_week"],
}

recommended_societies = get_society_recommendations(profile_data, limit=None)

all_domains = sorted(set(
    d.strip()
    for s in recommended_societies
    for d in s["domain"].split(",")
))
filter_col, _ = st.columns([1, 3])
with filter_col:
    filter_domain = st.selectbox("Filter by domain", ["All"] + all_domains)

st.markdown("---")

# ── AI recommendations are already sorted ──
sorted_societies = recommended_societies

if filter_domain != "All":
    sorted_societies = [
        s for s in sorted_societies
        if filter_domain.lower() in s["domain"].lower()
    ]

if not sorted_societies:
    st.info("No societies match this filter.")
else:
    for society in sorted_societies:

        def is_empty(value):
            if value is None:
                return True
            text = str(value).strip().lower()
            return text in ("", "n/a", "na", "none", "nan", "null")

        description_missing = is_empty(society.get("description"))
        activities_missing = is_empty(society.get("activities"))

        with st.expander(
            f"{society['society_name']}  —  {society['domain'][:45]}"
            f"{'...' if len(society['domain']) > 45 else ''}  |  "
            f"{round(society['score'])}% match"
        ):
            # Match % — quarter width
            prog_col, _ = st.columns([1, 3])
            with prog_col:
                st.caption("Match Score")
                st.progress(society["score"] / 100)
                st.metric("Match Score", f"{round(society['score'])}%")

            # Detail box — societies whose info hasn't been added to the
            # database yet get a friendly placeholder instead of raw "N/A".
            if description_missing and activities_missing:
                st.markdown(f"""
<div class="detail-box">
    <div class="detail-value">
        We don't have full details for this society yet — check
        their Instagram/website below, or check back soon!
    </div>
</div>
""", unsafe_allow_html=True)
            else:
                st.markdown(f"""
<div class="detail-box">
    <div class="detail-label">About</div>
    <div class="detail-value">
        {society['description'] if not description_missing else "Details coming soon."}
    </div>
    <div class="detail-label">Activities</div>
    <div class="detail-value">
        {society['activities'] if not activities_missing else "Details coming soon."}
    </div>
    <div class="detail-label">Matched Skills</div>
    <div class="detail-value">
        {", ".join(society["matched_skills"]) if society["matched_skills"] else "None"}
    </div>
    <div class="detail-label">Skills to Develop</div>
    <div class="detail-value">
        {", ".join(society["missing_skills"]) if society["missing_skills"] else "None"}
    </div>
    <div class="detail-label">Recommendation Reason</div>
    <div class="detail-value">
        {society["reason"]}
    </div>
</div>
""", unsafe_allow_html=True)

            # Contact links
            st.markdown(
                "<p style='color:#C99DA3; font-size:0.78rem; font-weight:700; "
                "text-transform:uppercase; letter-spacing:0.8px; margin-bottom:0.4rem;'>"
                "Contact</p>",
                unsafe_allow_html=True
            )

            if society.get("instagram"):
                st.markdown(
                    f'<a href="{society["instagram"]}" target="_blank" '
                    f'style="color:#C6DDF0; background:#3d2e38; border:1px solid #996888; '
                    f'border-radius:6px; padding:0.35rem 0.9rem; font-size:0.82rem; '
                    f'text-decoration:none; display:inline-block;">Instagram</a>',
                    unsafe_allow_html=True
                )
            if society.get("website"):
                st.markdown(
                    f'<a href="{society["website"]}" target="_blank" '
                    f'style="color:#C6DDF0; background:#3d2e38; border:1px solid #996888; '
                    f'border-radius:6px; padding:0.35rem 0.9rem; font-size:0.82rem; '
                    f'text-decoration:none; display:inline-block; margin-left:0.5rem;">Website</a>',
                    unsafe_allow_html=True
                )
            if not society.get("instagram") and not society.get("website"):
                st.markdown(
                    '<span style="color:#C99DA3; font-size:0.82rem;">'
                    'No contact links available</span>',
                    unsafe_allow_html=True
                )

            st.markdown("<div style='height:0.8rem'></div>", unsafe_allow_html=True)

             # Buttons
            btn1, btn2 = st.columns(2)

            with btn1:
                if st.button(
                    "Skill Gap Analysis",
                    key=f"gap_{society['society_name']}",
                    use_container_width=True,
                ):
                    st.session_state["selected_society"] = society
                    st.switch_page("pages/SkillGap.py")

            with btn2:
                if st.button(
                    "Save as Interested",
                    key=f"save_{society['society_name']}",
                    use_container_width=True,
                ):
                    try:
                        supabase.table("interested_societies").upsert(
                            {
                                "user_id": st.session_state["user_id"],
                                "society_name": society["society_name"],
                                "match_pct": round(society["score"]),
                            },
                            on_conflict="user_id,society_name",
                        ).execute()

                        st.success("Saved to favourites!")

                    except Exception as e:
                        st.error(f"Insert failed: {e}")