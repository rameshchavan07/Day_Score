import streamlit as st

def show(db):
    st.markdown("""
    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 40px 20px; border-radius: 10px; color: white; margin-bottom: 30px;'>
        <h1 style='margin: 0; color: white;'>👤 Your Profile</h1>
        <p style='margin-top: 10px; opacity: 0.9;'>Manage your wellness journey</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("""
        <div style='text-align: center;'>
            <div style='width: 120px; height: 120px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 50%; margin: 0 auto; display: flex; align-items: center; justify-content: center; color: white; font-size: 3em;'>
                😊
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("### Shivani")
        st.write("**Email:** shivani@example.com")
        st.write("**Joined:** January 2026")
        st.write("**Total Check-ins:** 5")
        st.write("**Average DayScore:** 72.5")
    
    st.markdown("---")
    st.subheader("⚙️ Settings")
    
    col1, col2 = st.columns(2)
    with col1:
        st.checkbox("Enable notifications", value=True)
        st.checkbox("Dark mode", value=False)
    
    with col2:
        st.checkbox("Share analytics", value=True)
        st.checkbox("Weekly report", value=True)
    
    st.markdown("---")
    if st.button("🚪 Logout", use_container_width=True):
        st.success("Logged out successfully!")