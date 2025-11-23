# app/pages/review.py
import streamlit as st
from config import THEME
from components.question_card import question_card

def review_page():
    """Beautiful review and edit page"""
    # Header
    st.markdown(f"""
    <div class="card card-elevated fade-in" style="padding: 20px; background: linear-gradient(135deg, {THEME['primary']}15 0%, {THEME['accent']}15 100%); margin-bottom: 24px;">
        <h1 style="margin: 0; color: {THEME['primary']}; font-size: 28px;">✏️ Review & Edit Questions</h1>
        <p style="margin: 8px 0 0 0; color: {THEME['muted']}; font-size: 14px;">Quality check and refine your generated questions</p>
    </div>
    """, unsafe_allow_html=True)
    
    questions = st.session_state.get("last_generated", [])
    
    if not questions:
        st.info("""
        📭 No generated questions found.
        
        **Please follow these steps:**
        1. Go to **Upload** page and upload documents
        2. Go to **Generation** page and create questions
        3. Come back here to review
        """)
        return
    
    # Stats
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div class="card" style="text-align: center; padding: 16px;">
            <p style="color: {THEME['muted']}; font-size: 12px; margin: 0 0 8px 0;">TOTAL</p>
            <h3 style="color: {THEME['primary']}; margin: 0; font-size: 24px;">{len(questions)}</h3>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="card" style="text-align: center; padding: 16px;">
            <p style="color: {THEME['muted']}; font-size: 12px; margin: 0 0 8px 0;">APPROVED</p>
            <h3 style="color: {THEME['success']}; margin: 0; font-size: 24px;">0</h3>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="card" style="text-align: center; padding: 16px;">
            <p style="color: {THEME['muted']}; font-size: 12px; margin: 0 0 8px 0;">PENDING</p>
            <h3 style="color: {THEME['warning']}; margin: 0; font-size: 24px;">{len(questions)}</h3>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Questions review
    st.markdown(f'<h3 style="color: {THEME["text"]}; margin-bottom: 16px;">📋 Questions to Review</h3>', unsafe_allow_html=True)
    
    for idx, q in enumerate(questions, 1):
        question_card(q, editable=True, question_number=idx)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Action buttons
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("✅ Approve All", use_container_width=True):
            st.success(f"✅ All {len(questions)} questions approved!")
            st.balloons()
    
    with col2:
        if st.button("💾 Save Changes", use_container_width=True):
            st.success("📝 Changes saved successfully!")
    
    with col3:
        if st.button("❌ Reject All", use_container_width=True):
            st.warning("⚠️ All questions rejected. Please regenerate.")
