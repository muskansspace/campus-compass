import streamlit as st
from supabase_client import supabase
from analytics import burnout_calculator, best_combinations, get_burnout_advice

st.set_page_config(
    page_title="Campus Compass | Favourites",
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

    /* Society row */
    .society-row {
        background: #5E4955;
        border: 1px solid #996888;
        border-radius: 12px;
        padding: 0.9rem 1.2rem;
        margin-bottom: 0.6rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    .society-row-name {
        color: #C6DDF0;
        font-size: 0.95rem;
        font-weight: 600;
    }
    .society-row-domain {
        color: #C99DA3;
        font-size: 0.78rem;
        margin-top: 0.15rem;
    }
    .society-row-match {
        color: #81C784;
        font-size: 0.85rem;
        font-weight: 600;
        white-space: nowrap;
    }

    /* Section card */
    .section-card {
        background: #5E4955;
        border: 1px solid #996888;
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1.2rem;
    }
    .section-title {
        color: #C6DDF0;
        font-size: 1rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.6px;
        margin-bottom: 1rem;
    }

    /* Burnout status */
    .burnout-value {
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 0.2rem;
    }
    .burnout-advice {
        color: #C99DA3;
        font-size: 0.88rem;
        line-height: 1.5;
        margin-top: 0.5rem;
    }

    /* Combo card */
    .combo-card {
        background: #3d2e38;
        border-radius: 10px;
        padding: 1rem 1.2rem;
        margin-bottom: 0.6rem;
    }
    .combo-title {
        color: #C6DDF0;
        font-size: 0.9rem;
        font-weight: 600;
        margin-bottom: 0.3rem;
    }
    .combo-detail {
        color: #C99DA3;
        font-size: 0.82rem;
        line-height: 1.5;
    }

    /* Buttons */
    .stButton > button {
        background: #7a4f6d !important;
        color: #ffffff !important;
        border: 1px solid #996888 !important;
        border-radius: 8px !important;
        font-weight: 500 !important;
        font-size: 0.85rem !important;
        transition: all 0.2s !important;
    }
    .stButton > button:hover {
        background: #996888 !important;
        color: #ffffff !important;
    }

    /* Progress bar */
    [data-testid="stProgress"] > div {
        background: #1a1414 !important;
        border-radius: 10px !important;
        height: 8px !important;
    }
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #4CAF50, #81C784) !important;
        border-radius: 10px !important;
        height: 8px !important;
    }

    hr { border-color: #996888 !important; margin: 1.2rem 0 !important; }
</style>
""", unsafe_allow_html=True)

# ── Auth check ──
if not st.session_state.get("logged_in"):
    st.switch_page("App.py")

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

# ── Header ──
st.markdown("""
<h1 style="color:#C6DDF0; margin-bottom:0.2rem;">Favourites</h1>
<p style="color:#C99DA3; margin-bottom:1.5rem; font-size:0.95rem;">
    Societies you are interested in.
</p>
""", unsafe_allow_html=True)

# ── Get saved societies ──
saved = st.session_state.get("saved_societies", [])

# ── Empty state ──
if not saved:
    st.markdown("""
    <div style="
        background: #5E4955;
        border: 1px solid #996888;
        border-radius: 16px;
        padding: 2.5rem;
        text-align: center;
    ">
        <p style="color:#C6DDF0; font-size:1rem; font-weight:600; margin-bottom:0.5rem;">
            No societies saved yet
        </p>
        <p style="color:#C99DA3; font-size:0.88rem; margin-bottom:1.2rem;">
            Explore recommendations and save societies you are interested in.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height:0.8rem'></div>", unsafe_allow_html=True)

    if st.button("Go to Recommendations", use_container_width=False):
        st.switch_page("pages/Recommendation.py")

else:
    # ── Saved societies list ──
    st.markdown('<div class="section-title" style="color:#C99DA3; font-size:0.78rem; font-weight:700; text-transform:uppercase; letter-spacing:0.8px; margin-bottom:0.8rem;">Saved Societies</div>', unsafe_allow_html=True)

    for i, society in enumerate(saved):
        col1, col2, col3 = st.columns([3, 1, 0.6])

        with col1:
            st.markdown(f"""
            <div>
                <div class="society-row-name">{society['name']}</div>
                <div class="society-row-domain">{society['domain']}</div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div style="padding-top:0.4rem;">
                <span class="society-row-match">{society['match_pct']}% match</span>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            if st.button("Remove", key=f"remove_{i}"):
                st.session_state["saved_societies"].pop(i)
                st.rerun()

        st.markdown("<hr style='border-color:#3d2e38; margin:0.3rem 0;'>", unsafe_allow_html=True)

    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

    # ── Get user available hours ──
    available_hrs = None
    try:
        result = supabase.table("profiles").select("hours_per_week").eq(
            "user_id", st.session_state["user_id"]
        ).execute()
        if result.data:
            available_hrs = int(result.data[0]["hours_per_week"])
    except:
        pass

    if not available_hrs:
        st.warning("Please complete your profile with available hours to see burnout analysis.")
        if st.button("Go to Home"):
            st.switch_page("pages/Home.py")
    else:
        # ── Burnout Calculator ──
        st.markdown("""
        <div class="section-card">
            <div class="section-title">Burnout Analysis</div>
        """, unsafe_allow_html=True)

        burnout_pct, status = burnout_calculator(saved, available_hrs)
        advice = get_burnout_advice(burnout_pct, None)

        # Color based on status
        if burnout_pct <= 80:
            color = "#81C784"
        elif burnout_pct <= 100:
            color = "#FFD54F"
        elif burnout_pct <= 130:
            color = "#FFB74D"
        else:
            color = "#E57373"

        col_b1, col_b2 = st.columns([1, 2])
        with col_b1:
            st.markdown(f"""
            <div style="text-align:center; padding:1rem;">
                <div class="burnout-value" style="color:{color};">{burnout_pct}%</div>
                <div style="color:{color}; font-size:0.88rem; font-weight:600;">{status}</div>
            </div>
            """, unsafe_allow_html=True)

        with col_b2:
            st.markdown(f"""
            <div class="burnout-advice">{advice}</div>
            <div style="margin-top:0.8rem;">
                <div style="color:#C99DA3; font-size:0.78rem; margin-bottom:0.3rem;">
                    {sum(s['commitment_per_week'] for s in saved)} hrs/week selected 
                    out of your {available_hrs} hrs/week available
                </div>
            </div>
            """, unsafe_allow_html=True)
            prog_col, _ = st.columns([2, 1])
            with prog_col:
                st.progress(min(burnout_pct / 100, 1.0))

        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)

        # ── Best Combination ──
        st.markdown("""
        <div class="section-card">
            <div class="section-title">Best Combination Suggestion</div>
        """, unsafe_allow_html=True)

        combos, error = best_combinations(saved, available_hrs)

        if error:
            st.markdown(f"""
            <p style="color:#C99DA3; font-size:0.88rem;">{error}</p>
            """, unsafe_allow_html=True)
        else:
            medals = ["1", "2", "3"]
            for idx, combo in enumerate(combos):
                names = [s['name'] for s in combo['societies']]
                total = combo['total_hrs']
                avg_match = round(combo['avg_match'], 1)
                domains = list(set(s['domain'].split(",")[0].strip() for s in combo['societies']))

                st.markdown(f"""
                <div class="combo-card">
                    <div class="combo-title">Option {medals[idx]}: {" + ".join(names)}</div>
                    <div class="combo-detail">
                        {total} hrs/week &nbsp;·&nbsp; {avg_match}% avg match &nbsp;·&nbsp; {", ".join(domains)}
                    </div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)