# app/main.py
import streamlit as st
from config import THEME
from nav import sidebar_nav
from pages import login, register, dashboard, upload, generation, review, exam_builder, student, settings

st.set_page_config(
    page_title="AssessNex AI",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={"Get help": "https://github.com/atharv-chaudhari/AssessNex-AI"}
)

# ============================================================================
# 🎨 MODERN CSS: Premium AI SaaS Design with Animations & Soft Shadows
# ============================================================================
st.markdown(f"""
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">

<style>
    :root {{
        --primary: {THEME['primary']};
        --accent: {THEME['accent']};
        --bg: {THEME['bg']};
        --card: {THEME['card']};
        --muted: {THEME['muted']};
        --text: {THEME['text']};
        --soft: {THEME['soft']};
        --success: {THEME['success']};
        --danger: {THEME['danger']};
        --warning: {THEME['warning']};
        --dark-bg: {THEME['dark_bg']};
        --gradient: linear-gradient(135deg, {THEME['gradient_start']} 0%, {THEME['gradient_end']} 100%);
    }}

    /* ========== GLOBAL STYLES ========== */
    html, body, [data-testid="stAppViewContainer"] {{
        background: var(--bg) !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
        color: var(--text) !important;
    }}

    /* ========== MAIN LAYOUT ========== */
    .css-1d391kg {{ padding-top: 0 !important; }}
    
    .stApp .block-container {{
        padding-top: 1.5rem;
        padding-left: 1.5rem;
        padding-right: 1.5rem;
        max-width: 100%;
        background: transparent !important;
    }}

    /* ========== SIDEBAR STYLING ========== */
    [data-testid="stSidebar"] {{
        background: linear-gradient(180deg, {THEME['card']} 0%, {THEME['soft']} 100%) !important;
        min-width: 260px;
        max-width: 320px;
        border-right: 1px solid {THEME['soft']};
    }}

    [data-testid="stSidebarNav"] {{
        padding-top: 1rem;
    }}

    .sidebar-section {{
        padding: 16px;
        margin-bottom: 8px;
        border-radius: 12px;
        background: {THEME['soft']};
        transition: all 0.3s ease;
    }}

    .sidebar-section:hover {{
        background: {THEME['primary']}10;
        transform: translateX(4px);
    }}

    /* ========== TOP BAR / HEADER ========== */
    .topbar {{
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 16px;
        padding: 16px 20px;
        background: var(--gradient);
        border-radius: 14px;
        box-shadow: 0 8px 24px rgba(59, 130, 246, 0.15);
        margin-bottom: 24px;
        animation: slideDown 0.5s ease-out;
    }}

    @keyframes slideDown {{
        from {{
            opacity: 0;
            transform: translateY(-20px);
        }}
        to {{
            opacity: 1;
            transform: translateY(0);
        }}
    }}

    .brand {{
        display: flex;
        align-items: center;
        gap: 12px;
    }}

    .brand img {{
        height: 40px;
        width: 40px;
        border-radius: 10px;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.25);
    }}

    .brand h1 {{
        font-size: 20px;
        font-weight: 700;
        margin: 0;
        color: white;
        letter-spacing: -0.5px;
    }}

    .brand-subtitle {{
        font-size: 12px;
        color: rgba(255, 255, 255, 0.9);
        font-weight: 500;
    }}

    /* ========== CARDS & CONTAINERS ========== */
    .card {{
        background: {THEME['card']} !important;
        padding: 18px;
        border-radius: 14px;
        box-shadow: 0 2px 8px rgba(30, 41, 59, 0.06);
        border: 1px solid {THEME['soft']};
        transition: all 0.3s ease;
    }}

    .card:hover {{
        box-shadow: 0 8px 24px rgba(30, 41, 59, 0.12);
        border-color: {THEME['primary']}40;
    }}

    .card-elevated {{
        box-shadow: 0 8px 24px rgba(59, 130, 246, 0.15);
        border: 1px solid {THEME['primary']}20;
    }}

    /* ========== BUTTONS ========== */
    .stButton > button {{
        background: var(--gradient);
        color: white !important;
        border-radius: 10px;
        padding: 10px 16px;
        border: none !important;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3) !important;
        font-weight: 600;
        font-size: 14px;
        transition: all 0.3s ease;
    }}

    .stButton > button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(59, 130, 246, 0.4) !important;
    }}

    .stButton > button:active {{
        transform: translateY(0);
    }}

    .btn-secondary {{
        background: {THEME['soft']} !important;
        color: var(--text) !important;
        box-shadow: 0 2px 8px rgba(100, 116, 139, 0.1) !important;
    }}

    .btn-secondary:hover {{
        background: {THEME['muted']}20 !important;
    }}

    .btn-danger {{
        background: {THEME['danger']} !important;
        box-shadow: 0 4px 12px rgba(239, 68, 68, 0.3) !important;
    }}

    .btn-success {{
        background: {THEME['success']} !important;
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3) !important;
    }}

    /* ========== INPUTS & TEXT FIELDS ========== */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > div,
    .stMultiSelect > div > div > div,
    input[type="text"],
    input[type="password"],
    input[type="email"],
    textarea {{
        border-radius: 10px !important;
        padding: 10px 12px !important;
        border: 1px solid {THEME['soft']} !important;
        background: {THEME['card']} !important;
        color: var(--text) !important;
        font-family: 'Inter', sans-serif !important;
        transition: all 0.3s ease;
    }}

    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus,
    input[type="text"]:focus,
    input[type="password"]:focus,
    input[type="email"]:focus,
    textarea:focus {{
        border-color: var(--primary) !important;
        box-shadow: 0 0 0 3px {THEME['primary']}15 !important;
    }}

    .stTextInput > label,
    .stTextArea > label,
    .stSelectbox > label {{
        font-weight: 600;
        color: var(--text);
        font-size: 14px;
    }}

    /* ========== ALERTS & MESSAGES ========== */
    .stAlert {{
        border-radius: 12px !important;
        border-left: 4px solid var(--primary) !important;
        padding: 12px 16px !important;
    }}

    .stSuccess {{
        background: {THEME['success']}10 !important;
        border-left-color: {THEME['success']} !important;
        color: {THEME['success']} !important;
    }}

    .stError {{
        background: {THEME['danger']}10 !important;
        border-left-color: {THEME['danger']} !important;
        color: {THEME['danger']} !important;
    }}

    .stWarning {{
        background: {THEME['warning']}10 !important;
        border-left-color: {THEME['warning']} !important;
        color: {THEME['warning']} !important;
    }}

    .stInfo {{
        background: {THEME['primary']}10 !important;
        border-left-color: var(--primary) !important;
        color: var(--primary) !important;
    }}

    /* ========== HEADERS & TEXT ========== */
    h1, h2, h3, h4, h5, h6 {{
        color: var(--text) !important;
        font-weight: 700;
        letter-spacing: -0.5px;
    }}

    h1 {{
        font-size: 28px;
        margin-top: 24px;
        margin-bottom: 16px;
    }}

    h2 {{
        font-size: 22px;
        margin-top: 20px;
        margin-bottom: 12px;
    }}

    h3 {{
        font-size: 18px;
        margin-top: 16px;
        margin-bottom: 8px;
    }}

    p, span, div {{
        color: var(--text) !important;
    }}

    small, .small-text {{
        color: var(--muted);
        font-size: 13px;
    }}

    /* ========== TABS ========== */
    .stTabs > [data-baseweb="tab-list"] {{
        gap: 8px;
        border-bottom: 2px solid {THEME['soft']};
    }}

    .stTabs > [data-baseweb="tab-list"] button {{
        padding: 12px 16px;
        border-radius: 10px 10px 0 0;
        color: var(--muted) !important;
        font-weight: 500;
        transition: all 0.3s ease;
    }}

    .stTabs > [data-baseweb="tab-list"] button[aria-selected="true"] {{
        background: var(--gradient) !important;
        color: white !important;
        border-bottom: 3px solid var(--primary);
    }}

    /* ========== COLUMNS & EXPANDER ========== */
    .stExpander {{
        border: 1px solid {THEME['soft']} !important;
        border-radius: 10px !important;
        background: {THEME['card']} !important;
    }}

    .stExpander > summary {{
        color: var(--text) !important;
        font-weight: 600;
    }}

    /* ========== DIVIDERS ========== */
    hr {{
        border: none;
        border-top: 1px solid {THEME['soft']};
        margin: 20px 0;
    }}

    /* ========== ANIMATIONS ========== */
    @keyframes fadeIn {{
        from {{ opacity: 0; transform: translateY(10px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}

    @keyframes pulse {{
        0%, 100% {{ opacity: 1; }}
        50% {{ opacity: 0.7; }}
    }}

    .fade-in {{
        animation: fadeIn 0.5s ease-out;
    }}

    .pulse {{
        animation: pulse 2s ease-in-out infinite;
    }}

    /* ========== RESPONSIVE ========== */
    @media (max-width: 768px) {{
        .stApp .block-container {{
            padding-left: 1rem;
            padding-right: 1rem;
        }}

        h1 {{ font-size: 24px; }}
        h2 {{ font-size: 20px; }}
        h3 {{ font-size: 16px; }}
    }}

    /* ========== SCROLLBAR ========== */
    ::-webkit-scrollbar {{
        width: 8px;
        height: 8px;
    }}

    ::-webkit-scrollbar-track {{
        background: {THEME['soft']};
        border-radius: 10px;
    }}

    ::-webkit-scrollbar-thumb {{
        background: {THEME['muted']};
        border-radius: 10px;
    }}

    ::-webkit-scrollbar-thumb:hover {{
        background: var(--primary);
    }}
</style>
""", unsafe_allow_html=True)

