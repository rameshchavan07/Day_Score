import streamlit as st

def show(db):
    """
    LEVEL 4: Games & Breathing Experience
    Relaxation-focused pages for stress relief
    """
    st.markdown("""
    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 40px 20px; border-radius: 10px; color: white; margin-bottom: 30px;'>
        <h1 style='margin: 0; color: white;'>🎮 Relaxing Games</h1>
        <p style='margin-top: 10px; opacity: 0.9;'>Take a break and play calming games to reduce stress</p>
    </div>
    """, unsafe_allow_html=True)

    st.info("🎮 Featured Games Coming Soon")
    
    # Game categories
    tab1, tab2, tab3 = st.tabs(["🧩 Puzzles", "🎨 Cozy Games", "🎯 Focus Games"])
    
    with tab1:
        st.subheader("Calm Puzzles")
        st.write("Relaxing puzzle games to help you unwind")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            <div style='background: #f0f4ff; padding: 20px; border-radius: 10px;'>
                <h3>🧩 Zen Puzzles</h3>
                <p>Meditative puzzle experience</p>
                <button style='background: #667eea; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer;'>Play Now</button>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style='background: #f0f4ff; padding: 20px; border-radius: 10px;'>
                <h3>🌈 Color Match</h3>
                <p>Peaceful color matching game</p>
                <button style='background: #667eea; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer;'>Play Now</button>
            </div>
            """, unsafe_allow_html=True)
    
    with tab2:
        st.subheader("Cozy Games")
        st.write("Comfortable, low-pressure gaming experiences")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            <div style='background: #fff0f5; padding: 20px; border-radius: 10px;'>
                <h3>🌸 Garden Sim</h3>
                <p>Grow your virtual garden</p>
                <button style='background: #764ba2; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer;'>Play Now</button>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style='background: #fff0f5; padding: 20px; border-radius: 10px;'>
                <h3>☕ Café Manager</h3>
                <p>Run a cozy virtual café</p>
                <button style='background: #764ba2; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer;'>Play Now</button>
            </div>
            """, unsafe_allow_html=True)
    
    with tab3:
        st.subheader("Focus Games")
        st.write("Games to improve concentration and mental clarity")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            <div style='background: #f0fff0; padding: 20px; border-radius: 10px;'>
                <h3>🧠 Memory Master</h3>
                <p>Enhance your memory skills</p>
                <button style='background: #28a745; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer;'>Play Now</button>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style='background: #f0fff0; padding: 20px; border-radius: 10px;'>
                <h3>🎯 Focus Quest</h3>
                <p>Improve concentration and focus</p>
                <button style='background: #28a745; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer;'>Play Now</button>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.info("💡 Games are coming soon! Check back later for interactive experiences.")
