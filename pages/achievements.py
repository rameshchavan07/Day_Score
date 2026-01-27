import streamlit as st

def show(db):
    st.title("🏆 Achievements")
    st.write("Your badges and milestones")
    # Custom CSS with white section titles and enhanced readability
    st.markdown("""
    <style>
        /* Page background */
        section.main > div {
            background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
        }
        
        /* Achievement card base */
        .achievement-card {
            background: white;
            border-radius: 16px;
            padding: 28px;
            box-shadow: 0 6px 16px rgba(0, 0, 0, 0.08);
            transition: all 0.3s ease;
            border: 1px solid #e2e8f0;
            height: 100%;
            display: flex;
            flex-direction: column;
            align-items: center;
            text-align: center;
        }
        
        .achievement-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 25px rgba(102, 126, 234, 0.15);
            border-color: #cbd5e1;
        }
        
        /* Unlocked achievement styling */
        .unlocked {
            border-top: 5px solid #4ade80;
            position: relative;
            overflow: hidden;
        }
        
        .unlocked::after {
            content: "✓ UNLOCKED";
            position: absolute;
            top: 12px;
            right: -35px;
            background: #4ade80;
            color: white;
            padding: 3px 30px;
            transform: rotate(45deg);
            font-weight: 700;
            font-size: 0.85em;
            letter-spacing: 1px;
        }
        
        .unlocked .badge {
            background: linear-gradient(135deg, #4ade80, #22c55e);
            color: white;
            box-shadow: 0 0 15px rgba(34, 197, 94, 0.4);
        }
        
        /* Locked achievement styling */
        .locked {
            border-top: 5px solid #94a3b8;
            opacity: 0.92;
            position: relative;
        }
        
        .locked::before {
            content: "🔒";
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%) scale(2.5);
            color: rgba(148, 163, 184, 0.15);
            font-size: 5rem;
            z-index: 0;
            pointer-events: none;
        }
        
        .locked .badge {
            background: #e2e8f0;
            color: #64748b;
            border: 1px dashed #94a3b8;
        }
        
        .locked .progress-text {
            color: #64748b !important;
        }
        
        /* Badge styling */
        .badge {
            width: 72px;
            height: 72px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 2.1em;
            margin-bottom: 18px;
            font-weight: bold;
            z-index: 1;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
        }
        
        /* Progress bar for locked achievements */
        .progress-container {
            width: 100%;
            background: #f1f5f9;
            border-radius: 12px;
            height: 10px;
            margin: 15px 0;
            overflow: hidden;
            z-index: 1;
        }
        
        .progress-bar {
            height: 100%;
            border-radius: 12px;
            background: linear-gradient(90deg, #667eea, #764ba2);
            width: 65%;
        }
        
        /* Header styling */
        .achievements-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 45px 25px;
            border-radius: 20px;
            color: white;
            margin-bottom: 40px;
            box-shadow: 0 10px 30px rgba(102, 126, 234, 0.25);
            text-align: center;
            position: relative;
            overflow: hidden;
        }
        
        .achievements-header::before {
            content: "";
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0) 70%);
            z-index: 0;
        }
        
        .achievements-header h1 {
            position: relative;
            z-index: 1;
            font-weight: 800;
            font-size: 3.2em;
            letter-spacing: -0.5px;
            text-shadow: 0 2px 10px rgba(0,0,0,0.2);
            margin-bottom: 8px;
        }
        
        .achievements-header p {
            position: relative;
            z-index: 1;
            font-size: 1.3em;
            opacity: 0.95;
            max-width: 700px;
            margin: 0 auto;
            font-weight: 300;
        }
        
        /* Section title - CHANGED TO WHITE WITH ENHANCED READABILITY */
        .section-title {
            text-align: center;
            color: white; /* ✅ CHANGED TO WHITE */
            font-size: 2.1em;
            margin: 50px 0 30px;
            position: relative;
            display: inline-block;
            left: 50%;
            transform: translateX(-50%);
            text-shadow: 0 2px 8px rgba(0, 0, 0, 0.15); /* Added subtle shadow for readability on light bg */
            background: rgba(0, 0, 0, 0.08); /* Slight dark tint behind text */
            padding: 8px 25px;
            border-radius: 16px;
        }
        
        .section-title::after {
            content: "";
            position: absolute;
            bottom: -12px;
            left: 50%;
            transform: translateX(-50%);
            width: 80px;
            height: 4px;
            background: linear-gradient(to right, #667eea, #764ba2, #667eea);
            border-radius: 2px;
            box-shadow: 0 2px 6px rgba(102, 126, 234, 0.4);
        }
        
        /* Info banner */
        .info-banner {
            background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
            border-left: 4px solid #3b82f6;
            border-radius: 0 12px 12px 0;
            padding: 20px;
            margin: 35px 0;
            color: #1e40af;
            font-weight: 500;
            box-shadow: 0 4px 6px rgba(59, 130, 246, 0.15);
        }
        
        /* Responsive adjustments */
        @media (max-width: 768px) {
            .achievements-header h1 {
                font-size: 2.5em;
            }
            .achievements-header p {
                font-size: 1.1em;
            }
            .badge {
                width: 60px;
                height: 60px;
                font-size: 1.8em;
            }
            .section-title {
                font-size: 1.8em;
                padding: 6px 20px;
            }
            .section-title::after {
                width: 60px;
                bottom: -10px;
            }
        }
    </style>
    """, unsafe_allow_html=True)

    # Header with enhanced visual treatment
    st.markdown("""
    <div class="achievements-header">
        <h1>🏆 Achievements</h1>
        <p>Unlock badges as you build healthier habits and improve your well-being journey</p>
    </div>
    """, unsafe_allow_html=True)

    # Unlocked Achievements Section - WHITE TEXT
    st.markdown('<div class="section-title">✨ Unlocked</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3, gap="large")
    
    with col1:
        st.markdown("""
        <div class="achievement-card unlocked">
            <div class="badge">🌅</div>
            <h3 style="margin: 10px 0 8px; color: #1e293b; font-size: 1.5em;">Early Riser</h3>
            <p style="color: #4b5563; margin: 0; line-height: 1.5;">Consistently wake up before 7 AM for 5 days</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="achievement-card unlocked">
            <div class="badge">🔥</div>
            <h3 style="margin: 10px 0 8px; color: #1e293b; font-size: 1.5em;">Active Streak</h3>
            <p style="color: #4b5563; margin: 0; line-height: 1.5;">Complete 7 consecutive days of physical activity</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="achievement-card unlocked">
            <div class="badge">📚</div>
            <h3 style="margin: 10px 0 8px; color: #1e293b; font-size: 1.5em;">Focused Mind</h3>
            <p style="color: #4b5563; margin: 0; line-height: 1.5;">Achieve 10+ hours of deep study sessions</p>
        </div>
        """, unsafe_allow_html=True)

    # Progress Section - WHITE TEXT
    st.markdown('<div class="section-title">🎯 In Progress</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        st.markdown("""
        <div class="achievement-card locked">
            <div class="badge">🌙</div>
            <h3 style="margin: 10px 0 8px; color: #334155; font-size: 1.45em; position: relative; z-index: 1;">Sleep Champion</h3>
            <p style="color: #4b5563; margin: 5px 0 15px; position: relative; z-index: 1; line-height: 1.5;">
                8+ hours of sleep for 7 consecutive days
            </p>
            <div style="position: relative; z-index: 1; width: 100%;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 8px; color: #334155; font-weight: 500;">
                    <span>65% Complete</span>
                    <span>3/7 days</span>
                </div>
                <div class="progress-container">
                    <div class="progress-bar"></div>
                </div>
                <p class="progress-text" style="font-size: 0.95em; margin-top: 8px; color: #4b5563;">
                    Keep your bedtime consistent! 🌙
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="achievement-card locked">
            <div class="badge">🧘</div>
            <h3 style="margin: 10px 0 8px; color: #334155; font-size: 1.45em; position: relative; z-index: 1;">Zen Master</h3>
            <p style="color: #4b5563; margin: 5px 0 15px; position: relative; z-index: 1; line-height: 1.5;">
                Complete 15 mindfulness sessions
            </p>
            <div style="position: relative; z-index: 1; width: 100%;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 8px; color: #334155; font-weight: 500;">
                    <span>40% Complete</span>
                    <span>6/15 sessions</span>
                </div>
                <div class="progress-container">
                    <div class="progress-bar" style="width: 40%; background: linear-gradient(90deg, #8b5cf6, #ec4899);"></div>
                </div>
                <p class="progress-text" style="font-size: 0.95em; margin-top: 8px; color: #4b5563;">
                    Try a 5-minute breathing exercise today! 💙
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Info banner
    st.markdown("""
    <div class="info-banner">
        💡 <strong>Pro Tip:</strong> Check in daily to earn points! Complete wellness challenges to unlock exclusive badges and level up your profile.
    </div>
    """, unsafe_allow_html=True)

    # Future achievements teaser - WHITE TEXT
    st.markdown('<div class="section-title" style="margin-top: 20px;">🔜 Coming Soon</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3, gap="large")
    with col1:
        st.markdown("""
        <div class="achievement-card locked" style="opacity: 0.75;">
            <div class="badge">🌟</div>
            <h3 style="margin: 10px 0 8px; color: #334155; font-size: 1.4em; position: relative; z-index: 1;">Wellness Guru</h3>
            <p style="color: #4b5563; margin: 0; position: relative; z-index: 1; line-height: 1.5;">Maintain 90+ DayScore for 14 days</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="achievement-card locked" style="opacity: 0.75;">
            <div class="badge">🌱</div>
            <h3 style="margin: 10px 0 8px; color: #334155; font-size: 1.4em; position: relative; z-index: 1;">Growth Mindset</h3>
            <p style="color: #4b5563; margin: 0; position: relative; z-index: 1; line-height: 1.5;">Complete all recovery challenges</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="achievement-card locked" style="opacity: 0.75;">
            <div class="badge">👑</div>
            <h3 style="margin: 10px 0 8px; color: #334155; font-size: 1.4em; position: relative; z-index: 1;">DayScore Legend</h3>
            <p style="color: #4b5563; margin: 0; position: relative; z-index: 1; line-height: 1.5;">Reach 10,000 total wellness points</p>
        </div>
        """, unsafe_allow_html=True)

    # Footer note
    st.markdown("""
    <div style="text-align: center; margin-top: 40px; padding: 20px; color: #64748b; font-size: 0.95em;">
        <p>Your achievements sync across all devices • New badges added monthly</p>
    </div>
    """, unsafe_allow_html=True)