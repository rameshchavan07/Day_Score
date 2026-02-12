import streamlit as st
import numpy as np

# ---------------------------------------
# AUDIO ENGINE
# ---------------------------------------

def generate_tone(frequency=432, duration=10, volume=0.5, sample_rate=44100):
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    tone = np.sin(2 * np.pi * frequency * t)
    audio = volume * tone
    return audio.astype(np.float32)


def generate_binaural(base_freq=432, beat_freq=6, duration=10, volume=0.5, sample_rate=44100):
    t = np.linspace(0, duration, int(sample_rate * duration), False)

    left = np.sin(2 * np.pi * base_freq * t)
    right = np.sin(2 * np.pi * (base_freq + beat_freq) * t)

    stereo = np.vstack((left, right)).T
    stereo = volume * stereo

    return stereo.astype(np.float32)


# ---------------------------------------
# AUTO FREQUENCY SELECTOR
# ---------------------------------------

def auto_frequency_selector(stress_score):
    if stress_score > 70:
        return 396, 4
    elif stress_score > 40:
        return 432, 6
    else:
        return 528, 8


# ---------------------------------------
# BREATHING ANIMATION
# ---------------------------------------

def breathing_animation():
    st.markdown("""
    <style>
    .breathing-circle {
        width: 150px;
        height: 150px;
        border-radius: 50%;
        background: radial-gradient(circle, #4facfe, #00f2fe);
        margin: 40px auto;
        animation: breathe 6s infinite ease-in-out;
    }

    @keyframes breathe {
        0% { transform: scale(0.8); opacity: 0.7; }
        50% { transform: scale(1.2); opacity: 1; }
        100% { transform: scale(0.8); opacity: 0.7; }
    }
    </style>

    <div class="breathing-circle"></div>
    <h4 style="text-align:center;">Inhale... Exhale...</h4>
    """, unsafe_allow_html=True)


# ---------------------------------------
# MAIN PAGE
# ---------------------------------------

def show(user_stress_score=50):

    st.title("🧘 DayScore Relaxation Engine")

    mode = st.radio("Choose Mode", ["Auto (AI Based)", "Manual"])

    duration = st.slider("Duration (seconds)", 5, 60, 20)
    volume = st.slider("Volume", 0.1, 1.0, 0.5)

    if mode == "Auto (AI Based)":
        st.subheader("AI Relaxation Mode")

        base_freq, beat_freq = auto_frequency_selector(user_stress_score)

        st.info(f"Stress Score: {user_stress_score}")
        st.success(f"Selected Frequency: {base_freq} Hz | Beat: {beat_freq} Hz")

        if st.button("▶ Start Relaxation"):
            audio = generate_binaural(base_freq, beat_freq, duration, volume)
            st.audio(audio, sample_rate=44100)
            breathing_animation()

    else:
        st.subheader("Manual Mode")

        base_freq = st.slider("Base Frequency (Hz)", 200, 1000, 432)
        beat_freq = st.slider("Beat Frequency (Hz)", 1, 20, 6)

        audio_type = st.radio("Audio Type", ["Single Tone", "Binaural Beats"])

        if st.button("▶ Start Relaxation"):
            if audio_type == "Single Tone":
                audio = generate_tone(base_freq, duration, volume)
            else:
                audio = generate_binaural(base_freq, beat_freq, duration, volume)

            st.audio(audio, sample_rate=44100)
            breathing_animation()
