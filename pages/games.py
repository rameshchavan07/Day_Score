import streamlit as st

import streamlit as st

def show(db):
    st.title("🎮 Games")

    """
    LEVEL 4: Games & Breathing Experience
    Relaxation-focused pages for stress relief
    """
    # Custom CSS with dark theme and animations
    st.markdown("""
    <style>
        /* Dark background */
        .main {
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
            color: #ffffff;
        }
        
        /* Header styling */
        .games-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 50px 30px;
            border-radius: 20px;
            color: white;
            margin-bottom: 40px;
            box-shadow: 0 15px 40px rgba(102, 126, 234, 0.35);
            text-align: center;
            position: relative;
            overflow: hidden;
        }
        
        .games-header::before {
            content: "";
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0) 70%);
            z-index: 0;
        }
        
        .games-header h1 {
            position: relative;
            z-index: 1;
            font-weight: 800;
            font-size: 3.2em;
            margin: 0;
            text-shadow: 0 2px 10px rgba(0,0,0,0.3);
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 20px;
        }
        
        .games-header p {
            position: relative;
            z-index: 1;
            font-size: 1.4em;
            opacity: 0.95;
            margin-top: 15px;
            font-weight: 300;
        }
        
        /* Tab styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 15px;
            background: rgba(30, 41, 59, 0.6);
            padding: 15px;
            border-radius: 16px;
            border: 1px solid rgba(100, 116, 139, 0.3);
        }
        
        .stTabs [data-baseweb="tab"] {
            height: 50px;
            background: rgba(56, 70, 89, 0.4);
            border-radius: 12px;
            color: #cbd5e1;
            font-weight: 600;
            font-size: 1.1em;
            padding: 0 25px;
            transition: all 0.3s ease;
            border: 2px solid transparent;
        }
        
        .stTabs [data-baseweb="tab"]:hover {
            background: rgba(102, 126, 234, 0.2);
            color: white;
        }
        
        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white !important;
            border-color: #667eea;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        }
        
        /* Game card styling */
        .game-card {
            background: rgba(30, 41, 59, 0.7);
            border-radius: 18px;
            padding: 30px;
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.4);
            transition: all 0.4s ease;
            border: 1px solid rgba(100, 116, 139, 0.3);
            height: 100%;
            display: flex;
            flex-direction: column;
        }
        
        .game-card:hover {
            transform: translateY(-8px);
            box-shadow: 0 15px 40px rgba(102, 126, 234, 0.25);
            border-color: rgba(102, 126, 234, 0.5);
            background: rgba(30, 41, 59, 0.85);
        }
        
        .game-card.puzzle {
            border-top: 5px solid #667eea;
        }
        
        .game-card.cozy {
            border-top: 5px solid #f59e0b;
        }
        
        .game-card.focus {
            border-top: 5px solid #10b981;
        }
        
        .game-icon {
            font-size: 3.5em;
            margin-bottom: 20px;
            display: flex;
            justify-content: center;
        }
        
        .game-title {
            font-size: 1.6em;
            font-weight: 700;
            color: white;
            margin: 0 0 15px 0;
            text-align: center;
        }
        
        .game-desc {
            font-size: 1.1em;
            color: #94a3b8;
            text-align: center;
            line-height: 1.6;
            margin-bottom: 25px;
            flex-grow: 1;
        }
        
        /* Button styling */
        .stButton > button {
            width: 100%;
            padding: 14px 25px;
            border-radius: 12px;
            font-weight: 600;
            font-size: 1.05em;
            transition: all 0.3s ease;
            border: none;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
        }
        
        .stButton > button:active {
            transform: translateY(1px);
        }
        
        /* Coming soon banner */
        .coming-soon {
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.15) 0%, rgba(118, 75, 162, 0.15) 100%);
            border-left: 4px solid #667eea;
            border-radius: 0 12px 12px 0;
            padding: 25px;
            margin: 40px 0;
            color: #cbd5e1;
            font-size: 1.1em;
            font-weight: 500;
            text-align: center;
        }
        
        /* Section divider */
        .section-divider {
            height: 2px;
            background: linear-gradient(to right, transparent, rgba(102, 126, 234, 0.5), transparent);
            margin: 50px 0;
            border-radius: 2px;
        }
        
        /* Responsive adjustments */
        @media (max-width: 768px) {
            .games-header h1 {
                font-size: 2.4em;
            }
            .games-header p {
                font-size: 1.15em;
            }
            .stTabs [data-baseweb="tab"] {
                font-size: 0.95em;
                padding: 0 15px;
            }
            .game-icon {
                font-size: 2.8em;
            }
            .game-title {
                font-size: 1.4em;
            }
            .game-desc {
                font-size: 1em;
            }
        }
    </style>
    """, unsafe_allow_html=True)

    # Header
    st.markdown("""
    <div class="games-header">
        <h1>🎮 Relaxing Games</h1>
        <p>Take a break and play calming games to reduce stress</p>
    </div>
    """, unsafe_allow_html=True)

    # Coming soon banner
    st.markdown("""
    <div class="coming-soon">
        🎮 <strong>Featured Games</strong> - Interactive experiences coming soon! Stay tuned for updates.
    </div>
    """, unsafe_allow_html=True)

    # Game categories tabs
    tab1, tab2, tab3 = st.tabs(["🧩 Puzzles", "🎨 Cozy Games", "🎯 Focus Games"])

    with tab1:
        st.markdown('<div style="color: #cbd5e1; font-size: 1.3em; margin-bottom: 30px;">🧩 Relaxing puzzle games to help you unwind and de-stress</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2, gap="large")
        
        with col1:
            st.markdown("""
            <div class="game-card puzzle">
                <div class="game-icon">🧩</div>
                <h3 class="game-title">Zen Puzzles</h3>
                <p class="game-desc">Meditative puzzle experience with soothing visuals and calming music. Perfect for unwinding after study sessions.</p>
            </div>
            """, unsafe_allow_html=True)
            st.button("Play Now", key="zen_puzzles", use_container_width=True, type="primary")
        
        with col2:
            st.markdown("""
            <div class="game-card puzzle">
                <div class="game-icon">🌈</div>
                <h3 class="game-title">Color Match</h3>
                <p class="game-desc">Peaceful color matching game that helps improve focus while keeping your mind relaxed. Beautiful gradients and smooth animations.</p>
            </div>
            """, unsafe_allow_html=True)
            st.button("Play Now", key="color_match", use_container_width=True, type="primary")

    with tab2:
        st.markdown('<div style="color: #cbd5e1; font-size: 1.3em; margin-bottom: 30px;">🎨 Comfortable, low-pressure gaming experiences for ultimate relaxation</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2, gap="large")
        
        with col1:
            st.markdown("""
            <div class="game-card cozy">
                <div class="game-icon">🌸</div>
                <h3 class="game-title">Garden Sim</h3>
                <p class="game-desc">Grow your virtual garden at your own pace. Plant flowers, tend to plants, and create your peaceful sanctuary. No time limits or pressure.</p>
            </div>
            """, unsafe_allow_html=True)
            st.button("Play Now", key="garden_sim", use_container_width=True, type="primary")
        
        with col2:
            st.markdown("""
            <div class="game-card cozy">
                <div class="game-icon">☕</div>
                <h3 class="game-title">Café Manager</h3>
                <p class="game-desc">Run a cozy virtual café where you can serve customers, decorate your space, and create the perfect relaxing atmosphere. Stress-free gameplay.</p>
            </div>
            """, unsafe_allow_html=True)
            st.button("Play Now", key="cafe_manager", use_container_width=True, type="primary")

    with tab3:
        st.markdown('<div style="color: #cbd5e1; font-size: 1.3em; margin-bottom: 30px;">🎯 Games designed to improve concentration and mental clarity</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2, gap="large")
        
        with col1:
            st.markdown("""
            <div class="game-card focus">
                <div class="game-icon">🧠</div>
                <h3 class="game-title">Memory Master</h3>
                <p class="game-desc">Enhance your memory skills with progressively challenging levels. Track your improvement over time and unlock new brain-training exercises.</p>
            </div>
            """, unsafe_allow_html=True)
            st.button("Play Now", key="memory_master", use_container_width=True, type="primary")
        
        with col2:
            st.markdown("""
            <div class="game-card focus">
                <div class="game-icon">🎯</div>
                <h3 class="game-title">Focus Quest</h3>
                <p class="game-desc">Improve concentration and focus through engaging mini-games. Perfect for study breaks or building mental stamina before exams.</p>
            </div>
            """, unsafe_allow_html=True)
            st.button("Play Now", key="focus_quest", use_container_width=True, type="primary")

    # Divider
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    # Final info banner
    st.markdown("""
    <div class="coming-soon" style="background: linear-gradient(135deg, rgba(16, 185, 129, 0.15) 0%, rgba(5, 150, 105, 0.15) 100%); border-left-color: #10b981;">
        💡 <strong>Pro Tip:</strong> Take 5-minute game breaks between study sessions to refresh your mind and improve productivity!
    </div>
    """, unsafe_allow_html=True)

    # Footer
    st.markdown("""
    <div style="text-align: center; margin-top: 40px; padding: 25px; color: #64748b; font-size: 0.95em;">
        <p>Games update monthly • Designed for student wellness • Zero ads, zero pressure</p>
    </div>
    """, unsafe_allow_html=True)