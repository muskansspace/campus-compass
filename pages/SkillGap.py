import streamlit as st

st.set_page_config(
    page_title="Skill Gap Analysis",
    page_icon="🎯",
    layout="wide"
)

if "selected_society" not in st.session_state:
    st.error("No society selected.")
    st.stop()

society = st.session_state["selected_society"]

st.title("🎯 Skill Gap Analysis")

st.subheader(society["society_name"])

st.metric(
    "Match Score",
    f"{round(society['score'])}%"
)

st.divider()

st.subheader("Matched Skills")

if society["matched_skills"]:
    for skill in society["matched_skills"]:
        st.success(skill)
else:
    st.info("No matched skills")

st.divider()

st.subheader("Skills To Develop")

if society["missing_skills"]:
    for skill in society["missing_skills"]:
        st.warning(skill)
else:
    st.success("No missing skills")

st.divider()

st.subheader("Recommendation")

st.write(society["reason"])

if st.button("⬅ Back"):
    st.switch_page("pages/Recommendation.py")