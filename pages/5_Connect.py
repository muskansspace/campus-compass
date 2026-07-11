import streamlit as st
from supabase_client import supabase

st.set_page_config(
    page_title="Campus Compass | Connect",
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

    /* Society section heading */
    .society-heading {
        color: #C99DA3;
        font-size: 0.78rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        margin: 1.5rem 0 0.8rem 0;
    }
    .society-heading:first-of-type { margin-top: 0; }

    /* Peer card */
    .peer-card {
        background: #5E4955;
        border: 1px solid #996888;
        border-radius: 12px;
        padding: 0.9rem 1.2rem;
        margin-bottom: 0.6rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    .peer-name {
        color: #C6DDF0;
        font-size: 0.95rem;
        font-weight: 600;
    }
    .peer-meta {
        color: #C99DA3;
        font-size: 0.78rem;
        margin-top: 0.15rem;
    }

    /* Connect link button */
    .connect-btn {
        background: #996888;
        color: #ffffff !important;
        border-radius: 8px;
        padding: 0.4rem 1rem;
        font-size: 0.82rem;
        font-weight: 500;
        text-decoration: none;
        white-space: nowrap;
        transition: all 0.2s;
    }
    .connect-btn:hover {
        background: #C99DA3;
        color: #2A252A !important;
    }

    /* Empty per-society state */
    .no-peers {
        color: #7a6670;
        font-size: 0.85rem;
        font-style: italic;
        padding: 0.6rem 0 1rem 0;
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

    hr { border-color: #996888 !important; margin: 1.2rem 0 !important; }
</style>
""", unsafe_allow_html=True)

# ── Auth check ──
if not st.session_state.get("logged_in"):
    st.switch_page("App.py")

user_id = st.session_state["user_id"]

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
        except Exception:
            pass
        st.session_state.clear()
        st.switch_page("App.py")

# ── Header ──
st.markdown("""
<h1 style="color:#C6DDF0; margin-bottom:0.2rem;">Connect</h1>
<p style="color:#C99DA3; margin-bottom:1.5rem; font-size:0.95rem;">
    People interested in the same societies as you.
</p>
""", unsafe_allow_html=True)

# ── Step 1: current user's interested societies ──
my_society_names = []
try:
    result = supabase.table("interested_societies").select("society_name").eq(
        "user_id", user_id
    ).execute()
    my_society_names = [r["society_name"] for r in result.data] if result.data else []
except:
    my_society_names = []

# ── Empty state: user hasn't saved any societies yet ──
if not my_society_names:
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
            Save societies you're interested in to see who else is interested too.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height:0.8rem'></div>", unsafe_allow_html=True)

    if st.button("Go to Recommendations", use_container_width=False):
        st.switch_page("pages/2_Recommendation.py")

else:
    # ── Step 2: everyone else interested in the same societies ──
    other_rows = []
    try:
        result = supabase.table("interested_societies").select("user_id, society_name").in_(
            "society_name", my_society_names
        ).neq("user_id", user_id).execute()
        other_rows = result.data if result.data else []
    except:
        other_rows = []

    other_user_ids = list(set(r["user_id"] for r in other_rows))

    # ── Step 3: profiles for those users, only linkedin_share = true ──
    profiles_by_id = {}
    if other_user_ids:
        try:
            result = supabase.table("profiles").select(
                "user_id, name, branch, year, linkedin_url, linkedin_share"
            ).in_("user_id", other_user_ids).eq("linkedin_share", True).execute()
            if result.data:
                profiles_by_id = {p["user_id"]: p for p in result.data}
        except:
            profiles_by_id = {}

    # ── Step 4: group peers by society ──
    peers_by_society = {name: [] for name in my_society_names}
    for row in other_rows:
        profile = profiles_by_id.get(row["user_id"])
        if profile:
            peers_by_society[row["society_name"]].append(profile)

    total_peers = sum(len(v) for v in peers_by_society.values())

    # ── Overall empty state: saved societies but literally no one to connect with ──
    if total_peers == 0:
        st.markdown("""
        <div style="
            background: #5E4955;
            border: 1px solid #996888;
            border-radius: 16px;
            padding: 2.5rem;
            text-align: center;
        ">
            <p style="color:#C6DDF0; font-size:1rem; font-weight:600; margin-bottom:0.5rem;">
                No one to connect with yet
            </p>
            <p style="color:#C99DA3; font-size:0.88rem; margin:0;">
                No one else interested in your saved societies has opted to share their LinkedIn yet.
                Check back later as more students join!
            </p>
        </div>
        """, unsafe_allow_html=True)
    else:
        for society_name in my_society_names:
            peers = peers_by_society.get(society_name, [])

            st.markdown(f'<div class="society-heading">{society_name}</div>', unsafe_allow_html=True)

            if not peers:
                st.markdown('<div class="no-peers">No one to connect with here yet.</div>', unsafe_allow_html=True)
                continue

            for peer in peers:
                name = peer.get("name", "Someone")
                branch = peer.get("branch", "")
                year = peer.get("year", "")
                linkedin_url = peer.get("linkedin_url", "")

                meta_parts = [p for p in [branch, year] if p]
                meta_text = " · ".join(meta_parts)

                st.markdown(f"""
                <div class="peer-card">
                    <div>
                        <div class="peer-name">{name}</div>
                        <div class="peer-meta">{meta_text}</div>
                    </div>
                    <a href="{linkedin_url}" target="_blank" class="connect-btn">Connect</a>
                </div>
                """, unsafe_allow_html=True)