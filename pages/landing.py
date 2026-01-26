from datetime import date
import streamlit as st

def show(db):
    # Hero section
    st.markdown("""
    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 60px 20px; border-radius: 15px; text-align: center; color: white; margin-bottom: 30px;'>
        <h1 style='font-size: 3em; margin: 0; color: white;'>🧠 DayScore+</h1>
        <h3 style='margin-top: 10px; font-weight: 300;'>Gamifying Student Well-Being with AI</h3>
        <p style='font-size: 1.1em; margin-top: 20px; opacity: 0.9;'>Track your daily habits and optimize your well-being</p>
    </div>
    """, unsafe_allow_html=True)

    # Stats section
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style='background: white; padding: 20px; border-radius: 10px; text-align: center; box-shadow: 0 2px 8px rgba(0,0,0,0.1);'>
            <h2 style='color: #667eea; margin: 0;'>📊</h2>
            <p style='font-size: 0.9em; color: #666; margin: 10px 0 0 0;'>Track Progress</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style='background: white; padding: 20px; border-radius: 10px; text-align: center; box-shadow: 0 2px 8px rgba(0,0,0,0.1);'>
            <h2 style='color: #667eea; margin: 0;'>🎯</h2>
            <p style='font-size: 0.9em; color: #666; margin: 10px 0 0 0;'>AI Predictions</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style='background: white; padding: 20px; border-radius: 10px; text-align: center; box-shadow: 0 2px 8px rgba(0,0,0,0.1);'>
            <h2 style='color: #667eea; margin: 0;'>🏆</h2>
            <p style='font-size: 0.9em; color: #666; margin: 10px 0 0 0;'>Achievements</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    
    # CTA
    st.markdown("""
    <div style='text-align: center; padding: 40px 20px;'>
        <h2 style='color: #2d3748;'>Ready to improve your day?</h2>
        <p style='color: #666; font-size: 1.1em;'>Start your daily check-in now!</p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("📝 Start Daily Check-In", key="cta_btn", use_container_width=True):
        st.switch_page("pages/checkin.py")

    st.markdown("---")
    
    # Show latest score if available
    if db:
        try:
            doc = db.collection("dayscores").document(f"shivani_demo_{date.today()}").get()
            if doc.exists:
                data = doc.to_dict()
                st.success(f"✨ Today's DayScore: **{data.get('DayScore', 0):.1f}**")
        except:
            pass