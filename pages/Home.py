import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

st.set_page_config(
    page_title="Home | M1·UI",
    page_icon="🏠",
    layout="wide"
)

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

    /* Metric Cards */
    .metric-card {
        background: linear-gradient(135deg, #7c3aed 0%, #a855f7 100%);
        padding: 1.5rem;
        border-radius: 16px;
        text-align: center;
        color: white;
        transition: all 0.3s ease;
        margin: 0.5rem 0;
    }

    .metric-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(124, 58, 237, 0.3);
    }

    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        margin: 0.5rem 0;
    }

    .metric-label {
        font-size: 0.85rem;
        opacity: 0.9;
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

    /* Activity item */
    .activity-item {
        background: #222222;
        padding: 0.8rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 3px solid #a855f7;
        color: #e0e0e0;
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
    <h1>🏠 Dashboard Home</h1>
    <p>Welcome back! Here's your overview</p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# Key Metrics
st.markdown("### 📊 Key Metrics")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-label">📋 Active Goals</div>
        <div class="metric-value">3</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-label">⭐ Total Points</div>
        <div class="metric-value">1,234</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-label">🔥 Current Streak</div>
        <div class="metric-value">7 days</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Two column layout
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🎯 Quick Actions</div>', unsafe_allow_html=True)

    if st.button("📊 View Tracker", use_container_width=True):
        st.switch_page("pages/tracker.py")

    if st.button("💡 Get Recommendations", use_container_width=True):
        st.switch_page("pages/recommendations.py")

    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🔄 Recent Activity</div>', unsafe_allow_html=True)

    activities = [
        "🎯 Updated 'Complete ML Course' progress",
        "⭐ Earned 50 points for daily tasks",
        "🔥 7 day streak achieved!"
    ]

    for activity in activities:
        st.markdown(f'<div class="activity-item">{activity}</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")

# Tips section
st.markdown("""
<div style="background: #1a1a1a; padding: 1rem; border-radius: 12px; text-align: center; border-left: 3px solid #a855f7;">
    <small style="color: #a0a0a0;">💡 Tip: Visit the Tracker page to update your goals and earn more points!</small>
</div>
""", unsafe_allow_html=True)