import streamlit as st

def show(db):
    st.markdown("""
    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 40px 20px; border-radius: 10px; color: white; margin-bottom: 30px;'>
        <h1 style='margin: 0; color: white;'>🏆 Achievements</h1>
        <p style='margin-top: 10px; opacity: 0.9;'>Unlock badges as you improve your well-being</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style='background: white; padding: 30px; border-radius: 10px; text-align: center; box-shadow: 0 2px 8px rgba(0,0,0,0.1);'>
            <h1 style='font-size: 3em; margin: 0;'>🌟</h1>
            <p style='margin-top: 10px; font-weight: bold;'>Early Riser</p>
            <p style='font-size: 0.9em; color: #666;'>Sleep 8+ hours</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style='background: white; padding: 30px; border-radius: 10px; text-align: center; box-shadow: 0 2px 8px rgba(0,0,0,0.1);'>
            <h1 style='font-size: 3em; margin: 0;'>💪</h1>
            <p style='margin-top: 10px; font-weight: bold;'>Active Streak</p>
            <p style='font-size: 0.9em; color: #666;'>7 days of exercise</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style='background: white; padding: 30px; border-radius: 10px; text-align: center; box-shadow: 0 2px 8px rgba(0,0,0,0.1);'>
            <h1 style='font-size: 3em; margin: 0;'>🧠</h1>
            <p style='margin-top: 10px; font-weight: bold;'>Scholar</p>
            <p style='font-size: 0.9em; color: #666;'>Study 50+ hours</p>
        </div>
        """, unsafe_allow_html=True)