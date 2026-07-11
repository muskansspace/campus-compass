from dotenv import load_dotenv
from supabase import create_client
import streamlit as st
import os

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")


def get_supabase_client():
    """
    Returns a Supabase client scoped to THIS browser session only.

    CRITICAL FIX: the old version of this file did
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    as a single module-level object. Since Streamlit runs one Python
    process serving every visitor, that object was a SINGLETON shared
    by every user of the deployed app — and supabase-py stores the
    logged-in user's auth session (JWT) as internal state on the
    client object itself. That meant whoever logged in most recently
    became "logged in" for EVERY other visitor too (auth.get_session()
    returns whatever session is currently active on the shared object),
    which is exactly the data leak you saw.

    Each browser session must get its own independent client, stored in
    st.session_state (which IS correctly isolated per browser session
    by Streamlit) instead of as shared module state.
    """

    if "supabase_client" not in st.session_state:
        st.session_state["supabase_client"] = create_client(
            SUPABASE_URL, SUPABASE_KEY
        )

    return st.session_state["supabase_client"]