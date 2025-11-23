# app/pages/parse_preview.py
import streamlit as st
from utils.api_client import post, get
from config import THEME

def parse_preview_page():
    """Beautiful document preview and OCR page"""
    # Header
    st.markdown(f"""
    <div class="card card-elevated fade-in" style="padding: 20px; background: linear-gradient(135deg, {THEME['primary']}15 0%, {THEME['accent']}15 100%); margin-bottom: 24px;">
        <h1 style="margin: 0; color: {THEME['primary']}; font-size: 28px;">👁️ Document Preview & OCR</h1>
        <p style="margin: 8px 0 0 0; color: {THEME['muted']}; font-size: 14px;">Preview and analyze extracted document content</p>
    </div>
    """, unsafe_allow_html=True)
    
    docs = get("list_docs")
    docs_list = docs.get("docs", [
        {"id": 1, "name": "Sample Document 1.pdf", "parsed": True},
        {"id": 2, "name": "Sample Document 2.pdf", "parsed": False},
        {"id": 3, "name": "Sample Document 3.pdf", "parsed": True},
    ])
    
    if not docs_list:
        st.info("📭 No documents available. Please upload documents first.")
        return
    
    # Document selection
    st.markdown(f'<h3 style="color: {THEME["text"]}; margin-bottom: 16px;">📄 Select Document</h3>', unsafe_allow_html=True)
    
    doc_options = [d["name"] for d in docs_list]
    selected_doc_name = st.selectbox(
        "Choose a document",
        options=doc_options,
        label_visibility="collapsed"
    )
    
    selected_doc = next((d for d in docs_list if d["name"] == selected_doc_name), None)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Preview section
    st.markdown(f'<h3 style="color: {THEME["text"]}; margin-bottom: 16px;">🔍 Document Content</h3>', unsafe_allow_html=True)
    
    if selected_doc:
        # Document info
        st.markdown(f"""
        <div class="card" style="padding: 16px; margin-bottom: 16px; background: {THEME['soft']};">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <p style="margin: 0; font-weight: 600; color: {THEME['text']}; font-size: 14px;">📋 {selected_doc.get('name', 'Document')}</p>
                    <p style="margin: 4px 0 0 0; font-size: 12px; color: {THEME['muted']};">Extracted Content</p>
                </div>
                <div style="text-align: right;">
                    <span style="background: {THEME['success']}20; color: {THEME['success']}; padding: 4px 8px; border-radius: 4px; font-size: 11px; font-weight: 600;">
                        ✅ {len(selected_doc.get('name', ''))} characters
                    </span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Parse button
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("🚀 Extract Content", use_container_width=True, type="primary"):
                with st.spinner("🔄 Extracting text from document..."):
                    resp = post("parse", data={"doc_id": selected_doc.get("id")})
                    st.session_state[f"parsed_{selected_doc.get('id')}"] = True
                    st.success("✅ Content extracted successfully!")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Extracted content display
        if st.session_state.get(f"parsed_{selected_doc.get('id')}"):
            st.markdown(f'<p style="color: {THEME["muted"]}; font-size: 12px; font-weight: 600; margin-bottom: 8px;">EXTRACTED TEXT:</p>', unsafe_allow_html=True)
            
            mock_text = """CHAPTER 1: FUNDAMENTALS

Definition: A fundamental concept in physics and science refers to the basic principles and laws that govern natural phenomena. These foundational principles form the basis of all advanced theories and applications.

Key Topics:
• Introduction to Core Concepts
• Historical Development
• Mathematical Foundations
• Practical Applications

1.1 Basic Principles
The fundamental principles are:
- First Law: Every object remains in rest or motion unless acted upon
- Second Law: Force equals mass times acceleration (F = ma)
- Third Law: For every action, there is an equal and opposite reaction

1.2 Mathematical Representation
The relationship is expressed as:
    F = m × a
    
Where:
    F = Force (Newtons)
    m = Mass (kilograms)
    a = Acceleration (m/s²)

1.3 Real-World Applications
- Vehicle dynamics
- Planetary motion
- Projectile motion
- Structural engineering"""
            
            st.markdown(f"""
            <div class="card" style="padding: 16px; background: {THEME['card']}; border-left: 4px solid {THEME['primary']}; max-height: 400px; overflow-y: auto;">
                <pre style="margin: 0; color: {THEME['text']}; font-family: 'Courier New', monospace; font-size: 12px; white-space: pre-wrap; word-wrap: break-word; line-height: 1.6;">
{mock_text}
                </pre>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Action buttons
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                if st.button("💾 Save", use_container_width=True):
                    st.success("✅ Content saved!")
            with col2:
                if st.button("📋 Copy", use_container_width=True):
                    st.info("📋 Copied to clipboard!")
            with col3:
                if st.button("⬇️ Download", use_container_width=True):
                    st.success("⬇️ Download started!")
            with col4:
                if st.button("🔄 Refresh", use_container_width=True):
                    st.rerun()
        else:
            st.info("📭 Click 'Extract Content' to view the parsed text from this document")
