import streamlit as st
import pickle
import pandas as pd
from firebase_config import db

# Page config
st.set_page_config(
    page_title="🧠 DayScore+",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={"About": "DayScore+ - Gamifying Student Well-Being with AI"}
)

# Custom CSS for better styling
st.markdown("""
<style>
    [data-testid="stSidebar"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    .main {
        background-color: #f5f7fa;
    }
    .metric-card {
        background: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        margin: 10px 0;
    }
    .header-title {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 30px;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 20px;
    }
    h1 {
        color: #2d3748;
    }
    h2 {
        color: #667eea;
    }
</style>
""", unsafe_allow_html=True)

# Load ML Model with error handling
model = None
try:
    with open("dayscore_model.pkl", "rb") as f:
        model = pickle.load(f)
except FileNotFoundError:
    st.warning("⚠️ ML model not found. Prediction features will be limited.")
except Exception as e:
    st.warning(f"⚠️ Error loading model: {e}")

# Sidebar Navigation
with st.sidebar:
    st.markdown("# 🧠 DayScore+")
    st.markdown("---")
    page = st.radio(
        "Navigate",
        ["Landing Page", "Daily Check-In", "Results Dashboard", "Achievements", "Insights", "Profile"],
        key="page_nav"
    )
    st.markdown("---")
    st.markdown("Made with ❤️ for student wellness")

# Page Routing
try:
    if page == "Landing Page":
        from pages.landing import show
        show(db)
    elif page == "Daily Check-In":
        from pages.checkin import show
        show(db, model)
    elif page == "Results Dashboard":
        from pages.results import show
        show(db)
    elif page == "Achievements":
        from pages.achievements import show
        show(db)
    elif page == "Insights":
        from pages.insights import show
        show(db)
    elif page == "Profile":
        from pages.profile import show
        show(db)
except Exception as e:
    st.error(f"❌ Error loading page: {str(e)}")
    st.info("Check the terminal for detailed error logs.")