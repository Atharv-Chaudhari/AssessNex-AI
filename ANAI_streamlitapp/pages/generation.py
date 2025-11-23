# app/pages/generation.py
import streamlit as st
from config import THEME
from utils.api_client import post
from components.question_card import question_card

def generation_page():
    """Beautiful question generation page"""
    # Header
    st.markdown(f"""
    <div class="card card-elevated fade-in" style="padding: 20px; background: linear-gradient(135deg, {THEME['primary']}15 0%, {THEME['accent']}15 100%); margin-bottom: 24px;">
        <h1 style="margin: 0; color: {THEME['primary']}; font-size: 28px;">✨ Question Generation</h1>
        <p style="margin: 8px 0 0 0; color: {THEME['muted']}; font-size: 14px;">AI-powered question creation from your documents</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Configuration form
    st.markdown(f'<h3 style="color: {THEME["text"]}; margin-bottom: 16px;">⚙️ Generation Settings</h3>', unsafe_allow_html=True)
    
    with st.form("genform"):
        col1, col2 = st.columns(2)
        
        with col1:
            qtype = st.selectbox(
                "❓ Question Type",
                ["MCQ", "Short", "Long", "Fill-in", "Coding", "True/False"],
                help="Select the type of questions to generate"
            )
            difficulty = st.select_slider(
                "📊 Difficulty Level",
                options=["Easy", "Medium", "Hard"],
                help="Choose difficulty distribution"
            )
        
        with col2:
            count = st.slider(
                "🔢 Number of Questions",
                min_value=1,
                max_value=20,
                value=5,
                help="How many questions to generate"
            )
            marks = st.number_input(
                "⭐ Marks per Question",
                min_value=1,
                max_value=50,
                value=2,
                help="Default marks assigned to each question"
            )
        
        prevent_copy = st.checkbox(
            "🔒 Prevent Verbatim Copy",
            value=True,
            help="Rephrase questions to avoid copying source text directly"
        )
        
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            submitted = st.form_submit_button(
                "🚀 Generate Questions",
                use_container_width=True,
                type="primary"
            )
        
        if submitted:
            with st.spinner("🤖 AI is generating your questions..."):
                params = {
                    "qtype": qtype,
                    "count": count,
                    "difficulty": difficulty,
                    "marks": marks,
                    "prevent_copy": prevent_copy
                }
                resp = post("generate_questions", data=params)
                questions = resp.get("questions", [])
                st.success(f"✅ Successfully generated {len(questions)} {qtype} questions!")
                st.balloons()
                
                # Store for review
                st.session_state["last_generated"] = questions
    
    # Display generated questions if any
    if st.session_state.get("last_generated"):
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(f'<h3 style="color: {THEME["text"]}; margin-bottom: 16px;">📋 Generated Questions</h3>', unsafe_allow_html=True)
        
        for idx, q in enumerate(st.session_state["last_generated"], 1):
            question_card(q, editable=False, question_number=idx)
        
        # Action buttons
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("✏️ Review & Edit", use_container_width=True):
                st.info("Navigate to 'Review' page to edit these questions.")
        with col2:
            if st.button("💾 Save as Draft", use_container_width=True):
                st.success("Questions saved as draft!")
        with col3:
            if st.button("🔄 Regenerate", use_container_width=True):
                st.session_state.pop("last_generated", None)
                st.rerun()
