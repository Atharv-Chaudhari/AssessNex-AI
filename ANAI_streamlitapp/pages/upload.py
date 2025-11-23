# app/pages/upload.py
import streamlit as st
from components.uploader import file_uploader_component
from config import THEME
from utils.api_client import post, get

def upload_page():
    """Beautiful document upload page"""
    # Header
    st.markdown(f"""
    <div class="card card-elevated fade-in" style="padding: 20px; background: linear-gradient(135deg, {THEME['primary']}15 0%, {THEME['accent']}15 100%); margin-bottom: 24px;">
        <h1 style="margin: 0; color: {THEME['primary']}; font-size: 28px;">📤 Upload Documents</h1>
        <p style="margin: 8px 0 0 0; color: {THEME['muted']}; font-size: 14px;">Upload PDFs, Word docs, or images for processing</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Upload section
    st.markdown(f'<h3 style="color: {THEME["text"]}; margin-bottom: 16px;">📁 Select Files</h3>', unsafe_allow_html=True)
    uploaded = file_uploader_component()
    
    # Refresh button
    col1, col2, col3 = st.columns([1, 3, 1])
    with col3:
        if st.button("🔄 Refresh", use_container_width=True):
            st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Server documents section
    st.markdown(f'<h3 style="color: {THEME["text"]}; margin-bottom: 16px;">📚 Server Documents</h3>', unsafe_allow_html=True)
    
    docs = get("list_docs")
    docs_list = docs.get("docs", [
        {"id": "1", "name": "Biology Chapter 3.pdf", "status": "✅ Ready", "size": "2.4 MB", "parsed": True},
        {"id": "2", "name": "Chemistry Basics.pdf", "status": "⏳ Processing", "size": "1.8 MB", "parsed": False},
        {"id": "3", "name": "Physics Notes.pdf", "status": "✅ Ready", "size": "3.2 MB", "parsed": True},
    ])
    
    if docs_list:
        for doc in docs_list:
            col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
            
            with col1:
                st.markdown(f"""
                <div style="padding: 12px 0;">
                    <p style="margin: 0; font-weight: 600; color: {THEME['text']};">📄 {doc.get('name', 'Document')}</p>
                    <p style="margin: 4px 0 0 0; font-size: 12px; color: {THEME['muted']};\">{doc.get('size', 'Unknown size')}</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                status = "✅" if doc.get("parsed") else "⏳"
                st.markdown(f"""
                <div style="padding: 12px 0; text-align: center;">
                    <p style="margin: 0; font-size: 14px; color: {THEME['success']}; font-weight: 600;">{status}</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                if st.button("👁️", key=f"preview_{doc.get('id')}", help="Preview"):
                    st.info(f"Preview of {doc.get('name')}: Sample text from document...")
            
            with col4:
                if st.button("✨", key=f"parse_{doc.get('id')}", help="Parse/Generate"):
                    with st.spinner("Processing..."):
                        resp = post("parse", data={"doc_id": doc.get("id")})
                        if resp.get("status") == "parsed":
                            st.success(f"✅ {doc.get('name')} processed successfully!")
                        else:
                            st.error("Parse failed")
    else:
        st.info("📭 No documents uploaded yet. Use the upload area above to get started.")
