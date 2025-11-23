# app/pages/exam_builder.py
import streamlit as st
from config import THEME
from utils.api_client import post

def exam_builder_page():
    """Beautiful exam builder with drag-and-drop interface"""
    # Header
    st.markdown(f"""
    <div class="card card-elevated fade-in" style="padding: 20px; background: linear-gradient(135deg, {THEME['primary']}15 0%, {THEME['accent']}15 100%); margin-bottom: 24px;">
        <h1 style="margin: 0; color: {THEME['primary']}; font-size: 28px;">🎯 Exam Builder</h1>
        <p style="margin: 8px 0 0 0; color: {THEME['muted']}; font-size: 14px;">Create and customize your exam papers</p>
    </div>
    """, unsafe_allow_html=True)
    
    questions = st.session_state.get("last_generated", [])
    
    if not questions:
        st.info("""
        📭 No questions available.
        
        **Please follow these steps:**
        1. Go to **Upload** and upload documents
        2. Go to **Generation** and create questions
        3. Go to **Review** to approve questions
        4. Return here to build your exam
        """)
        return
    
    # Exam details
    st.markdown(f'<h3 style="color: {THEME["text"]}; margin-bottom: 16px;">📋 Exam Details</h3>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        exam_name = st.text_input(
            "📝 Exam Title",
            value="Midterm Assessment",
            placeholder="Enter exam title"
        )
    with col2:
        duration = st.number_input(
            "⏱️ Duration (minutes)",
            min_value=30,
            max_value=240,
            value=120,
            step=15
        )
    
    # Question selection
    st.markdown(f'<h3 style="color: {THEME["text"]}; margin-bottom: 16px; margin-top: 24px;">❓ Select Questions</h3>', unsafe_allow_html=True)
    
    selected_indices = st.multiselect(
        "Choose questions to include",
        range(len(questions)),
        default=range(len(questions)),
        format_func=lambda i: f"Q{i+1}: {questions[i].get('text', 'Question')[:50]}..."
    )
    
    # Show selected questions preview
    if selected_indices:
        st.markdown(f'<h3 style="color: {THEME["text"]}; margin-bottom: 16px; margin-top: 24px;">👀 Preview</h3>', unsafe_allow_html=True)
        
        total_marks = 0
        for idx, q_idx in enumerate(selected_indices, 1):
            q = questions[q_idx]
            marks = q.get('marks', 0)
            total_marks += marks
            
            st.markdown(f"""
            <div class="card" style="padding: 16px; margin-bottom: 12px;">
                <div style="display: flex; justify-content: space-between; align-items: start;">
                    <div style="flex: 1;">
                        <p style="margin: 0; font-weight: 600; color: {THEME['text']}; font-size: 15px;">Q{idx}. {q.get('text', 'Question')[:100]}</p>
                        <div style="margin-top: 8px; display: flex; gap: 12px;">
                            <span style="background: {THEME['soft']}; padding: 4px 8px; border-radius: 4px; font-size: 12px; color: {THEME['muted']};">
                                Type: <strong>{q.get('type', 'MCQ')}</strong>
                            </span>
                            <span style="background: {THEME['soft']}; padding: 4px 8px; border-radius: 4px; font-size: 12px; color: {THEME['muted']};">
                                Marks: <strong>{marks}</strong>
                            </span>
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Summary
        st.markdown(f"""
        <div class="card card-elevated" style="padding: 16px; text-align: center; margin-top: 20px;">
            <p style="margin: 0; color: {THEME['muted']}; font-size: 14px;">TOTAL MARKS</p>
            <h2 style="margin: 8px 0 0 0; color: {THEME['primary']}; font-size: 32px;">{total_marks}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Save button
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("💾 Save Exam", use_container_width=True, type="primary"):
            payload = {
                "title": exam_name,
                "duration": duration,
                "questions": [questions[i] for i in selected_indices],
                "total_marks": sum([questions[i].get('marks', 0) for i in selected_indices])
            }
            resp = post("save_exam", data=payload)
            st.success(f"✅ Exam saved successfully! ID: {resp.get('exam_id')}")
            st.balloons()
