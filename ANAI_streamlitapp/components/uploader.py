# app/components/uploader.py
import streamlit as st
from config import THEME
from utils.api_client import post

def file_uploader_component(key_prefix="uploader"):
    """Beautiful file uploader component"""
    
    st.markdown(f"""
    <div class="card card-elevated" style="padding: 24px; text-align: center; border: 2px dashed {THEME['primary']}40; background: {THEME['primary']}05;">
        <div style="font-size: 40px; margin-bottom: 12px;">📤</div>
        <p style="margin: 0 0 8px 0; color: {THEME['text']}; font-weight: 600; font-size: 16px;">
            Drag and Drop or Click to Upload
        </p>
        <p style="margin: 0; color: {THEME['muted']}; font-size: 13px;">
            PDF, Word, PowerPoint, or Image files • Max 100MB
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    uploaded_files = st.file_uploader(
        "Select files to upload",
        accept_multiple_files=True,
        key=f"{key_prefix}_files",
        label_visibility="collapsed"
    )
    
    if uploaded_files:
        st.markdown(f'<p style="color: {THEME["text"]}; font-weight: 600; margin-bottom: 12px;">📁 {len(uploaded_files)} file(s) selected</p>', unsafe_allow_html=True)
        
        total_size = 0
        for idx, f in enumerate(uploaded_files, 1):
            name = getattr(f, 'name', getattr(f, 'filename', str(f)))
            size_bytes = len(f.getvalue()) if hasattr(f, 'getvalue') else 0
            size_mb = round(size_bytes / (1024 * 1024), 2)
            total_size += size_mb
            
            st.markdown(f"""
            <div class="card" style="padding: 12px; margin-bottom: 8px; display: flex; justify-content: space-between; align-items: center;">
                <div style="display: flex; align-items: center; gap: 10px; flex: 1;">
                    <div style="font-size: 20px;">📄</div>
                    <div style="flex: 1; min-width: 0;">
                        <p style="margin: 0; color: {THEME['text']}; font-weight: 600; font-size: 13px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">
                            {name}
                        </p>
                        <p style="margin: 2px 0 0 0; color: {THEME['muted']}; font-size: 12px;">
                            {size_mb} MB
                        </p>
                    </div>
                </div>
                <div style="color: {THEME['success']}; font-weight: 700; font-size: 16px;">✓</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="card" style="padding: 12px; text-align: center; background: {THEME['soft']}; margin: 12px 0;">
            <p style="margin: 0; color: {THEME['muted']}; font-size: 12px;">
                <strong>Total Size:</strong> {total_size} MB
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("🚀 Upload Files", key=f"{key_prefix}_upload_btn", use_container_width=True, type="primary"):
                with st.spinner("⏳ Uploading and processing files..."):
                    resp = post("upload", files=uploaded_files)
                    st.success(f"✅ Successfully uploaded {len(uploaded_files)} file(s)!")
                    st.balloons()
    
    return uploaded_files
