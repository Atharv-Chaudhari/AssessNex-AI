# app/pages/student.py
import streamlit as st
from utils.api_client import get
from config import THEME

def student_page():
    """Beautiful student practice and assignment page"""
    user = st.session_state.get("auth", {}).get("user", {"id": 1, "name": "Student"})
    
    # Header
    st.markdown(f"""
    <div class="card card-elevated fade-in" style="padding: 20px; background: linear-gradient(135deg, {THEME['primary']}15 0%, {THEME['accent']}15 100%); margin-bottom: 24px;">
        <h1 style="margin: 0; color: {THEME['primary']}; font-size: 28px;">📚 Practice & Assignments</h1>
        <p style="margin: 8px 0 0 0; color: {THEME['muted']}; font-size: 14px;">Complete your assignments and practice questions</p>
    </div>
    """, unsafe_allow_html=True)
    
    assigned = get("student_questions", params={"user_id": user.get("id")})
    assignments = assigned.get("assigned", [
        {"id": 1, "title": "Biology Chapter 3 Quiz", "due_date": "2024-11-25", "status": "Pending", "questions": 15},
        {"id": 2, "title": "Chemistry Basics Test", "due_date": "2024-11-28", "status": "Completed", "questions": 20, "score": "85/100"},
        {"id": 3, "title": "Physics Practice Set", "due_date": "2024-12-02", "status": "Pending", "questions": 10},
    ])
    
    if not assignments:
        st.info("📭 No assignments available yet. Check back later!")
        return
    
    # Tabs for different views
    tab1, tab2 = st.tabs(["📝 Assignments", "📊 Results"])
    
    with tab1:
        st.markdown(f'<h3 style="color: {THEME["text"]}; margin-bottom: 16px;">Your Assignments</h3>', unsafe_allow_html=True)
        
        for assignment in assignments:
            status = assignment.get("status", "Pending")
            status_color = THEME['success'] if status == "Completed" else THEME['warning']
            status_icon = "✅" if status == "Completed" else "⏳"
            
            st.markdown(f"""
            <div class="card" style="padding: 16px; margin-bottom: 12px;">
                <div style="display: flex; justify-content: space-between; align-items: start;">
                    <div style="flex: 1;">
                        <p style="margin: 0; font-weight: 600; color: {THEME['text']}; font-size: 16px;">📄 {assignment.get('title', 'Assignment')}</p>
                        <div style="margin-top: 8px; display: flex; gap: 16px;">
                            <span style="font-size: 13px; color: {THEME['muted']};">
                                📅 Due: <strong>{assignment.get('due_date', 'N/A')}</strong>
                            </span>
                            <span style="font-size: 13px; color: {THEME['muted']};">
                                ❓ Questions: <strong>{assignment.get('questions', 0)}</strong>
                            </span>
                        </div>
                    </div>
                    <div style="text-align: right;">
                        <p style="margin: 0; font-size: 13px; color: {status_color}; font-weight: 600;">{status_icon} {status}</p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if status == "Pending":
                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.button("▶️ Start", key=f"start_{assignment.get('id')}", use_container_width=True):
                        st.session_state[f"practicing_{assignment.get('id')}"] = True
                        st.rerun()
                with col2:
                    if st.button("📖 Preview", key=f"preview_{assignment.get('id')}", use_container_width=True):
                        st.info("Preview mode: View questions without answering")
                with col3:
                    if st.button("⏱️ Schedule", key=f"schedule_{assignment.get('id')}", use_container_width=True):
                        st.info("Reminder set for this assignment")
            else:
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("👁️ View Results", key=f"view_{assignment.get('id')}", use_container_width=True):
                        st.success(f"Your Score: {assignment.get('score', 'N/A')}")
                with col2:
                    if st.button("🔄 Retake", key=f"retake_{assignment.get('id')}", use_container_width=True):
                        st.info("This assignment cannot be retaken")
    
    with tab2:
        st.markdown(f'<h3 style="color: {THEME["text"]}; margin-bottom: 16px;">Your Results</h3>', unsafe_allow_html=True)
        
        completed = [a for a in assignments if a.get("status") == "Completed"]
        
        if completed:
            for assignment in completed:
                score_parts = assignment.get('score', '0/100').split('/')
                score = int(score_parts[0]) if len(score_parts) > 0 else 0
                total = int(score_parts[1]) if len(score_parts) > 1 else 100
                percentage = (score / total * 100) if total > 0 else 0
                
                # Determine color based on score
                if percentage >= 80:
                    color = THEME['success']
                    grade = "A"
                elif percentage >= 70:
                    color = THEME['primary']
                    grade = "B"
                elif percentage >= 60:
                    color = THEME['warning']
                    grade = "C"
                else:
                    color = THEME['danger']
                    grade = "F"
                
                st.markdown(f"""
                <div class="card" style="padding: 16px; margin-bottom: 12px;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <p style="margin: 0; font-weight: 600; color: {THEME['text']}; font-size: 15px;">{assignment.get('title', 'Assignment')}</p>
                            <p style="margin: 4px 0 0 0; font-size: 13px; color: {THEME['muted']};\">{assignment.get('due_date', 'N/A')}</p>
                        </div>
                        <div style="text-align: right;">
                            <h3 style="margin: 0; color: {color}; font-size: 28px; font-weight: 700;">{grade}</h3>
                            <p style="margin: 4px 0 0 0; font-size: 13px; color: {color}; font-weight: 600;">{assignment.get('score', 'N/A')}</p>
                        </div>
                    </div>
                    <div style="margin-top: 12px; background: {THEME['soft']}; border-radius: 4px; height: 4px; overflow: hidden;">
                        <div style="background: {color}; height: 100%; width: {percentage}%;\"></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("📭 No completed assignments yet")
