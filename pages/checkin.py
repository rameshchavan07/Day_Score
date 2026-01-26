import streamlit as st
import pandas as pd
from datetime import date


def show(db, model):
    # Header
    st.markdown("""
    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 40px 20px; border-radius: 10px; color: white; margin-bottom: 30px;'>
        <h1 style='margin: 0; color: white;'>🧠 Daily Check-In</h1>
        <p style='margin-top: 10px; opacity: 0.9;'>How was your day today? Let's calculate your DayScore!</p>
    </div>
    """, unsafe_allow_html=True)

    # Input section
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📚 Health & Habits")
        study_hours = st.slider("📚 Study Hours", 0, 12, 5, help="Total hours spent studying")
        sleep_hours = st.slider("😴 Sleep Hours", 0, 12, 7, help="Hours of sleep last night")
        screen_time = st.slider("📱 Screen Time (hours)", 0, 12, 3, help="Total screen time today")

    with col2:
        st.subheader("😊 Mental State")
        stress = st.slider("😵 Stress Level (1–10)", 1, 10, 5, help="How stressed are you? (1=Low, 10=High)")
        mood = st.slider("🙂 Mood (1–10)", 1, 10, 7, help="How's your mood? (1=Bad, 10=Great)")
        activity_mins = st.slider("🏃 Activity (minutes)", 0, 180, 30, help="Physical activity minutes")

    # Convert activity → steps (approx)
    steps = activity_mins * 80

    # Prepare model input
    input_data = pd.DataFrame([{
        "StressLevel": stress,
        "Mood": mood,
        "StudyHours": study_hours,
        "SleepHours": sleep_hours,
        "ScreenTimeHours": screen_time,
        "ActivityScore": steps
    }])

    # Score button
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🎯 Calculate My DayScore", use_container_width=True, key="score_btn"):
            # Predict DayScore
            score = float(model.predict(input_data)[0])

            # Display result with styling
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 40px; border-radius: 15px; text-align: center; color: white; margin: 30px 0;'>
                <h2 style='margin: 0; font-size: 2.5em;'>✨ {score:.1f}</h2>
                <p style='margin-top: 10px; font-size: 1.2em;'>Your DayScore</p>
                <p style='opacity: 0.9; margin-top: 10px;'>Great work maintaining your well-being!</p>
            </div>
            """, unsafe_allow_html=True)

            st.balloons()

            # Save to Firebase
            if db:
                try:
                    user_id = "shivani_demo"
                    today = str(date.today())

                    db.collection("dayscores").document(f"{user_id}_{today}").set({
                        "user_id": user_id,
                        "date": today,
                        "StressLevel": stress,
                        "Mood": mood,
                        "StudyHours": study_hours,
                        "SleepHours": sleep_hours,
                        "ScreenTimeHours": screen_time,
                        "Steps": steps,
                        "DayScore": score
                    })
                    st.success("✅ Saved to your profile!")
                except Exception as e:
                    st.warning(f"Could not save to database: {e}")