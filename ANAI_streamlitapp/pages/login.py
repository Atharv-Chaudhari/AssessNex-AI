# app/pages/login.py
import streamlit as st
from utils.api_client import post
from config import THEME

def login_page():
    """Beautiful login page with modern design"""
    st.markdown(f"""
    <div class="card card-elevated" style="padding: 24px;">
        <div style="text-align: center; margin-bottom: 24px;">
            <h2 style="color: {THEME['primary']}; margin-bottom: 8px;">🔐 Sign In</h2>
            <p style="color: {THEME['muted']}; font-size: 14px;">Welcome back to AssessNex AI</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("login_form", clear_on_submit=False):
        # Form fields with better styling
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input(
                "👤 Full Name",
                placeholder="Enter your full name",
                key="login_name"
            )
        with col2:
            email = st.text_input(
                "📧 Email Address",
                placeholder="your@email.com",
                key="login_email"
            )
        
        role = st.selectbox(
            "👥 Select Your Role",
            ["Professor", "Assistant", "Student"],
            help="Choose your role in the system"
        )
        
        # Submit button
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            submitted = st.form_submit_button(
                "✨ Sign In",
                use_container_width=True,
                type="primary"
            )
        
        if submitted:
            if not name or not email:
                st.error("❌ Please fill in all fields")
            else:
                payload = {
                    "name": name,
                    "email": email,
                    "role": role
                }
                resp = post("auth_login", data=payload)
                st.session_state["auth"] = {
                    "token": resp.get("token"),
                    "user": resp.get("user")
                }
                st.success("✅ Successfully logged in! Redirecting...")
                st.balloons()
                import time
                time.sleep(1)
                st.rerun()
