import streamlit as st
import pandas as pd
from datetime import date, datetime
from gemini_helper import get_ai_suggestion, get_burnout_risk


def show(db, model):
    # Initialize session state for score persistence
    if 'last_score' not in st.session_state:
        st.session_state.last_score = None
    if 'last_ai_suggestion' not in st.session_state:
        st.session_state.last_ai_suggestion = None
    if 'last_checkin_time' not in st.session_state:
        st.session_state.last_checkin_time = None

    # Custom CSS for dark theme consistency
    st.markdown("""
    <style>
        /* Dark background */
        .main {
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
            color: #ffffff;
        }
        
        /* Header styling */
        .checkin-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 50px 30px;
            border-radius: 24px;
            color: white;
            margin-bottom: 40px;
            box-shadow: 0 15px 40px rgba(102, 126, 234, 0.35);
            text-align: center;
            position: relative;
            overflow: hidden;
        }
        
        .checkin-header::before {
            content: "";
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0) 70%);
            z-index: 0;
        }
        
        .checkin-header h1 {
            position: relative;
            z-index: 1;
            font-weight: 800;
            font-size: 3.2em;
            margin: 0;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 20px;
        }
        
        .checkin-header p {
            position: relative;
            z-index: 1;
            font-size: 1.4em;
            opacity: 0.95;
            margin-top: 15px;
            font-weight: 300;
            max-width: 700px;
            margin-left: auto;
            margin-right: auto;
        }
        
        /* Section headers */
        .section-title {
            color: white;
            font-size: 1.8em;
            margin: 30px 0 20px;
            display: flex;
            align-items: center;
            gap: 12px;
        }
        
        /* Slider styling */
        .stSlider {
            padding: 15px 0;
        }
        
        /* Risk card styling */
        .risk-card {
            border-radius: 16px;
            padding: 25px;
            text-align: center;
            height: 100%;
        }
        
        .risk-high {
            background: rgba(239, 68, 68, 0.15);
            border-left: 4px solid #ef4444;
        }
        
        .risk-moderate {
            background: rgba(245, 158, 11, 0.15);
            border-left: 4px solid #f59e0b;
        }
        
        .risk-low {
            background: rgba(16, 185, 129, 0.15);
            border-left: 4px solid #10b981;
        }
        
        /* Score display */
        .score-display {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 45px;
            border-radius: 24px;
            text-align: center;
            color: white;
            margin: 35px 0;
            box-shadow: 0 12px 30px rgba(102, 126, 234, 0.4);
            position: relative;
            overflow: hidden;
        }
        
        .score-display::after {
            content: "";
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, rgba(255,255,255,0.15) 0%, rgba(255,255,255,0) 70%);
            z-index: 0;
        }
        
        .score-value {
            position: relative;
            z-index: 1;
            font-size: 5em;
            font-weight: 800;
            margin: 10px 0;
            text-shadow: 0 4px 15px rgba(0,0,0,0.3);
        }
        
        .score-message {
            position: relative;
            z-index: 1;
            font-size: 1.8em;
            font-weight: 700;
            margin-top: 10px;
        }
        
        .score-timestamp {
            position: relative;
            z-index: 1;
            opacity: 0.85;
            font-size: 1.1em;
            margin-top: 8px;
        }
        
        /* AI suggestion box */
        .ai-suggestion {
            background: rgba(30, 41, 59, 0.7);
            border-radius: 18px;
            padding: 30px;
            border-left: 4px solid #667eea;
            margin: 30px 0;
            box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
        }
        
        /* Action buttons */
        .action-buttons {
            display: flex;
            gap: 20px;
            margin: 30px 0;
            flex-wrap: wrap;
        }
        
        /* Footer */
        .footer-note {
            text-align: center;
            margin-top: 50px;
            padding: 25px;
            color: #64748b;
            font-size: 0.95em;
            border-top: 1px solid rgba(100, 116, 139, 0.3);
            border-radius: 16px;
            background: rgba(30, 41, 59, 0.3);
        }
        
        /* Responsive adjustments */
        @media (max-width: 768px) {
            .checkin-header h1 {
                font-size: 2.4em;
            }
            .checkin-header p {
                font-size: 1.15em;
            }
            .score-value {
                font-size: 4em;
            }
            .score-message {
                font-size: 1.5em;
            }
            .action-buttons {
                flex-direction: column;
            }
            .stButton > button {
                width: 100% !important;
            }
        }
    </style>
    """, unsafe_allow_html=True)

    # Header
    st.markdown("""
    <div class="checkin-header">
        <h1>🧠 Daily Check-In</h1>
        <p>How was your day today? Let's calculate your personalized DayScore!</p>
    </div>
    """, unsafe_allow_html=True)

    # Input section with improved layout
    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown('<div class="section-title">📚 Health & Habits</div>', unsafe_allow_html=True)
        study_hours = st.slider("📚 Study Hours", 0, 12, 5, help="Total hours spent studying today")
        sleep_hours = st.slider("😴 Sleep Hours", 0, 12, 7, help="Hours of quality sleep last night")
        screen_time = st.slider("📱 Screen Time (hours)", 0, 12, 3, help="Total recreational screen time today")

    with col2:
        st.markdown('<div class="section-title">😊 Mental State</div>', unsafe_allow_html=True)
        stress = st.slider("😵 Stress Level (1–10)", 1, 10, 5, help="Current stress level (1=Relaxed, 10=Overwhelmed)")
        mood = st.slider("🙂 Mood (1–10)", 1, 10, 7, help="Current mood (1=Terrible, 10=Amazing)")
        activity_mins = st.slider("🏃 Activity (minutes)", 0, 180, 30, help="Physical activity minutes today")

    # Convert activity → steps (approx)
    steps = activity_mins * 80

    # Burnout Risk Assessment (always visible based on current inputs)
    st.markdown('<div class="section-title">🏥 Wellness Status</div>', unsafe_allow_html=True)
    
    risk_level, recommendation = get_burnout_risk(
        stress=stress,
        sleep_hours=sleep_hours,
        screen_time=screen_time,
        study_hours=study_hours
    )
    
    # Determine risk color class
    if "HIGH" in risk_level:
        risk_class = "risk-high"
        risk_emoji = "🚨"
    elif "MODERATE" in risk_level:
        risk_class = "risk-moderate"
        risk_emoji = "⚠️"
    else:
        risk_class = "risk-low"
        risk_emoji = "✅"
    
    col_risk1, col_risk2 = st.columns([1, 1.5])
    with col_risk1:
        st.markdown(f"""
        <div class="risk-card {risk_class}">
            <div style='font-size: 1.3em; opacity: 0.85; margin-bottom: 10px;'>Burnout Risk</div>
            <div style='font-size: 2.8em; font-weight: 800; margin: 5px 0;'>{risk_level}</div>
            <div style='font-size: 2.5em; margin-top: 5px;'>{risk_emoji}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_risk2:
        st.markdown(f"""
        <div class="risk-card {risk_class}" style='display: flex; align-items: center; justify-content: center;'>
            <p style='font-size: 1.2em; margin: 0; line-height: 1.6;'>{recommendation}</p>
        </div>
        """, unsafe_allow_html=True)

    # Action buttons based on current inputs (always visible)
    st.markdown('<div class="section-title">💡 Recommended Actions</div>', unsafe_allow_html=True)
    
    col_btn1, col_btn2 = st.columns(2)
    
    if stress >= 7 or (st.session_state.last_score and st.session_state.last_score < 60):
        with col_btn1:
            if st.button("🌬️ Try Breathing Exercise", use_container_width=True, type="primary"):
                st.switch_page("pages/breathing.py")
    
    if (st.session_state.last_score and st.session_state.last_score < 70) or stress >= 6:
        with col_btn2:
            if st.button("🎮 Play Relaxing Games", use_container_width=True, type="primary"):
                st.switch_page("pages/games.py")

    # Calculate button - centered with animation
    st.markdown("<div style='text-align: center; margin: 40px 0 30px;'>", unsafe_allow_html=True)
    if st.button("🎯 Calculate My DayScore", use_container_width=True, type="primary", key="score_btn"):
        try:
            # Prepare model input
            input_data = pd.DataFrame([{
                "StressLevel": stress,
                "Mood": mood,
                "StudyHours": study_hours,
                "SleepHours": sleep_hours,
                "ScreenTimeHours": screen_time,
                "ActivityScore": steps
            }])
            
            # Calculate score
            if model is not None:
                try:
                    score = float(model.predict(input_data)[0])
                    score = max(0, min(100, score))  # Clamp to 0-100
                except Exception as e:
                    st.warning(f"⚠️ Model prediction failed, using fallback calculation: {str(e)}")
                    score = calculate_dayscore(stress, mood, sleep_hours, study_hours, screen_time, steps)
            else:
                score = calculate_dayscore(stress, mood, sleep_hours, study_hours, screen_time, steps)
            
            # Save to session state
            st.session_state.last_score = score
            st.session_state.last_checkin_time = datetime.now()
            
            # Save to Firebase immediately
            if db and hasattr(st.session_state, 'user_id') and st.session_state.user_id:
                try:
                    user_id = st.session_state.user_id
                    today = str(date.today())
                    
                    db.collection("dayscores").document(f"{user_id}_{today}").set({
                        "user_id": user_id,
                        "date": today,
                        "timestamp": datetime.now(),
                        "StressLevel": stress,
                        "Mood": mood,
                        "StudyHours": study_hours,
                        "SleepHours": sleep_hours,
                        "ScreenTimeHours": screen_time,
                        "Steps": steps,
                        "DayScore": score,
                        "BurnoutRisk": risk_level
                    }, merge=True)  # Use merge to avoid overwriting existing data
                    
                    st.success("✅ DayScore saved to your wellness profile!")
                except Exception as e:
                    st.warning(f"⚠️ Could not save to database: {str(e)}")
            else:
                st.info("ℹ️ DayScore calculated (database unavailable)")
            
            # Get AI suggestion
            with st.spinner("✨ Getting personalized AI insights..."):
                ai_suggestion = get_ai_suggestion(
                    score=score,
                    stress=stress,
                    mood=mood,
                    sleep_hours=sleep_hours,
                    study_hours=study_hours,
                    screen_time=screen_time
                )
                st.session_state.last_ai_suggestion = ai_suggestion
            
            # Trigger celebration
            st.balloons()
            
        except Exception as e:
            st.error(f"❌ Error calculating DayScore: {str(e)}")
            import traceback
            st.code(traceback.format_exc(), language="python")
    
    st.markdown("</div>", unsafe_allow_html=True)

    # Display results if available in session state
    if st.session_state.last_score is not None:
        score = st.session_state.last_score
        time_since = "just now"
        if st.session_state.last_checkin_time:
            seconds_ago = (datetime.now() - st.session_state.last_checkin_time).seconds
            if seconds_ago < 60:
                time_since = f"{seconds_ago} seconds ago"
            elif seconds_ago < 3600:
                time_since = f"{seconds_ago // 60} minutes ago"
            else:
                time_since = "earlier today"
        
        # Score display with dynamic color and animation
        score_message = get_score_message(score)
        score_color = "#10b981" if score >= 80 else "#f59e0b" if score >= 60 else "#ef4444"
        
        st.markdown(f"""
        <div class="score-display">
            <div class="score-timestamp">Your DayScore • {time_since}</div>
            <div class="score-value" style='color: {score_color};'>{score:.1f}</div>
            <div class="score-message">{score_message}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # AI Suggestions section
        if st.session_state.last_ai_suggestion:
            st.markdown('<div class="section-title">🤖 AI-Powered Insights</div>', unsafe_allow_html=True)
            st.markdown(f"""
            <div class="ai-suggestion">
                {st.session_state.last_ai_suggestion}
            </div>
            """, unsafe_allow_html=True)
    
    # Footer note
    st.markdown("""
    <div class="footer-note">
        <p>💡 Your DayScore is calculated using 6 wellness dimensions • Data is private and only visible to you</p>
        <p>🌙 Consistent check-ins help us provide better personalized insights over time</p>
    </div>
    """, unsafe_allow_html=True)


def calculate_dayscore(stress, mood, sleep_hours, study_hours, screen_time, steps):
    """
    Calculate comprehensive well-being score (0-100) based on user inputs.
    
    Algorithm weights:
    - Sleep quality (20%): 7-9 hours ideal
    - Mood state (20%): Higher = better
    - Stress management (20%): Lower = better  
    - Study balance (15%): 3-6 hours optimal
    - Digital wellness (15%): <3 hours screen time ideal
    - Physical activity (10%): >5000 steps recommended
    
    Returns:
        float: Normalized DayScore between 0-100
    """
    total_possible = 100
    score = 0
    
    # SLEEP (20 points)
    if 7 <= sleep_hours <= 9:
        score += 20
    elif 6 <= sleep_hours < 7 or 9 < sleep_hours <= 10:
        score += 15
    elif 5 <= sleep_hours < 6 or 10 < sleep_hours <= 11:
        score += 8
    else:
        score += 3  # <5 or >11 hours
    
    # MOOD (20 points) - linear scale
    score += (mood / 10) * 20
    
    # STRESS (20 points) - inverse scale
    score += ((10 - stress + 1) / 10) * 20  # +1 to avoid zero when stress=10
    
    # STUDY HOURS (15 points)
    if 3 <= study_hours <= 6:
        score += 15
    elif 2 <= study_hours < 3 or 6 < study_hours <= 8:
        score += 10
    elif 1 <= study_hours < 2 or 8 < study_hours <= 10:
        score += 5
    else:
        score += 2  # <1 or >10 hours
    
    # SCREEN TIME (15 points)
    if screen_time <= 3:
        score += 15
    elif 3 < screen_time <= 5:
        score += 10
    elif 5 < screen_time <= 8:
        score += 5
    else:
        score += 1  # >8 hours
    
    # ACTIVITY (10 points)
    if steps > 7000:
        score += 10
    elif steps > 5000:
        score += 8
    elif steps > 3000:
        score += 5
    elif steps > 1000:
        score += 2
    else:
        score += 0  # <1000 steps
    
    # Normalize to 0-100 (should already be in range but clamp just in case)
    final_score = max(0, min(100, score))
    return round(final_score, 1)


def get_score_message(score):
    """Return appropriate message based on score range"""
    if score >= 90:
        return "🌟 Exceptional Balance!"
    elif score >= 80:
        return "✨ Excellent Well-being"
    elif score >= 70:
        return "😊 Good Balance"
    elif score >= 60:
        return "🙂 Needs Minor Tweaks"
    elif score >= 50:
        return "⚠️ Moderate Imbalance"
    else:
        return "🚨 Needs Attention"