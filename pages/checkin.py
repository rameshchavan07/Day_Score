import streamlit as st
import pandas as pd
from datetime import date
from gemini_helper import get_ai_suggestion, get_burnout_risk


def show(db, model):
    try:
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
                try:
                    # Predict DayScore using model
                    if model is not None:
                        score = float(model.predict(input_data)[0])
                        # Clamp score between 0-100
                        score = max(0, min(100, score))
                    else:
                        # Calculate score using simple formula if model unavailable
                        score = calculate_dayscore(stress, mood, sleep_hours, study_hours, screen_time, steps)
                except Exception as e:
                    st.warning(f"Model prediction error: {e}")
                    score = calculate_dayscore(stress, mood, sleep_hours, study_hours, screen_time, steps)

                # Display result with styling
                st.markdown(f"""
                <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 40px; border-radius: 15px; text-align: center; color: white; margin: 30px 0;'>
                    <h2 style='margin: 0; font-size: 2.5em;'>✨ {score:.1f}</h2>
                    <p style='margin-top: 10px; font-size: 1.2em;'>Your DayScore</p>
                    <p style='opacity: 0.9; margin-top: 10px;'>Great work maintaining your well-being!</p>
                </div>
                """, unsafe_allow_html=True)

                st.balloons()

                # Get AI Suggestions
                st.markdown("---")
                st.subheader("🤖 AI-Powered Insights")
                
                with st.spinner("🔄 Getting personalized suggestions..."):
                    ai_suggestion = get_ai_suggestion(
                        score=score,
                        stress=stress,
                        mood=mood,
                        sleep_hours=sleep_hours,
                        study_hours=study_hours,
                        screen_time=screen_time
                    )
                
                st.markdown(f"""
                <div style='background: #f0f4ff; padding: 20px; border-radius: 10px; border-left: 4px solid #667eea;'>
                    {ai_suggestion}
                </div>
                """, unsafe_allow_html=True)
            
            # Burnout Risk Assessment
            risk_level, recommendation = get_burnout_risk(
                stress=stress,
                sleep_hours=sleep_hours,
                screen_time=screen_time,
                study_hours=study_hours
            )
            
            st.markdown("---")
            st.subheader("🏥 Wellness Status")
            
            col1, col2 = st.columns([1, 1])
            with col1:
                st.metric("Burnout Risk", risk_level)
            with col2:
                if "HIGH" in risk_level:
                    st.error(recommendation)
                elif "MODERATE" in risk_level:
                    st.warning(recommendation)
                else:
                    st.success(recommendation)
            
            # Action buttons based on score
            st.markdown("---")
            st.subheader("💡 Recommended Actions")
            
            col1, col2 = st.columns(2)
            
            if stress >= 7 or score < 60:
                with col1:
                    if st.button("🌬️ Try Breathing Exercise", use_container_width=True):
                        st.switch_page("pages/breathing.py")
            
            if score < 70 or stress >= 6:
                with col2:
                    if st.button("🎮 Play Relaxing Games", use_container_width=True):
                        st.switch_page("pages/games.py")
            
            # Save to Firebase
            if db:
                try:
                    user_id = st.session_state.user_id
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
    
    except Exception as e:
        st.error(f"❌ Error in check-in page: {str(e)}")
        st.info("Please refresh the page and try again")


def calculate_dayscore(stress, mood, sleep_hours, study_hours, screen_time, steps):
    """
    LEVEL 2: DayScore Calculation Engine
    
    Calculate a comprehensive well-being score (0-100) based on user inputs.
    
    Algorithm:
    - Starts with baseline of 50 points
    - Each factor contributes weighted points based on health guidelines
    - Sleep: 7-9 hours is ideal (15 points max)
    - Mood: Higher is better (15 points max)
    - Stress: Lower is better (15 points max)
    - Study: Moderate 3-6 hours is best (10 points max)
    - Screen time: <3 hours is ideal (10 points max)
    - Activity: >5000 steps recommended (10 points max)
    - Total: 0-100 score
    
    Args:
        stress (int): Stress level 1-10
        mood (int): Mood level 1-10
        sleep_hours (int): Hours of sleep
        study_hours (int): Hours studied
        screen_time (int): Hours on screen
        steps (int): Steps taken (~activity_mins * 80)
    
    Returns:
        float: DayScore 0-100
    """
    score = 50  # Start at baseline
    
    # SLEEP SCORING (15 points max)
    # Ideal range: 7-9 hours
    if 7 <= sleep_hours <= 9:
        score += 15  # Perfect sleep
    elif 6 <= sleep_hours < 7:
        score += 10  # Slightly under
    elif 9 < sleep_hours <= 10:
        score += 10  # Slightly over
    elif 5 <= sleep_hours < 6:
        score += 5   # Significantly under
    # Below 5 or above 10: no bonus (possibly negative impact)
    
    # MOOD SCORING (15 points max)
    # Linear: higher mood = more points
    mood_percentage = (mood / 10)  # 0.0 to 1.0
    score += mood_percentage * 15
    
    # STRESS SCORING (15 points max)
    # Inverse: lower stress = more points
    stress_percentage = (10 - stress) / 10  # 0.0 to 1.0
    score += stress_percentage * 15
    
    # STUDY HOURS SCORING (10 points max)
    # Ideal: 3-6 hours (balanced studying)
    if 3 <= study_hours <= 6:
        score += 10  # Excellent balance
    elif 2 <= study_hours < 3:
        score += 5   # Under-studying
    elif 6 < study_hours <= 8:
        score += 5   # Over-studying
    elif study_hours > 8:
        score += 2   # Excessive (burnout risk)
    # Below 2: no bonus (not enough study)
    
    # SCREEN TIME SCORING (10 points max)
    # Ideal: <3 hours (healthy digital balance)
    if screen_time <= 3:
        score += 10  # Excellent
    elif 3 < screen_time <= 6:
        score += 5   # Moderate
    elif 6 < screen_time <= 8:
        score += 2   # High
    # Above 8: no bonus (digital overload)
    
    # ACTIVITY SCORING (10 points max)
    # Recommended: >5000 steps
    if steps > 5000:
        score += 10  # Excellent activity
    elif steps > 3000:
        score += 5   # Moderate activity
    elif steps > 1000:
        score += 2   # Light activity
    # Below 1000: no bonus (sedentary)
    
    # Clamp to valid range 0-100
    final_score = max(0, min(100, score))
    
    return final_score