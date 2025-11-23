# app/pages/dashboard.py
import streamlit as st
from config import THEME
from utils.api_client import get

def dashboard_page():
    """Beautiful role-based dashboard"""
    user = st.session_state.get("auth", {}).get("user", {"name": "Demo", "role": "Professor"})
    name = user.get("name", "User")
    role = user.get("role", "Professor")
    
    # Welcome section with animation
    st.markdown(f"""
    <div class="card card-elevated fade-in" style="padding: 24px; background: linear-gradient(135deg, {THEME['primary']}15 0%, {THEME['accent']}15 100%); margin-bottom: 24px;">
        <div style="display: flex; align-items: center; justify-content: space-between;">
            <div>
                <h1 style="margin: 0; color: {THEME['primary']}; font-size: 32px;">👋 Welcome back, {name}!</h1>
                <p style="margin: 8px 0 0 0; color: {THEME['muted']}; font-size: 16px;">
                    📍 Role: <strong>{role}</strong> | Ready to create amazing assessments
                </p>
            </div>
            <div style="font-size: 48px;">✨</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Key metrics section
    st.markdown('<h2 style="color: #1E293B; margin-bottom: 16px;">📊 Dashboard Overview</h2>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="card" style="text-align: center; padding: 24px;">
            <div style="font-size: 32px; margin-bottom: 8px;">📄</div>
            <p style="color: {THEME['muted']}; font-size: 13px; margin: 0 0 8px 0;">DOCUMENTS</p>
            <h3 style="color: {THEME['primary']}; margin: 0; font-size: 28px;">12</h3>
            <p style="color: {THEME['muted']}; font-size: 12px; margin: 8px 0 0 0;">Processed</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="card" style="text-align: center; padding: 24px;">
            <div style="font-size: 32px; margin-bottom: 8px;">❓</div>
            <p style="color: {THEME['muted']}; font-size: 13px; margin: 0 0 8px 0;">QUESTIONS</p>
            <h3 style="color: {THEME['accent']}; margin: 0; font-size: 28px;">123</h3>
            <p style="color: {THEME['muted']}; font-size: 12px; margin: 8px 0 0 0;">Generated</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="card" style="text-align: center; padding: 24px;">
            <div style="font-size: 32px; margin-bottom: 8px;">⏳</div>
            <p style="color: {THEME['muted']}; font-size: 13px; margin: 0 0 8px 0;">PENDING</p>
            <h3 style="color: {THEME['warning']}; margin: 0; font-size: 28px;">4</h3>
            <p style="color: {THEME['muted']}; font-size: 12px; margin: 8px 0 0 0;">Reviews</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Recent activity
    st.markdown('<h2 style="color: #1E293B; margin-bottom: 16px;">📋 Recent Activity</h2>', unsafe_allow_html=True)
    
    docs = get("list_docs")
    doc_list = docs.get("docs", [
        {"name": "Sample Document 1", "status": "✅ Processed", "date": "2024-11-21"},
        {"name": "Sample Document 2", "status": "⏳ Processing", "date": "2024-11-20"},
        {"name": "Sample Document 3", "status": "✅ Processed", "date": "2024-11-19"},
    ])
    
    for doc in doc_list:
        st.markdown(f"""
        <div class="card" style="padding: 16px; margin-bottom: 12px; display: flex; justify-content: space-between; align-items: center;">
            <div>
                <p style="margin: 0; font-weight: 600; color: {THEME['text']};">📄 {doc.get('name', 'Document')}</p>
                <p style="margin: 4px 0 0 0; font-size: 12px; color: {THEME['muted']};\">{doc.get('date', 'N/A')}</p>
            </div>
            <div style="color: {THEME['success']}; font-weight: 600; font-size: 14px;\">{doc.get('status', '⏳')}</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Quick actions
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<h2 style="color: #1E293B; margin-bottom: 16px;">⚡ Quick Actions</h2>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📤 Upload Document", use_container_width=True):
            st.session_state.page = "Upload"
            st.rerun()
    with col2:
        if st.button("✨ Generate Questions", use_container_width=True):
            st.session_state.page = "Generation"
            st.rerun()
    with col3:
        if st.button("🔍 Review Items", use_container_width=True):
            st.session_state.page = "Review"
            st.rerun()
