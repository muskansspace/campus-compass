import streamlit as st
from supabase_client import supabase

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

# ── Societies data ──
SOCIETIES = [
    {
        "name": "TechNeeds",
        "domain": "AI/ML, DSA, Web Dev, UI/UX",
        "description": "Active technical society organizing tech events and workshops throughout the year.",
        "activities": "InnoVortex Hackathon, SSSC Summer Cohort, 21 Days of Code, workshops",
        "skills_required": "Enthusiasm to learn and contribute consistently",
        "commitment_per_week": 6,
        "commitment_text": "2-10 hrs (varies by event)",
        "recruitment_month": "August (sometimes June/July)",
        "instagram": "https://www.instagram.com/techneeds_igdtuw_/",
        "website": None,
        "match_pct": 85
    },
    {
        "name": "AssetMerkle",
        "domain": "Web3, Blockchain, Decentralized Tech",
        "description": "IGDTUW's only Web3/blockchain society focused on awareness and community building.",
        "activities": "AM Hacks (flagship hackathon), Web3 Week, Community Meetups",
        "skills_required": "Basic coding, Event management, Communication, Canva/design",
        "commitment_per_week": 2,
        "commitment_text": "~2 hrs/week avg (more during events)",
        "recruitment_month": "End of August (1st & 2nd year)",
        "instagram": "https://www.instagram.com/assetmerkle.igdtuw/",
        "website": None,
        "match_pct": 72
    },
    {
        "name": "IEEE IGDTUW",
        "domain": "Electrical, Electronics, CS, AI, Blockchain, AR/VR",
        "description": "Aligns with IEEE WIE global network; promotes women in engineering and STEM.",
        "activities": "Speaker sessions, hands-on workshops on AR/VR, 3D printing, drone making",
        "skills_required": "Interest in technical research, hardware, emerging tech (AR/VR)",
        "commitment_per_week": 5,
        "commitment_text": "High during flagship weeks; none during exams",
        "recruitment_month": "August-September",
        "instagram": "https://www.instagram.com/ieeeigdtuw/",
        "website": None,
        "match_pct": 90
    },
    {
        "name": "Nirvana",
        "domain": "UI/UX Design, Graphic Design",
        "description": "Design club focused on design thinking before students transition into development.",
        "activities": "Cohorts, hackathons, workshops, quizzes, design showcases",
        "skills_required": "Basic Canva proficiency, colour theory, curiosity to learn",
        "commitment_per_week": 4.5,
        "commitment_text": "~4-5 hrs/week during cohorts",
        "recruitment_month": "Induction period",
        "instagram": "https://www.instagram.com/designclubigdtuw/",
        "website": None,
        "match_pct": 78
    },
    {
        "name": "Tarannum",
        "domain": "Music - Indian Classical, Western, Rock Band, PR & Media",
        "description": "Musical society with 3 performance teams and PR and Media team.",
        "activities": "Riyaz sessions, Garba Night, Halloween events, flash mobs, inter-college competitions",
        "skills_required": "Passion for music; good voice/instrument skills; PR/Media skills",
        "commitment_per_week": 12,
        "commitment_text": "Varies — regular riyaz + increased during events",
        "recruitment_month": "August",
        "instagram": "https://www.instagram.com/tarannum.igdtuw/",
        "website": None,
        "match_pct": 60
    },
    {
        "name": "Rahnuma",
        "domain": "Dramatics, Theatre, Street Play, Public Speaking",
        "description": "Dramatics society that teaches life lessons through theatre and street plays.",
        "activities": "Aaghaz Street Play, Bachpan-e-Karvaan (Children's Day event)",
        "skills_required": "Eagerness to learn; no prior acting experience required",
        "commitment_per_week": 3,
        "commitment_text": "2-3 hrs/day (alternating timings)",
        "recruitment_month": "Mid August - Early September",
        "instagram": "https://www.instagram.com/rahnuma_igdtuw/",
        "website": None,
        "match_pct": 55
    },
    {
        "name": "Hypnotics",
        "domain": "Dance, Choreography, Cultural Events",
        "description": "Official dance society of IGDTUW — platform for dance skill-building and competitions.",
        "activities": "Dance workshops, inter-college competitions, cultural fest performances",
        "skills_required": "Passion for dance, dedication, teamwork, creativity",
        "commitment_per_week": 9,
        "commitment_text": "6-12 hrs/week",
        "recruitment_month": "August-September",
        "instagram": "https://www.instagram.com/hypnotics_igdtuw/",
        "website": None,
        "match_pct": 50
    },
    {
        "name": "Finivesta",
        "domain": "Finance, Economics, Financial Literacy, Stock Markets",
        "description": "Women-led finance and economics society promoting financial literacy through events.",
        "activities": "Payload, Bidding Blitz, Finopoly, Money Masterclass, FinWeek",
        "skills_required": "Basic finance and economics understanding; enthusiasm, proactiveness",
        "commitment_per_week": 2.5,
        "commitment_text": "2-3 hrs/week",
        "recruitment_month": "Late September - Early October",
        "instagram": "https://www.instagram.com/finivesta_igdtuw/",
        "website": None,
        "match_pct": 65
    },
    {
        "name": "MSC IGDTUW",
        "domain": "Tech Education, AI/DS, Skill Development, Networking",
        "description": "Microsoft Learn Student Ambassador chapter empowering women technologists.",
        "activities": "Hackathons, webinars, Summer Bootcamp, Networking Nights, Microsoft office sessions",
        "skills_required": "Passion for tech, interest in leadership and community building",
        "commitment_per_week": 2,
        "commitment_text": "1-2 hrs/week",
        "recruitment_month": "June (1st years)",
        "instagram": "https://www.instagram.com/msc.igdtuw/",
        "website": None,
        "match_pct": 88
    },
    {
        "name": "SOCH",
        "domain": "Art, Writing, Management, PR & Marketing",
        "description": "Art and writing society providing a creative platform for expression and storytelling.",
        "activities": "Art and writing competitions, slam poetry, creative workshops",
        "skills_required": "Sketching, graphic design, creative writing, poetry, event management",
        "commitment_per_week": 3,
        "commitment_text": "2-4 hrs/week",
        "recruitment_month": "Beginning of academic session",
        "instagram": None,
        "website": None,
        "match_pct": 62
    },
    {
        "name": "B.H.A.V",
        "domain": "Public Speaking, Debate, MUN, Creative Writing",
        "description": "Creative society focused on public speaking and literary exposure.",
        "activities": "Aarohan (annual lit fest), IGDTUMUN, mock Youth Parliaments",
        "skills_required": "Basic Hindi and English, awareness of current topics",
        "commitment_per_week": 2,
        "commitment_text": "Monthly/event-based",
        "recruitment_month": "August-October",
        "instagram": None,
        "website": None,
        "match_pct": 58
    },
    {
        "name": "ACM Student Chapter",
        "domain": "Competitive Programming, ML/AI, Data Science, Open Source",
        "description": "One of IGDTUW's oldest technical societies; fosters learning in tech and innovation.",
        "activities": "ACM Research Internship, workshops, bootcamps, hackathons, open-source initiatives",
        "skills_required": "Enthusiasm to learn; teamwork; basic domain knowledge preferred",
        "commitment_per_week": 3,
        "commitment_text": "2-3 hrs/week (reduced during exams)",
        "recruitment_month": "August-September",
        "instagram": "https://www.instagram.com/acm_igdtuw/",
        "website": None,
        "match_pct": 92
    },
    {
        "name": "Rotaract Club",
        "domain": "Community Service, Women Empowerment, Mental Health",
        "description": "Student-led organization for community service, leadership, and global networking.",
        "activities": "Dear Zindagi (mental health fest), blood donation camps, NGO outreach",
        "skills_required": "Communication, leadership, event planning; no prior experience needed",
        "commitment_per_week": 2,
        "commitment_text": "Flexible/volunteer-based",
        "recruitment_month": "August-September",
        "instagram": None,
        "website": None,
        "match_pct": 70
    },
    {
        "name": "SWE IGDTUW",
        "domain": "Technical Workshops, Leadership, Industry Networking",
        "description": "Student chapter of Society of Women Engineers empowering women in engineering.",
        "activities": "Workshops, bootcamps, expert talks, mentorship programs, hackathons",
        "skills_required": "Teamwork, communication, interest in tech and leadership",
        "commitment_per_week": 4,
        "commitment_text": "Regular: 2-4 hrs/week; Core: 4-8 hrs/week",
        "recruitment_month": "August-September",
        "instagram": None,
        "website": None,
        "match_pct": 80
    },
    {
        "name": "ASME IGDTUW",
        "domain": "AI & Computer Vision, CAD, Robotics, Embedded Systems",
        "description": "Student-led technical society focused on hands-on learning and industry exposure.",
        "activities": "Technical workshops, expert talks, industry sessions, project-based learning",
        "skills_required": "Curiosity and willingness to learn; prior experience is a plus",
        "commitment_per_week": 3.5,
        "commitment_text": "2-5 hrs/week (more during events)",
        "recruitment_month": "August-September",
        "instagram": None,
        "website": None,
        "match_pct": 75
    },
    {
        "name": "CodeBenders",
        "domain": "DSA, Competitive Programming, Open Source, Career Prep",
        "description": "Technical society dedicated to building a strong tech community through mentorship.",
        "activities": "DSA Bootcamps, Open Source Week, resume building, pre-placement prep",
        "skills_required": "Basic programming; Figma/Canva for design; communication for sponsorship",
        "commitment_per_week": 4,
        "commitment_text": "3-5 hrs/week (more during events)",
        "recruitment_month": "September-October",
        "instagram": None,
        "website": None,
        "match_pct": 87
    },
    {
        "name": "E-Cell",
        "domain": "Entrepreneurship, Innovation, Startup Awareness, Leadership",
        "description": "Student-led entrepreneurship cell fostering innovation and startup culture.",
        "activities": "Founder talks, expert workshops, ideathons, case study competitions",
        "skills_required": "Communication, teamwork, leadership, problem-solving, organizational skills",
        "commitment_per_week": 13.5,
        "commitment_text": "12-15 hrs/week (highest commitment)",
        "recruitment_month": "August-September",
        "instagram": None,
        "website": None,
        "match_pct": 68
    },
    {
        "name": "Enactus",
        "domain": "Social Entrepreneurship, Community Development, Sustainability",
        "description": "Social entrepreneurship society building scalable solutions for real-world challenges.",
        "activities": "Enactova (National Business Plan Competition), Innovation Fair, community outreach",
        "skills_required": "Communication, teamwork, problem-solving, creativity, research skills",
        "commitment_per_week": 4,
        "commitment_text": "3-5 hrs/week (more during major events)",
        "recruitment_month": "August-September",
        "instagram": None,
        "website": None,
        "match_pct": 73
    },
]

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
                    existing = supabase.table("interested_societies").select("id").eq(
                        "user_id", st.session_state["user_id"]
                    ).eq("society_name", society["name"]).execute()

                    if existing.data:
                        st.info("Already in your favourites!")
                    else:
                        supabase.table("interested_societies").insert({
                            "user_id": st.session_state["user_id"],
                            "society_name": society["name"],
                            "match_pct": society["match_pct"],
                            "commitment_per_week": society["commitment_per_week"]
                        }).execute()

                        if "saved_societies" not in st.session_state:
                            st.session_state["saved_societies"] = []
                        st.session_state["saved_societies"].append(society)

                        st.success(f"{society['name']} saved to favourites!")