import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

st.set_page_config(
    page_title="Tracker | M1·UI",
    page_icon="📊",
    layout="wide"
)

# Initialize session state for tracking data
if 'tasks' not in st.session_state:
    st.session_state.tasks = []
if 'goals' not in st.session_state:
    st.session_state.goals = [
        {"name": "Complete ML Course", "progress": 75, "target": 100},
        {"name": "Read 12 Books", "progress": 5, "target": 12},
        {"name": "Exercise Routine", "progress": 18, "target": 30},
    ]
if 'points' not in st.session_state:
    st.session_state.points = 1234
if 'streak' not in st.session_state:
    st.session_state.streak = 7

# Custom CSS - Dark theme with purple cards
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
    .metric-card {
        background: linear-gradient(135deg, #7c3aed 0%, #a855f7 100%);
        padding: 1.5rem;
        border-radius: 16px;
        text-align: center;
        color: white;
        transition: all 0.3s ease;
        margin: 0.5rem 0;
        cursor: pointer;
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
        margin-bottom: 0.5rem;
    }

    .metric-delta {
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

    /* Goal items */
    .goal-item {
        background: #222222;
        padding: 1rem;
        border-radius: 12px;
        margin: 0.5rem 0;
        border-left: 3px solid #a855f7;
    }

    /* Progress bar */
    .progress-bar-bg {
        background: #333333;
        border-radius: 10px;
        overflow: hidden;
        margin: 0.5rem 0;
    }

    .progress-bar-fill {
        background: linear-gradient(90deg, #7c3aed, #a855f7);
        padding: 0.4rem;
        text-align: center;
        color: white;
        font-size: 0.8rem;
        border-radius: 10px;
        transition: width 0.3s ease;
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

    /* Input fields */
    .stTextInput > div > div > input, .stSelectbox > div > div {
        background: #222222;
        color: white;
        border-color: #444444;
    }

    /* Success message */
    .stSuccess {
        background: #1a3a2a;
        color: #00ff88;
    }

    /* Remove unnecessary white space */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 0rem;
    }

    /* Divider */
    hr {
        border-color: #2a2a2a;
        margin: 1.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>📊 Progress Tracker</h1>
    <p>Track your goals, tasks, and achievements</p>
</div>
""", unsafe_allow_html=True)

# Date selector
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    date_range = st.selectbox(
        "📅 View Period",
        ["Today", "This Week", "This Month", "All Time"],
        key="period"
    )

st.markdown("---")

# Main KPIs - Functional cards
st.markdown("### 🎯 Key Metrics")

col1, col2, col3 = st.columns(3)

with col1:
    points_delta = st.session_state.points - 1234
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">⭐ Total Points</div>
        <div class="metric-value">{st.session_state.points}</div>
        <div class="metric-delta">+{points_delta} this month</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    streak_delta = "+3 days" if st.session_state.streak > 7 else "+0 days"
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">🔥 Current Streak</div>
        <div class="metric-value">{st.session_state.streak} days</div>
        <div class="metric-delta">{streak_delta}</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    completion_rate = 78
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">✅ Completion Rate</div>
        <div class="metric-value">{completion_rate}%</div>
        <div class="metric-delta">↑ 12% this month</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Functional Goals Section
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">🎯 Active Goals</div>', unsafe_allow_html=True)

# Display and update goals
for idx, goal in enumerate(st.session_state.goals):
    col1, col2, col3 = st.columns([2, 2, 1])

    with col1:
        st.markdown(f"**{goal['name']}**")

    with col2:
        progress_percent = (goal['progress'] / goal['target']) * 100
        st.markdown(f"""
        <div class="progress-bar-bg">
            <div class="progress-bar-fill" style="width: {progress_percent}%;">
                {goal['progress']}/{goal['target']}
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        # Update progress button
        if st.button(f"➕", key=f"update_{idx}"):
            if goal['progress'] < goal['target']:
                goal['progress'] += 1
                st.session_state.points += 10
                st.session_state.streak = min(st.session_state.streak + 1, 30)
                st.rerun()

# Add new goal
with st.expander("➕ Add New Goal", expanded=False):
    col1, col2 = st.columns(2)
    with col1:
        new_goal_name = st.text_input("Goal Name", placeholder="e.g., Learn Python")
    with col2:
        new_goal_target = st.number_input("Target", min_value=1, value=10)

    if st.button("Create Goal", use_container_width=True):
        if new_goal_name:
            st.session_state.goals.append({
                "name": new_goal_name,
                "progress": 0,
                "target": new_goal_target
            })
            st.success(f"✅ Goal '{new_goal_name}' created!")
            st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

# Weekly Progress Chart (Using Streamlit's native chart)
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">📈 Weekly Progress</div>', unsafe_allow_html=True)

# Generate sample progress data
days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
weekly_data = np.random.randint(40, 90, 7)

chart_data = pd.DataFrame({
    'Day': days,
    'Progress': weekly_data
})

st.bar_chart(chart_data.set_index('Day'), use_container_width=True)
st.caption("💡 Complete tasks daily to improve your progress")

st.markdown('</div>', unsafe_allow_html=True)

# Quick Task Section (Functional)
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">✅ Quick Tasks</div>', unsafe_allow_html=True)

# Today's tasks
tasks_today = [
    {"task": "Review daily goals", "completed": False, "points": 5},
    {"task": "Update progress tracker", "completed": False, "points": 10},
    {"task": "Share achievements", "completed": False, "points": 15}
]

for idx, task in enumerate(tasks_today):
    col1, col2, col3 = st.columns([3, 1, 1])
    with col1:
        st.write(f"📌 {task['task']}")
    with col2:
        st.write(f"+{task['points']} pts")
    with col3:
        if st.button(f"Complete", key=f"task_{idx}"):
            st.session_state.points += task['points']
            st.success(f"✅ Completed! +{task['points']} points")
            st.balloons()
            st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

# Recent Activity (Functional)
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">🔄 Recent Activity</div>', unsafe_allow_html=True)

activities = [
    f"🎯 Updated 'Complete ML Course' progress",
    f"⭐ Earned 50 points for daily tasks",
    f"🔥 {st.session_state.streak} day streak achieved!"
]

for activity in activities:
    st.markdown(f"• {activity}")

st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #888; padding: 1rem;">
    ✨ Complete tasks to earn points and maintain your streak!
</div>
""", unsafe_allow_html=True)