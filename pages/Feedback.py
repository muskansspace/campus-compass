import streamlit as st
from supabase_client import supabase

st.set_page_config(
    page_title="Campus Compass | Feedback",
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
    hr { border-color: #996888 !important; }

    .stTextArea label {
        color: #C99DA3 !important;
        font-size: 0.85rem !important;
        font-weight: 500 !important;
    }
    .stTextArea > div > div > textarea {
        background: #3d2e38 !important;
        color: #C6DDF0 !important;
        caret-color: #C6DDF0 !important;
        border: 1px solid #996888 !important;
        border-radius: 10px !important;
        font-size: 0.92rem !important;
        line-height: 1.6 !important;
    }
    .stTextArea > div > div > textarea::placeholder {
        color: #7a6670 !important;
    }
    .stTextArea > div > div > textarea:focus {
        border-color: #C99DA3 !important;
        box-shadow: 0 0 0 2px rgba(201,157,163,0.2) !important;
    }

    /* Star buttons — completely hidden visually, star shown via markdown above */
    div[data-testid="stMainBlockContainer"] [data-testid="stButton"] button {
        background: #996888 !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        padding: 0.65rem 1.5rem !important;
        width: 100% !important;
        transition: all 0.2s !important;
    }
    div[data-testid="stMainBlockContainer"] [data-testid="stButton"] button:hover {
        background: #C99DA3 !important;
        color: #2A252A !important;
    }

    /* Hide star click buttons completely — only emoji shows */
    .star-click-btn button {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        color: transparent !important;
        font-size: 0 !important;
        padding: 0 !important;
        height: 0px !important;
        min-height: 0 !important;
        width: 100% !important;
        cursor: pointer !important;
        margin-top: -0.3rem !important;
    }
    .star-click-btn button:hover {
        background: transparent !important;
    }

    .section-label {
        color: #C99DA3;
        font-size: 0.85rem;
        font-weight: 500;
        margin-bottom: 0.4rem;
    }
    .rating-hint {
        text-align: center;
        font-size: 0.88rem;
        font-weight: 600;
        letter-spacing: 0.03em;
        margin: 0.4rem 0 1.2rem 0;
        min-height: 1.3rem;
    }
    .success-box {
        background: #3d4a3d;
        border: 1px solid #5a8a5a;
        border-radius: 16px;
        padding: 2.5rem 2rem;
        text-align: center;
        max-width: 480px;
        margin: 4rem auto;
    }
    .success-box h2 { color: #a8d5a8 !important; margin-bottom: 0.5rem; }
    .success-box p { color: #C99DA3; font-size: 0.95rem; margin: 0; }
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
        try:
            supabase.auth.sign_out()
        except:
            pass
        st.session_state.clear()
        st.switch_page("App.py")

# ── Success screen ──
if st.session_state.get("feedback_submitted"):
    st.session_state.pop("feedback_submitted")
    st.markdown("""
    <div class="success-box">
        <div style="font-size:2.8rem; margin-bottom:0.8rem">✅</div>
        <h2>Thank you!</h2>
        <p>Your feedback helps us make Campus Compass better for every IGDTUW student.</p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# ── Page header ──
st.markdown("""
<h1 style="color:#C6DDF0; margin-bottom:0.2rem;">Share Your Feedback</h1>
<p style="color:#C99DA3; margin-bottom:2rem; font-size:0.95rem;">
    Honest input from you helps us improve — take 2 minutes.
</p>
""", unsafe_allow_html=True)

# ── State ──
if "fb_rating" not in st.session_state:
    st.session_state["fb_rating"] = 0

STAR_LABELS = {0: "", 1: "😞 Poor", 2: "😐 Fair", 3: "🙂 Good", 4: "😊 Great", 5: "🤩 Excellent!"}
STAR_COLORS = {0: "", 1: "#e05c5c", 2: "#d4956a", 3: "#d4c46a", 4: "#96c96a", 5: "#6ac96a"}

_, center, _ = st.columns([1, 2, 1])

with center:

    # ── Stars ──
    st.markdown('<p class="section-label" style="text-align:center;">How would you rate Campus Compass overall?</p>', unsafe_allow_html=True)

    # Row 1: just the big star icons
    star_cols = st.columns(5)
    for i, col in enumerate(star_cols, start=1):
        with col:
            icon = "★" if i <= st.session_state["fb_rating"] else "☆"
            color = "#F4C430" if i <= st.session_state["fb_rating"] else "#5a4555"
            st.markdown(
                f'<div style="text-align:center; font-size:2.8rem; color:{color}; line-height:1; margin-bottom:0.1rem;">{icon}</div>',
                unsafe_allow_html=True
            )

    # Row 2: invisible click buttons directly below stars
    btn_cols = st.columns(5)
    for i, col in enumerate(btn_cols, start=1):
        with col:
            st.markdown('<div class="star-click-btn">', unsafe_allow_html=True)
            if st.button(f"{i}", key=f"star_{i}", use_container_width=True):
                st.session_state["fb_rating"] = i
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

    # ── Rating label ──
    hint = STAR_LABELS[st.session_state["fb_rating"]]
    hint_color = STAR_COLORS[st.session_state["fb_rating"]]
    st.markdown(
        f'<p class="rating-hint" style="color:{hint_color if hint else "transparent"};">{hint or "·"}</p>',
        unsafe_allow_html=True
    )

    # ── Text feedback ──
    st.markdown('<p class="section-label">Tell us more</p>', unsafe_allow_html=True)
    feedback_text = st.text_area(
        label="Tell us more",
        placeholder="What did you like? What felt off? Any society we missed? Any feature you'd love to see?",
        height=220,
        max_chars=1000,
        label_visibility="collapsed"
    )

    char_count = len(feedback_text)
    st.markdown(
        f'<p style="text-align:right; color:#7a6670; font-size:0.75rem; margin-top:-0.4rem;">{char_count}/1000</p>',
        unsafe_allow_html=True
    )

    st.markdown("<div style='height:0.6rem'></div>", unsafe_allow_html=True)

    # ── Submit ──
    if st.button("Submit Feedback", use_container_width=True):
        if st.session_state["fb_rating"] == 0:
            st.error("Please give a star rating before submitting.")
        elif not feedback_text.strip():
            st.error("Please write something in the feedback box.")
        else:
            try:
                supabase.table("feedback").insert({
                    "user_id": st.session_state["user_id"],
                    "feedback_text": feedback_text.strip(),
                    "rating": st.session_state["fb_rating"]
                }).execute()

                st.session_state["fb_rating"] = 0
                st.session_state["feedback_submitted"] = True
                st.rerun()

            except Exception as e:
                st.error(f"Could not submit feedback: {e}")