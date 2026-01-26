import streamlit as st
import time

def show(db):
    """
    LEVEL 4: Breathing Exercise Experience
    Guided breathing exercises for stress reduction
    """
    st.markdown("""
    <style>
        @keyframes breathe {
            0% {
                transform: scale(0.8);
                opacity: 0.5;
            }
            50% {
                transform: scale(1.2);
                opacity: 1;
            }
            100% {
                transform: scale(0.8);
                opacity: 0.5;
            }
        }
        
        .breathing-circle {
            width: 300px;
            height: 300px;
            margin: 50px auto;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 4em;
            font-weight: bold;
            animation: breathe 8s infinite;
            box-shadow: 0 10px 40px rgba(102, 126, 234, 0.3);
        }
    </style>
    
    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 40px 20px; border-radius: 10px; color: white; margin-bottom: 30px; text-align: center;'>
        <h1 style='margin: 0; color: white;'>🌬️ Breathing Exercises</h1>
        <p style='margin-top: 10px; opacity: 0.9;'>Guided exercises to calm your mind and reduce stress</p>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("Choose Your Exercise")
    
    exercise_type = st.radio(
        "Select breathing pattern:",
        ["🌊 4-7-8 Relaxation", "📿 Box Breathing", "🧘 Extended Exhale", "💤 Sleep Prep"]
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        duration = st.slider("Duration (minutes)", 1, 10, 5)
    
    with col2:
        background_music = st.checkbox("Background Music", value=True)
    
    st.markdown("---")
    
    if st.button("🎯 Start Exercise", use_container_width=True):
        st.markdown("""
        <div class='breathing-circle'>
            🌬️
        </div>
        """, unsafe_allow_html=True)
        
        if exercise_type == "🌊 4-7-8 Relaxation":
            st.write("### 4-7-8 Breathing Pattern")
            st.write("Follow this calming technique:")
            st.write("1. **Inhale** for 4 counts")
            st.write("2. **Hold** for 7 counts")
            st.write("3. **Exhale** for 8 counts")
            st.info(f"⏱️ Session: {duration} minutes | Music: {'On' if background_music else 'Off'}")
        
        elif exercise_type == "📿 Box Breathing":
            st.write("### Box Breathing Pattern")
            st.write("A balanced technique used by athletes:")
            st.write("1. **Inhale** for 4 counts")
            st.write("2. **Hold** for 4 counts")
            st.write("3. **Exhale** for 4 counts")
            st.write("4. **Hold** for 4 counts")
            st.info(f"⏱️ Session: {duration} minutes | Music: {'On' if background_music else 'Off'}")
        
        elif exercise_type == "🧘 Extended Exhale":
            st.write("### Extended Exhale Pattern")
            st.write("Activate your parasympathetic nervous system:")
            st.write("1. **Inhale** for 4 counts")
            st.write("2. **Exhale** for 8 counts (twice as long)")
            st.info(f"⏱️ Session: {duration} minutes | Music: {'On' if background_music else 'Off'}")
        
        else:  # Sleep Prep
            st.write("### Sleep Preparation Pattern")
            st.write("Prepare your body for restful sleep:")
            st.write("1. **Inhale** for 4 counts")
            st.write("2. **Hold** for 4 counts")
            st.write("3. **Exhale** for 6 counts")
            st.info(f"⏱️ Session: {duration} minutes | Music: {'On' if background_music else 'Off'}")
        
        st.success(f"✅ Breathing exercise completed! Feel more relaxed? Come back anytime.")
    
    st.markdown("---")
    
    st.subheader("💡 Tips for Effective Breathing")
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("✓ Find a quiet, comfortable place")
        st.write("✓ Sit or lie down in a relaxed position")
        st.write("✓ Close your eyes if comfortable")
    
    with col2:
        st.write("✓ Breathe through your nose")
        st.write("✓ Practice regularly for best results")
        st.write("✓ Don't force your breath")
