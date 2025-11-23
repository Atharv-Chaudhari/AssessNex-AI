# app/components/question_card.py
import streamlit as st
from config import THEME

def question_card(q, editable=False, question_number=1, key=None):
    """Beautiful question card component"""
    
    qtype = q.get('type', 'MCQ')
    difficulty = q.get('difficulty', 'Medium')
    marks = q.get('marks', 0)
    
    # Color for difficulty
    difficulty_colors = {
        'Easy': THEME['success'],
        'Medium': THEME['warning'],
        'Hard': THEME['danger']
    }
    diff_color = difficulty_colors.get(difficulty, THEME['muted'])
    
    # Color for type badge
    type_colors = {
        'MCQ': THEME['primary'],
        'Short': THEME['accent'],
        'Long': '#8B5CF6',
        'Fill-in': '#EC4899',
        'Coding': '#6366F1',
        'True/False': '#14B8A6'
    }
    type_color = type_colors.get(qtype, THEME['primary'])
    
    st.markdown(f"""
    <div class="card fade-in" style="padding: 16px; margin-bottom: 16px; border-left: 4px solid {type_color};">
        <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 12px;">
            <div style="flex: 1;">
                <h4 style="margin: 0; color: {THEME['text']}; font-size: 15px; font-weight: 600;">
                    Question {question_number}
                </h4>
            </div>
            <div style="display: flex; gap: 6px;">
                <span style="background: {type_color}20; color: {type_color}; padding: 4px 8px; border-radius: 4px; font-size: 11px; font-weight: 600;">
                    {qtype}
                </span>
                <span style="background: {diff_color}20; color: {diff_color}; padding: 4px 8px; border-radius: 4px; font-size: 11px; font-weight: 600;">
                    {difficulty}
                </span>
                <span style="background: {THEME['primary']}20; color: {THEME['primary']}; padding: 4px 8px; border-radius: 4px; font-size: 11px; font-weight: 600;">
                    ⭐ {marks}
                </span>
            </div>
        </div>
        
        <p style="margin: 0 0 12px 0; color: {THEME['text']}; font-size: 14px; line-height: 1.6;">
            {q.get('text', 'Question text not available')}
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Options if MCQ
    if qtype == 'MCQ' and q.get("choices"):
        st.markdown(f"<p style=\"color: {THEME['muted']}; font-size: 12px; font-weight: 600; margin-bottom: 8px;\">OPTIONS:</p>", unsafe_allow_html=True)
        for i, choice in enumerate(q["choices"]):
            st.markdown(f"""
            <div style="background: {THEME['soft']}; padding: 8px 12px; margin-bottom: 6px; border-radius: 6px; font-size: 13px; color: {THEME['text']};">
                <strong>{chr(65+i)}.</strong> {choice}
            </div>
            """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
    
    # Edit mode
    if editable:
        key_prefix = str(key or q.get('id', 'q_default'))
        with st.expander(f"✏️ Edit Question {question_number}", expanded=False):
            new_text = st.text_area(
                "Question Text",
                value=q.get('text', ''),
                key=f"{key_prefix}_text",
                height=100
            )
            q['text'] = new_text
            
            if qtype == 'MCQ' and q.get("choices"):
                st.markdown("**Edit Options**")
                new_choices = []
                for i, choice in enumerate(q["choices"]):
                    new_choice = st.text_input(
                        f"Option {chr(65+i)}",
                        value=choice,
                        key=f"{key_prefix}_choice_{i}"
                    )
                    new_choices.append(new_choice)
                q['choices'] = new_choices
    
    # Action buttons
    col1, col2, col3, col4, col5 = st.columns(5)
    
    key_prefix = str(key or q.get('id', 'q_default'))
    
    with col1:
        if st.button("✅ Approve", key=f"{key_prefix}_approve", use_container_width=True):
            st.success("✅ Question approved!")
    
    with col2:
        if st.button("⚠️ Flag", key=f"{key_prefix}_flag", use_container_width=True):
            st.warning("⚠️ Question flagged for review")
    
    with col3:
        if st.button("❌ Reject", key=f"{key_prefix}_reject", use_container_width=True):
            st.error("❌ Question rejected")
    
    with col4:
        if st.button("🔄 Regen", key=f"{key_prefix}_regen", use_container_width=True):
            st.info("🔄 Regenerating similar question...")
    
    with col5:
        if st.button("📋 Copy", key=f"{key_prefix}_copy", use_container_width=True):
            st.success("📋 Question copied to clipboard!")
