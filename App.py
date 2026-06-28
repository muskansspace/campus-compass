import streamlit as st
from supabase_client import supabase

st.set_page_config(
    page_title="Campus Compass",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# App.py mein sabse upar add karo — set_page_config ke baad
if not st.session_state.get("logged_in"):
    try:
        session = supabase.auth.get_session()
        if session and session.user:
            st.session_state["logged_in"] = True
            st.session_state["user_id"] = session.user.id
            st.session_state["email"] = session.user.email
    except:
        pass

st.markdown("""
<style>
    .stApp { background: #2A252A; }
    [data-testid="collapsedControl"] { display: none; }
    .block-container {
        padding-top: 5vh !important;
        padding-bottom: 0 !important;
    }

    /* The center column gets card styling */
    [data-testid="column"]:nth-child(2) {
        background: #5E4955 !important;
        border: 1px solid #996888 !important;
        border-radius: 24px !important;
        padding: 2rem 1.5rem 2rem 1.5rem !important;
    }

    /* Input labels */
    .stTextInput label {
        color: #C99DA3 !important;
        font-size: 0.83rem !important;
        font-weight: 500 !important;
    }

    /* Input fields */
    .stTextInput > div > div > input {
        background: #3d2e38 !important;
        color: #C6DDF0 !important;
        border: 1px solid #996888 !important;
        border-radius: 8px !important;
    }
    .stTextInput > div > div > input::placeholder {
        color: #7a6670 !important;
    }
    .stTextInput > div > div > input:focus {
        border-color: #C99DA3 !important;
        box-shadow: 0 0 0 2px rgba(201,157,163,0.2) !important;
    }

    /* All buttons base */
    .stButton > button {
        border-radius: 8px !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        padding: 0.6rem !important;
        width: 100% !important;
        transition: all 0.2s !important;
    }

    /* Sign Up — first button */
    .stButton:nth-of-type(1) > button {
        background: #996888 !important;
        color: #ffffff !important;
        border: none !important;
    }
    .stButton:nth-of-type(1) > button:hover {
        background: #C99DA3 !important;
        color: #2A252A !important;
    }

    /* Login — second button */
    .stButton:nth-of-type(2) > button {
        background: transparent !important;
        color: #C6DDF0 !important;
        border: 1px solid #996888 !important;
    }
    .stButton:nth-of-type(2) > button:hover {
        border-color: #C99DA3 !important;
        color: #C99DA3 !important;
    }
    .stTextInput > div > div > input,
.stTextInput > div > div > input:focus {
    background-color: #3d2e38 !important;
    color: #C6DDF0 !important;
    caret-color: #C6DDF0 !important;
    -webkit-text-fill-color: #C6DDF0 !important;
    opacity: 1 !important;
}
</style>
""", unsafe_allow_html=True)

if st.session_state.get("logged_in"):
    st.switch_page("pages/Home.py")

left, center, right = st.columns([1, 1.2, 1])

with center:
    # Logo + title inside card
    st.markdown("""
    <div style="text-align:center; padding: 1rem 0 1.5rem 0;">
        <div style="font-size:2.8rem">🧭</div>
        <h1 style="color:#C6DDF0; font-size:1.8rem; margin:0.3rem 0; font-weight:700;">
            Campus Compass
        </h1>
        <p style="color:#C99DA3; font-size:0.85rem; margin:0.2rem 0 0 0;">
            Your AI-powered society discovery platform for IGDTUW
        </p>
    </div>
    <hr style="border:none; border-top:1px solid #996888; margin-bottom:1.5rem;">
    """, unsafe_allow_html=True)

    email = st.text_input("Email", placeholder="you@gmail.com")
    password = st.text_input("Password", type="password", placeholder="••••••••")

    st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)

    col_a, col_b = st.columns(2)

    with col_a:
        if st.button("Sign Up", use_container_width=True):
            if email and password:
                try:
                    supabase.auth.sign_up({
                        "email": email.strip(),
                        "password": password
                    })
                    st.success("Account created! Please login.")
                except Exception as e:
                    st.error(f"Signup failed: {e}")
            else:
                st.error("Please fill all fields.")

    with col_b:
        if st.button("Login", use_container_width=True):
            if email and password:
                try:
                    response = supabase.auth.sign_in_with_password({
                        "email": email.strip(),
                        "password": password
                    })
                    st.session_state["logged_in"] = True
                    st.session_state["user_id"] = response.user.id
                    st.session_state["email"] = response.user.email
                    st.rerun()
                except Exception as e:
                    st.error(f"Login failed: {e}")
            else:
                st.error("Please fill all fields.")