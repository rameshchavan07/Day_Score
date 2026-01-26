import streamlit as st
import pickle
import pandas as pd
from firebase_config import db

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_id" not in st.session_state:
    st.session_state.user_id = None
if "user_email" not in st.session_state:
    st.session_state.user_email = None

# Page config
st.set_page_config(
    page_title="🧠 DayScore+",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={"About": "DayScore+ - Gamifying Student Well-Being with AI"}
)

# Enhanced Custom CSS
st.markdown("""
<style>
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%) !important;
    }
    
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
        color: white !important;
    }
    
    [data-testid="stSidebar"] label {
        color: white !important;
        font-weight: 600 !important;
    }
    
    [data-testid="stSidebar"] [role="radio"] {
        accent-color: #ffd700 !important;
    }
    
    [data-testid="stSidebar"] .stButton > button {
        background: linear-gradient(135deg, #ffd700 0%, #ffed4e 100%) !important;
        color: #333 !important;
        font-weight: 700 !important;
        border: none !important;
        transition: all 0.3s ease !important;
    }
    
    [data-testid="stSidebar"] .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 5px 15px rgba(255, 215, 0, 0.4) !important;
    }
    
    /* Main area */
    .main {
        background-color: #f5f7fa;
    }
    
    /* Header styling */
    h1 {
        color: #2d3748 !important;
    }
    
    h2 {
        color: #667eea !important;
    }
    
    /* Sidebar radio buttons */
    [data-testid="stSidebar"] [role="radiogroup"] {
        gap: 0 !important;
    }
    
    [data-testid="stSidebar"] [role="radio"] > span {
        color: white !important;
        font-size: 1.05em !important;
    }
    
    /* Selected option highlight */
    [data-testid="stSidebar"] [aria-checked="true"] {
        background: rgba(255, 255, 255, 0.2) !important;
        border-radius: 8px !important;
    }
    
    /* Divider in sidebar */
    [data-testid="stSidebar"] hr {
        border-color: rgba(255, 255, 255, 0.3) !important;
        margin: 20px 0 !important;
    }
</style>
""", unsafe_allow_html=True)

# Check if user is logged in
if not st.session_state.logged_in:
    try:
        from pages.auth import show
        show()
    except Exception as e:
        st.error(f"❌ Error loading auth page: {str(e)}")
else:
    # Load ML Model with error handling
    model = None
    try:
        with open("dayscore_model.pkl", "rb") as f:
            model = pickle.load(f)
    except FileNotFoundError:
        st.warning("⚠️ ML model not found. Using default scoring formula.")
    except Exception as e:
        st.warning(f"⚠️ Error loading model: {e}. Using default scoring.")

    # Sidebar Navigation
    with st.sidebar:
        st.markdown("""
        <div style='text-align: center; padding: 20px 0; background: rgba(255,255,255,0.1); border-radius: 10px; margin-bottom: 30px;'>
            <h2 style='color: white; margin: 0; font-size: 1.8em;'>🧠 DayScore+</h2>
            <p style='color: rgba(255,255,255,0.9); margin: 10px 0 0 0; font-size: 0.9em;'>Your Wellness Companion</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"<p style='color: white; font-size: 0.95em; margin-bottom: 20px;'><strong>👤 {st.session_state.user_email}</strong></p>", unsafe_allow_html=True)
        st.markdown("<hr style='border-color: rgba(255,255,255,0.3);'>", unsafe_allow_html=True)
        
        st.markdown("<p style='color: rgba(255,255,255,0.8); font-weight: 600; margin-bottom: 15px; font-size: 0.9em;'>📱 NAVIGATE</p>", unsafe_allow_html=True)
        
        page = st.radio(
            "Select Page:",
            ["🏠 Landing", "📝 Check-In", "📊 Results", "📈 Analytics", "🏆 Achievements", "🌬️ Breathing", "🎮 Games", "💡 Insights", "👤 Profile"],
            key="page_nav",
            label_visibility="collapsed"
        )
        
        st.markdown("<hr style='border-color: rgba(255,255,255,0.3);'>", unsafe_allow_html=True)
        
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.user_id = None
            st.session_state.user_email = None
            st.rerun()
        
        st.markdown("<hr style='border-color: rgba(255,255,255,0.3);'>", unsafe_allow_html=True)
        st.markdown("<p style='color: rgba(255,255,255,0.6); text-align: center; font-size: 0.85em; margin: 20px 0 0 0;'>Made with ❤️ for student wellness</p>", unsafe_allow_html=True)

    # Page Routing with error handling
    try:
        if "Landing" in page:
            from pages.landing import show
            show(db)
        elif "Check-In" in page:
            from pages.checkin import show
            show(db, model)
        elif "Results" in page:
            from pages.results import show
            show(db)
        elif "Analytics" in page:
            from pages.analytics import show
            show(db)
        elif "Achievements" in page:
            from pages.achievements import show
            show(db)
        elif "Breathing" in page:
            from pages.breathing import show
            show(db)
        elif "Games" in page:
            from pages.games import show
            show(db)
        elif "Insights" in page:
            from pages.insights import show
            show(db)
        elif "Profile" in page:
            from pages.profile import show
            show(db)
    except Exception as e:
        st.error(f"❌ Error loading page: {str(e)}")
        import traceback
        st.info(f"Details: {traceback.format_exc()}")