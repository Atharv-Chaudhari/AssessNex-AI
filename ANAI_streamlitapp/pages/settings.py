# app/pages/settings.py
import streamlit as st
from config import THEME
from utils.api_client import post, get

def settings_page():
    """Beautiful settings and profile page"""
    user = st.session_state.get("auth", {}).get("user", {"name": "Demo", "email": "demo@example.com", "role": "Professor"})
    
    # Header
    st.markdown(f"""
    <div class="card card-elevated fade-in" style="padding: 20px; background: linear-gradient(135deg, {THEME['primary']}15 0%, {THEME['accent']}15 100%); margin-bottom: 24px;">
        <h1 style="margin: 0; color: {THEME['primary']}; font-size: 28px;">⚙️ Settings & Profile</h1>
        <p style="margin: 8px 0 0 0; color: {THEME['muted']}; font-size: 14px;">Manage your account and preferences</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Tabs
    tab1, tab2, tab3 = st.tabs(["👤 Profile", "🔔 Notifications", "📧 Emails"])
    
    with tab1:
        st.markdown(f'<h3 style="color: {THEME["text"]}; margin-bottom: 16px;">Account Information</h3>', unsafe_allow_html=True)
        
        with st.form("profile_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                name = st.text_input(
                    "👤 Full Name",
                    value=user.get("name", ""),
                    help="Your full name"
                )
            
            with col2:
                email = st.text_input(
                    "📧 Email Address",
                    value=user.get("email", ""),
                    help="Your email address"
                )
            
            role = st.selectbox(
                "👥 Role",
                ["Professor", "Assistant", "Student"],
                index=["Professor", "Assistant", "Student"].index(user.get("role", "Professor")),
                disabled=True,
                help="Your role in the system"
            )
            
            col1, col2, col3 = st.columns([1, 1, 1])
            with col2:
                submitted = st.form_submit_button("💾 Save Changes", use_container_width=True, type="primary")
            
            if submitted:
                st.session_state["auth"]["user"]["name"] = name
                st.session_state["auth"]["user"]["email"] = email
                st.success("✅ Profile updated successfully!")
    
    with tab2:
        st.markdown(f'<h3 style="color: {THEME["text"]}; margin-bottom: 16px;">Notification Preferences</h3>', unsafe_allow_html=True)
        
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown("📧 **Email Notifications**", unsafe_allow_html=True)
        with col2:
            email_notif = st.toggle("Enable", value=True)
        
        st.markdown("---")
        
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown("⏰ **Question Generation Alerts**", unsafe_allow_html=True)
        with col2:
            gen_notif = st.toggle("Enable ", value=True)
        
        st.markdown("---")
        
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown("✅ **Review Reminders**", unsafe_allow_html=True)
        with col2:
            review_notif = st.toggle("Enable  ", value=False)
        
        st.markdown("---")
        
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown("📊 **Analytics Summary**", unsafe_allow_html=True)
        with col2:
            analytics_notif = st.toggle("Enable   ", value=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("💾 Save Preferences", use_container_width=True, type="primary"):
            st.success("✅ Notification preferences saved!")
    
    with tab3:
        st.markdown(f'<h3 style="color: {THEME["text"]}; margin-bottom: 16px;">Send Email</h3>', unsafe_allow_html=True)
        
        with st.form("email_form"):
            to = st.text_input(
                "📧 To Email",
                value="colleague@example.com",
                placeholder="recipient@email.com"
            )
            
            subject = st.text_input(
                "📝 Subject",
                value="Invitation to AssessNex AI",
                placeholder="Email subject"
            )
            
            message = st.text_area(
                "💬 Message",
                value="You've been invited to join AssessNex AI - the AI-powered assessment platform!",
                height=120,
                placeholder="Your message here..."
            )
            
            col1, col2, col3 = st.columns([1, 1, 1])
            with col2:
                submitted = st.form_submit_button("✉️ Send Email", use_container_width=True, type="primary")
            
            if submitted:
                resp = post("notify", data={
                    "to": to,
                    "subject": subject,
                    "message": message
                })
                if resp.get("success"):
                    st.success("✅ Email sent successfully!")
                    st.balloons()
                else:
                    st.error("❌ Failed to send email")
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(f'<h3 style="color: {THEME["text"]}; margin-bottom: 16px;">📬 Sent Emails</h3>', unsafe_allow_html=True)
        
        emails = get("list_emails").get("emails", [
            {"to": "prof@example.com", "subject": "Assignment Review", "date": "2024-11-20"},
            {"to": "student@example.com", "subject": "Exam Scheduled", "date": "2024-11-18"},
        ])
        
        if emails:
            for email in reversed(emails):
                st.markdown(f"""
                <div class="card" style="padding: 12px; margin-bottom: 8px;">
                    <p style="margin: 0; font-weight: 600; color: {THEME['text']}; font-size: 14px;">✉️ {email.get('subject', 'No subject')}</p>
                    <p style="margin: 4px 0 0 0; font-size: 12px; color: {THEME['muted']};">
                        To: <strong>{email.get('to', 'Unknown')}</strong> | {email.get('date', 'Unknown date')}
                    </p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("📭 No emails sent yet")