# Ensure auth exists in session or send to login
if "auth" not in st.session_state:
    st.session_state.auth = None


def _render_topbar():
    """Render animated top bar with branding"""
    with st.container():
        cols = st.columns([0.02, 1, 0.3])
        with cols[1]:
            st.markdown(
                '<div class="topbar">'
                '<div class="brand">'
                '<img src="https://raw.githubusercontent.com/atharv-chaudhari/AssessNex-AI/main/logo.png" '
                'onerror="this.style.display=\'none\'"/> '
                f'<div><h1>AssessNex AI</h1>'
                '<small class="brand-subtitle">Premium Assessment Platform</small></div>'
                '</div>'
                '<div style="display:flex;gap:8px;align-items:center">'
                '<small style="color:rgba(255,255,255,0.9);font-weight:500">'
                '✨ AI-Powered Assessment Toolkit'
                '</small></div></div>',
                unsafe_allow_html=True
            )


_render_topbar()

# If not authenticated -> show login/register side-by-side
if not st.session_state.get("auth"):
    st.markdown('<div class="card card-elevated" style="margin-top:20px;">', unsafe_allow_html=True)
    cols = st.columns([1, 1])
    with cols[0]:
        st.markdown("### 🔐 Login")
        login.login_page()
    with cols[1]:
        st.markdown("### 📝 Create Account")
        register.register_page()
    st.markdown('</div>', unsafe_allow_html=True)
    st.info("👤 Choose a role and sign in. Roles: **Professor** | **Assistant** | **Student**")
else:
    role = st.session_state["auth"]["user"]["role"]
    page = sidebar_nav(role)
    # main content container
    with st.container():
        try:
            if page == "Dashboard":
                dashboard.dashboard_page()
            elif page == "Upload":
                upload.upload_page()
            elif page == "Generation":
                generation.generation_page()
            elif page == "Review":
                review.review_page()
            elif page == "Exam Builder":
                exam_builder.exam_builder_page()
            elif page == "Assigned":
                student.student_page()
            elif page == "Settings":
                settings.settings_page()
            else:
                st.header(page)
                st.write("Page not found.")
        except Exception as e:
            st.error(f"Error loading page: {str(e)}")
            st.info(f"Page: {page}")

