# app/pages/register.py
import streamlit as st
from utils.api_client import post
from config import THEME

def register_page():
    """Beautiful registration page with modern design"""
    st.markdown(f"""
    <div class="card card-elevated" style="padding: 24px;">
        <div style="text-align: center; margin-bottom: 24px;">
            <h2 style="color: {THEME['accent']}; margin-bottom: 8px;">📝 Create Account</h2>
            <p style="color: {THEME['muted']}; font-size: 14px;">Join AssessNex AI today</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("reg_form", clear_on_submit=False):
        # Form fields
        name = st.text_input(
            "👤 Full Name",
            placeholder="Enter your full name",
            key="reg_name"
        )
        
        email = st.text_input(
            "📧 Email Address",
            placeholder="your@email.com",
            key="reg_email"
        )
        
        role = st.selectbox(
            "👥 Select Your Role",
            ["Professor", "Assistant", "Student"],
            help="Choose your role in the system",
            key="reg_role"
        )
        
        # Submit button
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            submitted = st.form_submit_button(
                "🚀 Create Account",
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
                resp = post("auth_register", data=payload)
                st.success("✅ Account created successfully! Please login.")
                st.info("💡 Tip: Use the same email and role to sign in on the left side.")
