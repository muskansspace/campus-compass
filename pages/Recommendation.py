import streamlit as st
import random

st.set_page_config(
    page_title="Recommendations | M1·UI",
    page_icon="💡",
    layout="wide"
)

# Initialize session state for recommendations
if 'rec_history' not in st.session_state:
    st.session_state.rec_history = []

# Custom CSS - Dark theme with purple cards
st.markdown("""
<style>
    /* Dark background */
    .stApp {
        background: #0e0e0e;
    }

    /* Main header */
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

    /* Recommendation Cards */
    .rec-card {
        background: linear-gradient(135deg, #7c3aed 0%, #a855f7 100%);
        padding: 1.2rem;
        border-radius: 16px;
        margin: 0.8rem 0;
        color: white;
        transition: all 0.3s ease;
        cursor: pointer;
    }

    .rec-card:hover {
        transform: translateX(5px);
        box-shadow: 0 5px 15px rgba(124, 58, 237, 0.3);
    }

    .rec-title {
        font-size: 1.1rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }

    .rec-category {
        font-size: 0.8rem;
        opacity: 0.9;
        margin-bottom: 0.5rem;
    }

    .rec-match {
        font-size: 0.75rem;
        background: rgba(255,255,255,0.2);
        padding: 0.2rem 0.5rem;
        border-radius: 20px;
        display: inline-block;
    }

    /* Section cards */
    .section-card {
        background: #1a1a1a;
        padding: 1.5rem;
        border-radius: 16px;
        margin: 1rem 0;
        border: 1px solid #2a2a2a;
    }

    .section-title {
        color: #a855f7;
        font-size: 1.2rem;
        font-weight: 600;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    /* Filter section */
    .filter-card {
        background: #222222;
        padding: 1rem;
        border-radius: 12px;
        margin: 0.5rem 0;
    }

    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #7c3aed, #a855f7);
        color: white;
        border: none;
        padding: 0.5rem 1.5rem;
        border-radius: 10px;
        font-weight: 500;
        transition: all 0.3s ease;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(124, 58, 237, 0.4);
    }

    /* Selectbox styling */
    .stSelectbox > div > div {
        background: #222222;
        color: white;
        border-color: #444444;
    }

    /* Remove white space */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 0rem;
    }

    hr {
        border-color: #2a2a2a;
        margin: 1.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>💡 AI Recommendations</h1>
    <p>Personalized suggestions based on your interests</p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# Filters section
col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    st.markdown('<div class="filter-card">', unsafe_allow_html=True)
    category = st.selectbox(
        "📂 Category",
        ["All", "Learning", "Productivity", "Health", "Career", "Lifestyle"]
    )
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="filter-card">', unsafe_allow_html=True)
    confidence = st.slider("🎯 Minimum Match %", 50, 100, 70)
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="filter-card">', unsafe_allow_html=True)
    if st.button("🔄 Refresh Recommendations", use_container_width=True):
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")

# Main content
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📌 Top Picks For You</div>', unsafe_allow_html=True)

    # Recommendation data
    recommendations = {
        "Learning": {"title": "Advanced Python Course", "description": "Master Python with hands-on projects",
                     "match": 94},
        "Productivity": {"title": "Time Management Masterclass", "description": "Boost productivity by 200%",
                         "match": 88},
        "Health": {"title": "Daily Meditation Guide", "description": "15-min mindfulness routine", "match": 82},
        "Career": {"title": "Portfolio Building Workshop", "description": "Stand out to employers", "match": 76},
        "Lifestyle": {"title": "Work-Life Balance Tips", "description": "Achieve harmony in daily life", "match": 71}
    }

    # Display filtered recommendations
    shown = 0
    for rec_cat, rec_data in recommendations.items():
        if (category == "All" or category == rec_cat) and rec_data['match'] >= confidence:
            st.markdown(f"""
            <div class="rec-card">
                <div class="rec-title">{rec_data['title']}</div>
                <div class="rec-category">{rec_cat}</div>
                <div class="rec-match">🔍 {rec_data['match']}% match</div>
                <div style="margin-top: 0.5rem; font-size: 0.9rem;">{rec_data['description']}</div>
            </div>
            """, unsafe_allow_html=True)
            shown += 1

    if shown == 0:
        st.info("No recommendations match your filters. Try adjusting the category or match percentage!")

    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📊 Recommendation Stats</div>', unsafe_allow_html=True)

    st.markdown("""
    <div style="text-align: center; padding: 1rem;">
        <div style="font-size: 2rem; color: #a855f7;">5</div>
        <div style="color: #a0a0a0;">Available Picks</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    st.markdown('<div class="section-title">💡 Pro Tips</div>', unsafe_allow_html=True)

    tips = [
        "✨ Lower match % for more recommendations",
        "🎯 Higher match % for better quality",
        "🔄 Refresh to see new suggestions",
        "📊 Check back daily for updated picks"
    ]

    for tip in tips:
        st.markdown(f'<div style="color: #a0a0a0; margin: 0.5rem 0;">• {tip}</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")

# Footer
st.markdown("""
<div style="background: #1a1a1a; padding: 1rem; border-radius: 12px; text-align: center; border-left: 3px solid #a855f7;">
    <small style="color: #a0a0a0;">💡 Tip: Adjust filters to find the perfect recommendations for your goals!</small>
</div>
""", unsafe_allow_html=True)