import streamlit as st

def show(db):
    st.title("👤 Profile")
    st.markdown("""
    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 40px 20px; border-radius: 10px; color: white; margin-bottom: 30px;'>
        <h1 style='margin: 0; color: white;'>👤 Your Profile</h1>
        <p style='margin-top: 10px; opacity: 0.9;'>Manage your wellness journey</p>
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.user_id and db:
        try:
            # Fetch user data from Firestore
            user_doc = db.collection("users").document(st.session_state.user_id).get()
            
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
                if user_doc.exists:
                    user_data = user_doc.to_dict()
                    st.markdown(f"### {user_data.get('name', 'User')}")
                    st.write(f"**Email:** {st.session_state.user_email}")
                    
                    # Get check-in count and average score
                    try:
                        docs = list(db.collection("dayscores").where("user_id", "==", st.session_state.user_id).stream())
                        checkin_count = len(docs)
                        if checkin_count > 0:
                            scores = [d.to_dict().get('DayScore', 0) for d in docs]
                            avg_score = sum(scores) / len(scores)
                            st.write(f"**Total Check-ins:** {checkin_count}")
                            st.write(f"**Average DayScore:** {avg_score:.1f}")
                    except:
                        st.write("**Total Check-ins:** 0")
                else:
                    st.markdown(f"### {st.session_state.user_email}")
                    st.write("**Status:** New user")
            
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
            if st.button("💾 Save Settings", use_container_width=True):
                st.success("Settings saved successfully!")
        except Exception as e:
            st.error(f"Error loading profile: {e}")
    else:
        st.warning("Please log in to view your profile")