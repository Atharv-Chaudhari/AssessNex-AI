# app/nav.py
import streamlit as st
from config import THEME

def sidebar_nav(role):
    """Beautiful sidebar navigation with role-based menu"""
    with st.sidebar:
        # Brand section
        st.markdown(f"""
        <div style="text-align: center; padding: 16px 0; margin-bottom: 16px; border-bottom: 1px solid {THEME['soft']};">
            <div style="font-size: 32px; margin-bottom: 8px;">✨</div>
            <h2 style="margin: 0; color: {THEME['primary']}; font-size: 20px;">AssessNex AI</h2>
            <p style="margin: 4px 0 0 0; color: {THEME['muted']}; font-size: 11px; font-weight: 500; text-transform: uppercase; letter-spacing: 0.5px;">Premium Assessment</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Role-aware menu items
        if role == "Student":
            menu_items = ["Dashboard", "Assigned", "Settings"]
        else:
            menu_items = ["Dashboard", "Upload", "Generation", "Review", "Exam Builder", "Settings"]
        
        # emoji icons
        icon_emoji = {
            "Dashboard": "📊",
            "Upload": "📤",
            "Generation": "✨",
            "Review": "✏️",
            "Exam Builder": "🎯",
            "Settings": "⚙️",
            "Assigned": "📚",
        }
        
        nav_labels = [f"{icon_emoji.get(it, '')} {it}" for it in menu_items]
        label_to_item = {lbl: itm for lbl, itm in zip(nav_labels, menu_items)}
        
        # Navigation menu
        st.markdown(f'<p style="color: {THEME["muted"]}; font-size: 11px; font-weight: 700; text-transform: uppercase; margin: 12px 0 8px 0; letter-spacing: 0.5px;">MENU</p>', unsafe_allow_html=True)
        
        chosen_label = st.radio("Navigate", nav_labels, index=0, key="main_nav", label_visibility="collapsed")
        chosen = label_to_item.get(chosen_label, menu_items[0])
        
        # Divider
        st.markdown(f"<div style=\"height: 1px; background: {THEME['soft']}; margin: 16px 0;\"></div>", unsafe_allow_html=True)
        
        # User info section
        st.markdown(f'<p style="color: {THEME["muted"]}; font-size: 11px; font-weight: 700; text-transform: uppercase; margin: 12px 0 8px 0; letter-spacing: 0.5px;">ACCOUNT</p>', unsafe_allow_html=True)
        
        user = st.session_state.get("auth", {}).get("user", {"name": "Guest", "role": role, "email": ""})
        avatar = user.get("name", "G")[0].upper()
        
        st.markdown(f"""
        <div style="background: {THEME['soft']}; padding: 12px; border-radius: 10px; margin-bottom: 12px;">
            <div style="display: flex; align-items: center; gap: 10px;">
                <div style="width: 40px; height: 40px; border-radius: 8px; background: linear-gradient(135deg, {THEME['primary']} 0%, {THEME['accent']} 100%); display: flex; align-items: center; justify-content: center; color: white; font-weight: 700; font-size: 16px;">
                    {avatar}
                </div>
                <div style="flex: 1; min-width: 0;">
                    <p style="margin: 0; font-weight: 600; color: {THEME['text']}; font-size: 13px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">{user.get('name', 'User')}</p>
                    <p style="margin: 2px 0 0 0; font-size: 11px; color: {THEME['muted']}; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">{user.get('email', '')}</p>
                    <div style="margin-top: 4px;">
                        <span style="background: {THEME['primary']}20; color: {THEME['primary']}; padding: 2px 6px; border-radius: 4px; font-size: 10px; font-weight: 600;">
                            {role}
                        </span>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Quick actions
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Logout", use_container_width=True, key="logout_btn"):
                st.session_state["auth"] = None
                st.rerun()
        with col2:
            if st.button("Profile", use_container_width=True, key="profile_btn"):
                st.session_state["page"] = "Settings"
                st.rerun()
        
        # Footer
        st.markdown(f"""
        <div style="text-align: center; padding: 8px; margin-top: 20px; border-top: 1px solid {THEME['soft']};">
            <p style="margin: 0; font-size: 11px; color: {THEME['muted']};">{role} Dashboard • v1.0.0</p>
        </div>
        """, unsafe_allow_html=True)
        
        return chosen
