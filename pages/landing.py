from datetime import date
import streamlit as st
import time


def show(db):
    st.title("🏠 Landing")

    # Add robust CSS with all animations properly defined (no duplicates)
    st.markdown("""
    <style>
        @keyframes fadeInDown {
            from { opacity: 0; transform: translateY(-30px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        @keyframes fadeInUp {
            from { opacity: 0; transform: translateY(30px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        @keyframes slideInLeft {
            from { opacity: 0; transform: translateX(-50px); }
            to { opacity: 1; transform: translateX(0); }
        }
        
        @keyframes slideInRight {
            from { opacity: 0; transform: translateX(50px); }
            to { opacity: 1; transform: translateX(0); }
        }
        
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.7; }
        }
        
        @keyframes float {
            0%, 100% { transform: translateY(0px); }
            50% { transform: translateY(-10px); }
        }
        
        @keyframes slideInUp {
            from { opacity: 0; transform: translateY(30px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .hero-title {
            animation: fadeInDown 1s ease-out forwards;
            font-size: 3.5em !important;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-weight: 800;
            margin: 0 !important;
        }
        
        .hero-subtitle {
            animation: fadeInDown 1.2s ease-out 0.1s forwards;
            opacity: 0;
            font-size: 1.3em;
            color: #667eea;
            font-weight: 500;
            margin-top: 15px !important;
        }
        
        .hero-description {
            animation: fadeInUp 1.4s ease-out 0.2s forwards;
            opacity: 0;
            font-size: 1.1em;
            color: #666;
            margin-top: 20px;
            line-height: 1.6;
        }
        
        .stat-card {
            animation: slideInUp 0.8s ease-out forwards;
            opacity: 0;
            background: white;
            padding: 30px 20px;
            border-radius: 15px;
            text-align: center;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            transition: all 0.3s ease;
            border: 2px solid transparent;
            margin-bottom: 25px;
        }
        
        .stat-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 25px rgba(102, 126, 234, 0.25);
            border-color: #667eea;
        }
        
        .stat-icon {
            font-size: 3em;
            margin-bottom: 15px;
            animation: float 3s ease-in-out infinite;
            color: #667eea;
        }
        
        .feature-box {
            animation: fadeInUp 1s ease-out 0.3s forwards;
            opacity: 0;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            border-radius: 15px;
            text-align: center;
        }
        
        .step-card {
            animation: slideInUp 0.7s ease-out forwards;
            opacity: 0;
            background: #f8fafc;
            padding: 25px;
            border-radius: 15px;
            margin-bottom: 20px;
            border-left: 4px solid #667eea;
            box-shadow: 0 3px 10px rgba(0,0,0,0.08);
            transition: all 0.3s ease;
        }
        
        .step-card:hover {
            transform: translateX(5px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.2);
        }
        
        .divider {
            margin: 45px 0;
            border: 0;
            height: 3px;
            background: linear-gradient(to right, transparent, #667eea, #764ba2, transparent);
            border-radius: 3px;
        }
        
        .highlight-text {
            color: #667eea;
            font-weight: 600;
        }
        
        .score-card {
            animation: fadeInUp 1s ease-out forwards;
            opacity: 0;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 18px;
            text-align: center;
            margin: 20px 0;
        }
    </style>
    """, unsafe_allow_html=True)

    # Hero section
    st.markdown("""
    <div style='text-align: center; padding: 60px 20px; background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%); border-radius: 20px; margin-bottom: 40px;'>
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
    st.markdown("<h2 style='text-align: center; color: #1e293b; margin: 50px 0 40px 0; font-size: 2.2em;'>✨ Key Features</h2>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3, gap="medium")
    
    with col1:
        st.markdown("""
        <div class='stat-card' style='animation-delay: 0.1s;'>
            <div class='stat-icon'>📊</div>
            <h3 style='color: #4338ca; margin: 10px 0 15px 0;'>Daily Tracking</h3>
            <p style='color: #4b5563; margin: 0; line-height: 1.5;'>
                Monitor sleep, stress, mood, and study habits in real-time
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='stat-card' style='animation-delay: 0.2s;'>
            <div class='stat-icon'>🤖</div>
            <h3 style='color: #4338ca; margin: 10px 0 15px 0;'>AI Insights</h3>
            <p style='color: #4b5563; margin: 0; line-height: 1.5;'>
                Get personalized recommendations powered by advanced AI
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class='stat-card' style='animation-delay: 0.3s;'>
            <div class='stat-icon'>🏆</div>
            <h3 style='color: #4338ca; margin: 10px 0 15px 0;'>Achievements</h3>
            <p style='color: #4b5563; margin: 0; line-height: 1.5;'>
                Unlock badges and earn rewards for maintaining wellness
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    # How it works section - FIXED with reliable per-card animations
    st.markdown("<h2 style='text-align: center; color: #1e293b; margin: 50px 0 40px 0; font-size: 2.2em;'>🚀 How It Works</h2>", unsafe_allow_html=True)
    
    steps_col1, steps_col2 = st.columns(2, gap="large")
    
    with steps_col1:
        st.markdown("""
        <div class='step-card' style='animation-delay: 0.1s;'>
            <h3 style='color: #4338ca; display: flex; align-items: center; gap: 12px; margin-top: 0;'>
                <span style='background: #eef2ff; width: 36px; height: 36px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold;'>1</span>
                Daily Check-In
            </h3>
            <p style='color: #4b5563; margin: 0; line-height: 1.6;'>
                Answer simple questions about your day—sleep, stress, mood, and activities
            </p>
        </div>
        
        <div class='step-card' style='animation-delay: 0.3s;'>
            <h3 style='color: #4338ca; display: flex; align-items: center; gap: 12px; margin-top: 0;'>
                <span style='background: #eef2ff; width: 36px; height: 36px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold;'>3</span>
                AI Suggestions
            </h3>
            <p style='color: #4b5563; margin: 0; line-height: 1.6;'>
                Get personalized insights and actionable tips to improve your wellness
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with steps_col2:
        st.markdown("""
        <div class='step-card' style='animation-delay: 0.2s;'>
            <h3 style='color: #4338ca; display: flex; align-items: center; gap: 12px; margin-top: 0;'>
                <span style='background: #eef2ff; width: 36px; height: 36px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold;'>2</span>
                Get Your Score
            </h3>
            <p style='color: #4b5563; margin: 0; line-height: 1.6;'>
                Receive an instant DayScore (0-100) reflecting your overall well-being
            </p>
        </div>
        
        <div class='step-card' style='animation-delay: 0.4s;'>
            <h3 style='color: #4338ca; display: flex; align-items: center; gap: 12px; margin-top: 0;'>
                <span style='background: #eef2ff; width: 36px; height: 36px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold;'>4</span>
                Track Progress
            </h3>
            <p style='color: #4b5563; margin: 0; line-height: 1.6;'>
                View trends and analytics to see how your wellness improves over time
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    # Why DayScore section
    st.markdown("""
    <div class='feature-box'>
        <h2 style='margin-top: 0; font-size: 2em;'>Why Students Love DayScore+?</h2>
        <div style='display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 25px; margin-top: 25px; text-align: left;'>
            <div style='background: rgba(255,255,255,0.15); padding: 20px; border-radius: 12px;'>
                <p style='margin: 0; font-size: 1.05em;'>✅ <strong>AI-Powered</strong><br><span style='opacity: 0.95;'>Gemini AI provides intelligent, personalized insights</span></p>
            </div>
            <div style='background: rgba(255,255,255,0.15); padding: 20px; border-radius: 12px;'>
                <p style='margin: 0; font-size: 1.05em;'>✅ <strong>Real-Time</strong><br><span style='opacity: 0.95;'>Get instant feedback after each check-in</span></p>
            </div>
            <div style='background: rgba(255,255,255,0.15); padding: 20px; border-radius: 12px;'>
                <p style='margin: 0; font-size: 1.05em;'>✅ <strong>Data-Driven</strong><br><span style='opacity: 0.95;'>Track patterns and spot burnout risks early</span></p>
            </div>
            <div style='background: rgba(255,255,255,0.15); padding: 20px; border-radius: 12px;'>
                <p style='margin: 0; font-size: 1.05em;'>✅ <strong>Recovery Focus</strong><br><span style='opacity: 0.95;'>Guided breathing exercises & mini-games for stress relief</span></p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    # CTA Section
    st.markdown("""
    <div style='text-align: center; padding: 50px 20px;'>
        <h2 style='color: #1e293b; font-size: 2.1em; margin-top: 0; animation: fadeInUp 1s ease-out 0.2s forwards; opacity: 0;'>Ready to Optimize Your Well-Being?</h2>
        <p style='color: #4b5563; font-size: 1.15em; margin-bottom: 35px; max-width: 700px; margin-left: auto; margin-right: auto; animation: fadeInUp 1s ease-out 0.4s forwards; opacity: 0;'>
            Start tracking your daily wellness today and unlock personalized insights to thrive in your studies!
        </p>
    </div>
    """, unsafe_allow_html=True)

    # CTA Button with pulse animation
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<div style='animation: pulse 2s ease-in-out 1s infinite; margin-bottom: 15px;'></div>", unsafe_allow_html=True)
        if st.button("🚀 Start Daily Check-In", key="cta_btn", use_container_width=True, 
                     type="primary", help="Begin your wellness journey in 60 seconds"):
            st.switch_page("pages/checkin.py")

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    # Show latest score if available - with robust error handling
    if db and hasattr(st.session_state, 'user_id') and st.session_state.user_id:
        try:
            today_str = date.today().isoformat()
            doc_ref = db.collection("dayscores").document(f"{st.session_state.user_id}_{today_str}")
            doc = doc_ref.get()
            
            if doc.exists:
                data = doc.to_dict()
                score = data.get('DayScore', 0)
                st.markdown(f"""
                <div class='score-card' style='animation-delay: 0.3s;'>
                    <h3 style='margin-top: 0; font-size: 1.4em; opacity: 0.95;'>✨ Your Today's Wellness Score</h3>
                    <div style='font-size: 3.2em; font-weight: 800; margin: 20px 0; text-shadow: 0 2px 10px rgba(0,0,0,0.2);'>
                        {score:.1f}<span style='font-size: 1.2em; opacity: 0.8;'>/100</span>
                    </div>
                    <p style='margin: 0; font-size: 1.1em; opacity: 0.92;'>
                        {'Excellent balance!' if score >= 80 else 'Good effort!' if score >= 60 else 'Time for self-care 💙'}
                    </p>
                </div>
                """, unsafe_allow_html=True)
        except Exception as e:
            # Silent failure - don't show errors to users
            pass
    
    # Footer
    st.markdown("""
    <div style='text-align: center; margin-top: 50px; padding: 25px; color: #64748b; font-size: 0.95em; background: #f8fafc; border-radius: 16px;'>
        <p style='margin: 5px 0;'>Made with ❤️ for student wellness</p>
        <p style='margin: 5px 0; font-weight: 500;'>DayScore+ © 2026 • Your mental health matters</p>
    </div>
    """, unsafe_allow_html=True)

