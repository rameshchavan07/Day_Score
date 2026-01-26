import streamlit as st
import pandas as pd
from datetime import date

def show(db):
    st.markdown("""
    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 40px 20px; border-radius: 10px; color: white; margin-bottom: 30px;'>
        <h1 style='margin: 0; color: white;'>📊 Results Dashboard</h1>
        <p style='margin-top: 10px; opacity: 0.9;'>Your daily performance and analytics</p>
    </div>
    """, unsafe_allow_html=True)

    if db and st.session_state.user_id:
        try:
            user_id = st.session_state.user_id
            today_doc = db.collection("dayscores").document(f"{user_id}_{date.today()}").get()
            
            if today_doc.exists:
                data = today_doc.to_dict()
                dayscore = data.get('DayScore', 0)
                
                # Display score
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("🎯 Today's DayScore", f"{dayscore:.1f}", "+5.2")
                
                with col2:
                    st.metric("🔥 Current Streak", "3 days", "+1")
                
                with col3:
                    st.metric("⭐ Total XP", "234", "+78")
                
                st.markdown("---")
                
                # Progress bar
                st.subheader("Daily Progress")
                st.progress(min(dayscore / 100, 1.0))
                
                # Burnout risk
                st.subheader("🏥 Wellness Status")
                if dayscore > 80:
                    st.success("Great! Low burnout risk 🟢")
                elif dayscore > 50:
                    st.warning("Moderate burnout risk 🟡 - Consider taking a break")
                else:
                    st.error("High burnout risk 🔴 - Please prioritize rest")
                
                # Stats breakdown
                st.subheader("📈 Today's Stats")
                stat_cols = st.columns(3)
                
                with stat_cols[0]:
                    st.info(f"😴 Sleep: {data.get('SleepHours', 0)} hours")
                
                with stat_cols[1]:
                    st.info(f"📚 Study: {data.get('StudyHours', 0)} hours")
                
                with stat_cols[2]:
                    st.info(f"🙂 Mood: {data.get('Mood', 0)}/10")
            else:
                st.info("📝 No data yet. Complete your daily check-in to see results!")
                if st.button("Go to Daily Check-In"):
                    st.switch_page("pages/checkin.py")
        except Exception as e:
            st.error(f"Error loading results: {e}")
    else:
        st.warning("Please log in to view your results")