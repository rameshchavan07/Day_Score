from datetime import date
import streamlit as st
import time

def show(db):
    # Add custom CSS with animations
    st.markdown("""
    <style>
        @keyframes fadeInDown {
            from {
                opacity: 0;
                transform: translateY(-30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        @keyframes slideInLeft {
            from {
                opacity: 0;
                transform: translateX(-50px);
            }
            to {
                opacity: 1;
                transform: translateX(0);
            }
        }
        
        @keyframes slideInRight {
            from {
                opacity: 0;
                transform: translateX(50px);
            }
            to {
                opacity: 1;
                transform: translateX(0);
            }
        }
        
        @keyframes pulse {
            0%, 100% {
                opacity: 1;
            }
            50% {
                opacity: 0.7;
            }
        }
        
        @keyframes float {
            0%, 100% {
                transform: translateY(0px);
            }
            50% {
                transform: translateY(-10px);
            }
        }
        
        .hero-title {
            animation: fadeInDown 1s ease-out;
            font-size: 3.5em !important;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-weight: 800;
            margin: 0 !important;
        }
        
        .hero-subtitle {
            animation: fadeInDown 1.2s ease-out;
            font-size: 1.3em;
            color: #667eea;
            font-weight: 500;
            margin-top: 15px !important;
        }
        
        .hero-description {
            animation: fadeInUp 1.4s ease-out;
            font-size: 1.1em;
            color: #666;
            margin-top: 20px;
            line-height: 1.6;
        }
        
        .stat-card {
            animation: slideInUp 1s ease-out;
            background: white;
            padding: 30px 20px;
            border-radius: 15px;
            text-align: center;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            transition: all 0.3s ease;
            border: 2px solid transparent;
        }
        
        .stat-card:hover {
            transform: translateY(-10px);
            box-shadow: 0 8px 25px rgba(102, 126, 234, 0.2);
            border-color: #667eea;
        }
        
        .stat-icon {
            font-size: 3em;
            margin-bottom: 15px;
            animation: float 3s ease-in-out infinite;
        }
        
        .feature-box {
            animation: fadeInUp 1.5s ease-out;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            border-radius: 15px;
            text-align: center;
        }
        
        .cta-button {
            animation: pulse 2s ease-in-out infinite;
        }
        
        .divider {
            margin: 40px 0;
            border: 0;
            height: 2px;
            background: linear-gradient(to right, transparent, #667eea, transparent);
        }
        
        .highlight-text {
            color: #667eea;
            font-weight: 600;
        }
        
        @keyframes slideInUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
    </style>
    """, unsafe_allow_html=True)

    # Hero section with animation
    st.markdown("""
    <div style='text-align: center; padding: 60px 20px; background: linear-gradient(135deg, #f5f7fa 0%, #e9ecef 100%); border-radius: 20px; margin-bottom: 40px;'>
        <div class='hero-title'>🧠 DayScore+</div>
        <div class='hero-subtitle'>Gamifying Student Well-Being with AI</div>
        <div class='hero-description'>
            Transform your daily habits into meaningful insights. Track your wellness journey, 
            <span class='highlight-text'>understand burnout risks</span>, and discover personalized 
            recovery strategies powered by AI.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Features section
    st.markdown("<h2 style='text-align: center; color: #2d3748; margin: 50px 0 30px 0;'>✨ Key Features</h2>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3, gap="medium")
    
    with col1:
        st.markdown("""
        <div class='stat-card'>
            <div class='stat-icon'>📊</div>
            <h3 style='color: #667eea; margin: 0;'>Daily Tracking</h3>
            <p style='color: #666; margin-top: 10px;'>Monitor your sleep, stress, mood, and study habits in real-time</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='stat-card'>
            <div class='stat-icon'>🤖</div>
            <h3 style='color: #667eea; margin: 0;'>AI Insights</h3>
            <p style='color: #666; margin-top: 10px;'>Get personalized recommendations powered by advanced AI</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class='stat-card'>
            <div class='stat-icon'>🏆</div>
            <h3 style='color: #667eea; margin: 0;'>Achievements</h3>
            <p style='color: #666; margin-top: 10px;'>Unlock badges and earn rewards for maintaining wellness</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    # How it works section
    st.markdown("<h2 style='text-align: center; color: #2d3748; margin: 50px 0 30px 0;'>🚀 How It Works</h2>", unsafe_allow_html=True)
    
    steps_col1, steps_col2 = st.columns(2, gap="large")
    
    with steps_col1:
        st.markdown("""
        <div style='animation: slideInLeft 1s ease-out;'>
            <div style='background: #f0f4ff; padding: 25px; border-radius: 12px; margin-bottom: 20px;'>
                <h3 style='color: #667eea; margin-top: 0;'>1️⃣ Daily Check-In</h3>
                <p style='color: #555;'>Answer simple questions about your day—sleep, stress, mood, and activities</p>
            </div>
            
            <div style='background: #f0f4ff; padding: 25px; border-radius: 12px;'>
                <h3 style='color: #667eea; margin-top: 0;'>2️⃣ Get Your Score</h3>
                <p style='color: #555;'>Receive an instant DayScore (0-100) that reflects your overall well-being</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with steps_col2:
        st.markdown("""
        <div style='animation: slideInRight 1s ease-out;'>
            <div style='background: #f0f4ff; padding: 25px; border-radius: 12px; margin-bottom: 20px;'>
                <h3 style='color: #667eea; margin-top: 0;'>3️⃣ AI Suggestions</h3>
                <p style='color: #555;'>Get personalized insights and actionable tips to improve your wellness</p>
            </div>
            
            <div style='background: #f0f4ff; padding: 25px; border-radius: 12px;'>
                <h3 style='color: #667eea; margin-top: 0;'>4️⃣ Track Progress</h3>
                <p style='color: #555;'>View trends and analytics to see how your wellness improves over time</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    # Why DayScore section
    st.markdown("""
    <div class='feature-box' style='animation: fadeInUp 1.6s ease-out;'>
        <h2 style='margin-top: 0; font-size: 2em;'>Why DayScore+?</h2>
        <div style='display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 20px; text-align: left;'>
            <div>
                <p>✅ <strong>AI-Powered</strong> - Gemini AI provides intelligent insights</p>
                <p>✅ <strong>Real-Time</strong> - Get instant feedback after each check-in</p>
            </div>
            <div>
                <p>✅ <strong>Data-Driven</strong> - Track patterns over time</p>
                <p>✅ <strong>Recovery Focus</strong> - Games and breathing exercises to combat stress</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    # CTA Section
    st.markdown("""
    <div style='text-align: center; padding: 50px 20px; animation: fadeInUp 1.8s ease-out;'>
        <h2 style='color: #2d3748; font-size: 2em; margin-top: 0;'>Ready to Optimize Your Well-Being?</h2>
        <p style='color: #666; font-size: 1.1em; margin-bottom: 30px;'>
            Start tracking your daily wellness today and unlock personalized insights!
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Button with animation
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        button_clicked = st.button("🚀 Start Daily Check-In", key="cta_btn", use_container_width=True)
        if button_clicked:
            st.switch_page("pages/checkin.py")

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    # Show latest score if available
    if db and st.session_state.user_id:
        try:
            doc = db.collection("dayscores").document(f"{st.session_state.user_id}_{date.today()}").get()
            if doc.exists:
                data = doc.to_dict()
                score = data.get('DayScore', 0)
                st.markdown(f"""
                <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; border-radius: 15px; text-align: center; animation: fadeInUp 2s ease-out;'>
                    <h3 style='margin-top: 0;'>✨ Your Today's Progress</h3>
                    <div style='font-size: 3em; font-weight: 800; margin: 20px 0;'>{score:.1f}/100</div>
                    <p style='margin: 0; opacity: 0.9;'>Keep up the great work! 💪</p>
                </div>
                """, unsafe_allow_html=True)
        except:
            pass
    
    # Footer
    st.markdown("""
    <div style='text-align: center; margin-top: 60px; color: #999; font-size: 0.9em;'>
        <p>Made with ❤️ for student wellness | DayScore+ © 2026</p>
    </div>
    """, unsafe_allow_html=True)