
import streamlit as st

from supabase_client import supabase

st.title("Campus Compass Login")

email = st.text_input("Email")
password = st.text_input("Password", type="password")

if st.button("Sign Up"):
    try:
        response = supabase.auth.sign_up(
            {
                "email": email.strip(),
                "password": password
            }
        )

        st.success("Signup successful!")
        st.write(response)

    except Exception as e:
        st.error(f"Signup failed: {e}")

if st.button("Login"):
    try:
        response = supabase.auth.sign_in_with_password(
            {
                "email": email.strip(),
                "password": password
            }
        )

        st.session_state["logged_in"] = True
        st.session_state["user_id"] = response.user.id
        st.session_state["email"] = response.user.email

        st.success("Login successful!")

    except Exception as e:
        st.error(f"Login failed: {e}")

if st.session_state.get("logged_in"):
    st.success(f"Logged in as {st.session_state['email']}")

if st.session_state.get("logged_in"):
    if st.button("Logout"):
        st.session_state.clear()
        st.rerun()
        
st.set_page_config(
    page_title="Campus Compass| Smart Dashboard",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS - Dark theme with purple cards (matching tracker.py)
st.markdown("""
<style>
    /* Dark background */
    .stApp {
        background: #0e0e0e;
    }

    /* Main container */
    .main-header {
        text-align: center;
        margin-bottom: 2rem;
    }

    .main-header h1 {
        color: #e0e0e0;
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
    }

    .main-header p {
        color: #a0a0a0;
        font-size: 1rem;
    }

    /* Purple/Lavender Cards */
    .feature-card {
        background: linear-gradient(135deg, #7c3aed 0%, #a855f7 100%);
        padding: 1.5rem;
        border-radius: 16px;
        text-align: center;
        color: white;
        transition: all 0.3s ease;
        margin: 0.5rem 0;
        cursor: pointer;
        min-height: 180px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }

    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(124, 58, 237, 0.3);
    }

    .feature-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
    }

    .feature-title {
        font-size: 1.3rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }

    .feature-desc {
        font-size: 0.85rem;
        opacity: 0.9;
    }

    /* Stats card */
    .stats-card {
        background: #1a1a1a;
        padding: 1.5rem;
        border-radius: 16px;
        margin: 1rem 0;
        border: 1px solid #2a2a2a;
        text-align: center;
    }

    .stats-number {
        font-size: 2rem;
        font-weight: bold;
        color: #a855f7;
    }

    .stats-label {
        color: #a0a0a0;
        font-size: 0.9rem;
        margin-top: 0.5rem;
    }

    /* Divider */
    hr {
        border-color: #2a2a2a;
        margin: 1.5rem 0;
    }

    /* Remove white space */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 0rem;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>🎯Campus Compass</h1>
    <p>Your smart companion for goals, recommendations, and progress tracking</p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# Quick Stats
st.markdown("### 📊 Platform Overview")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="stats-card">
        <div class="stats-number">3</div>
        <div class="stats-label">Smart Pages</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="stats-card">
        <div class="stats-number">24/7</div>
        <div class="stats-label">AI Powered</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="stats-card">
        <div class="stats-number">100%</div>
        <div class="stats-label">Free to Use</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="stats-card">
        <div class="stats-number">Real-time</div>
        <div class="stats-label">Updates</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Feature Cards
st.markdown("### 🚀 Explore Features")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-card" onclick="window.location.href='/Home'">
        <div class="feature-icon">🏠</div>
        <div class="feature-title">Home</div>
        <div class="feature-desc">Dashboard overview and quick insights</div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Go to Home", key="home_btn", use_container_width=True):
        st.switch_page("pages/Home.py")

with col2:
    st.markdown("""
    <div class="feature-card" onclick="window.location.href='/Recommendation'">
        <div class="feature-icon">💡</div>
        <div class="feature-title">Recommendations</div>
        <div class="feature-desc">Personalized AI-powered suggestions</div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Get Recommendations", key="rec_btn", use_container_width=True):
        st.switch_page("pages/Recommendation.py")

with col3:
    st.markdown("""
    <div class="feature-card" onclick="window.location.href='/Tracker'">
        <div class="feature-icon">📊</div>
        <div class="feature-title">Tracker</div>
        <div class="feature-desc">Monitor goals and achievements</div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Track Progress", key="track_btn", use_container_width=True):
        st.switch_page("pages/Tracker.py")

st.markdown("---")

# Quick tip
st.markdown("""
<div style="background: #1a1a1a; padding: 1rem; border-radius: 12px; text-align: center; border-left: 3px solid #a855f7;">
    <small style="color: #a0a0a0;">💡 Pro tip: Use the sidebar to navigate between pages or click on any feature card above!</small>
</div>
""", unsafe_allow_html=True)

