import streamlit as st
import numpy as np
import time
import matplotlib.pyplot as plt
import io
import wave

# Reduced sample rate to avoid WAV format issues
SAMPLE_RATE = 22050  # Changed from 44100 to 22050

# ---------------------------------------
# AUDIO SAFETY
# ---------------------------------------

def safe_audio(audio):
    """Normalize + clip audio safely for Streamlit"""
    max_val = np.max(np.abs(audio))
    if max_val > 1:
        audio = audio / max_val

    audio = np.clip(audio, -1, 1)
    return audio.astype(np.float32)


# ---------------------------------------
# AUDIO EFFECTS
# ---------------------------------------

def apply_fade(audio, fade_duration=2):
    fade_samples = int(SAMPLE_RATE * fade_duration)

    if fade_samples > len(audio):
        fade_samples = len(audio) // 2

    fade_in = np.linspace(0, 1, fade_samples)
    fade_out = np.linspace(1, 0, fade_samples)

    audio[:fade_samples] *= fade_in
    audio[-fade_samples:] *= fade_out

    return audio


def add_sleep_mode(audio):
    fade_curve = np.linspace(1, 0.1, len(audio))
    return audio * fade_curve


# ---------------------------------------
# SOUND GENERATORS
# ---------------------------------------

def generate_binaural(base_freq, beat_freq, duration, volume):
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), False)

    left = np.sin(2 * np.pi * base_freq * t)
    right = np.sin(2 * np.pi * (base_freq + beat_freq) * t)

    stereo = np.vstack((left, right)).T
    stereo *= volume

    return stereo


def generate_rain_noise(duration, volume=0.1):
    noise = np.random.normal(0, 1, int(SAMPLE_RATE * duration))
    # Apply low-pass filter to make it sound more like rain
    b = np.ones(100)/100  # Simple moving average
    rain_filtered = np.convolve(noise, b, mode='same')
    return rain_filtered * volume


def generate_ocean_wave(duration, volume=0.1):
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), False)
    # Create a more realistic ocean sound with multiple frequencies
    wave = np.sin(2 * np.pi * 0.2 * t) + 0.5*np.sin(2 * np.pi * 0.1 * t)
    # Add some randomness to simulate waves
    noise = np.random.normal(0.5, 0.2, len(t))
    return (wave * noise) * volume


def generate_white_noise(duration, volume=0.1):
    noise = np.random.normal(0, 1, int(SAMPLE_RATE * duration))
    return noise * volume


def generate_pink_noise(duration, volume=0.1):
    # Pink noise generation using Voss-McCartney algorithm
    noise = np.random.normal(0, 1, int(SAMPLE_RATE * duration))
    # Apply simple pink noise filter
    b = [0.99765, -0.99531]
    a = [1, -1.99531, 0.99531]
    pink = np.convolve(noise, np.polyval(b, np.arange(len(b))), mode='same')
    return pink * volume


# ---------------------------------------
# VISUALIZER
# ---------------------------------------

def waveform_visualizer(audio):
    fig, ax = plt.subplots()
    ax.plot(audio[:3000])
    ax.set_title("Waveform Preview")
    ax.set_xlabel("Samples")
    ax.set_ylabel("Amplitude")
    st.pyplot(fig)


def spectrum_visualizer(audio):
    # Compute FFT for frequency analysis
    fft = np.fft.fft(audio[:4096])  # Use first 4096 samples
    freqs = np.fft.fftfreq(len(fft), 1/SAMPLE_RATE)
    magnitude = np.abs(fft)
    
    fig, ax = plt.subplots()
    ax.plot(freqs[:len(freqs)//2], magnitude[:len(magnitude)//2])
    ax.set_title("Frequency Spectrum")
    ax.set_xlabel("Frequency (Hz)")
    ax.set_ylabel("Magnitude")
    ax.set_xlim(0, 1000)  # Focus on audible range
    st.pyplot(fig)


# ---------------------------------------
# COUNTDOWN TIMER (Non-blocking style)
# ---------------------------------------

def countdown_timer(duration):
    placeholder = st.empty()
    for i in range(duration, 0, -1):
        placeholder.markdown(f"### ⏳ Time Remaining: {i} sec")
        time.sleep(1)
    placeholder.markdown("### 🌙 Session Complete")


# ---------------------------------------
# BREATHING ANIMATION
# ---------------------------------------

def breathing_animation():
    st.markdown("""
    <style>
    .breathing-circle {
        width: 160px;
        height: 160px;
        border-radius: 50%;
        background: radial-gradient(circle, #667eea, #764ba2);
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

    st.title("🧘 DayScore Relaxation Engine PRO")

    duration = st.slider("Duration (seconds)", 5, 60, 20)
    volume = st.slider("Volume", 0.1, 1.0, 0.5)

    # Choose between binaural beats or pure tones
    sound_type = st.radio("Sound Type", ("Binaural Beats", "Pure Tones"))
    
    if sound_type == "Binaural Beats":
        base_freq = st.slider("Base Frequency (Hz)", 200, 1000, 432)
        beat_freq = st.slider("Beat Frequency (Hz)", 1, 20, 6)
    else:
        base_freq = st.slider("Frequency (Hz)", 100, 1000, 432)
        beat_freq = 0  # No beat frequency for pure tones

    background = st.selectbox("Background Sound", ["None", "Rain", "Ocean", "White Noise", "Pink Noise"])
    sleep_mode = st.checkbox("💤 Sleep Mode (Gradual Fade)")
    show_wave = st.checkbox("📊 Show Waveform")
    show_spectrum = st.checkbox("🎵 Show Frequency Spectrum")

    if st.button("▶ Start Relaxation"):

        # Generate main audio
        if sound_type == "Binaural Beats":
            audio = generate_binaural(base_freq, beat_freq, duration, volume)
        else:
            t = np.linspace(0, duration, int(SAMPLE_RATE * duration), False)
            mono = np.sin(2 * np.pi * base_freq * t)
            audio = np.vstack((mono, mono)).T  # Same signal for both channels
            audio *= volume

        # Background mixing (safe weighted mixing)
        if background == "Rain":
            rain = generate_rain_noise(duration)
            audio[:, 0] = (audio[:, 0] * 0.8) + (rain * 0.2)
            audio[:, 1] = (audio[:, 1] * 0.8) + (rain * 0.2)

        elif background == "Ocean":
            ocean = generate_ocean_wave(duration)
            audio[:, 0] = (audio[:, 0] * 0.8) + (ocean * 0.2)
            audio[:, 1] = (audio[:, 1] * 0.8) + (ocean * 0.2)
            
        elif background == "White Noise":
            white = generate_white_noise(duration)
            audio[:, 0] = (audio[:, 0] * 0.7) + (white * 0.3)
            audio[:, 1] = (audio[:, 1] * 0.7) + (white * 0.3)
            
        elif background == "Pink Noise":
            pink = generate_pink_noise(duration)
            audio[:, 0] = (audio[:, 0] * 0.7) + (pink * 0.3)
            audio[:, 1] = (audio[:, 1] * 0.7) + (pink * 0.3)

        # Sleep mode
        if sleep_mode:
            audio[:, 0] = add_sleep_mode(audio[:, 0])
            audio[:, 1] = add_sleep_mode(audio[:, 1])

        # Fade in/out
        audio[:, 0] = apply_fade(audio[:, 0])
        audio[:, 1] = apply_fade(audio[:, 1])

        # FINAL SAFETY FIX (Prevents your crash)
        audio = safe_audio(audio)

        # Convert to bytes for Streamlit compatibility
        import io
        import wave
        
        # Ensure audio is in correct shape and type
        audio = audio.T  # Transpose to (channels, samples)
        
        # Create WAV file in memory
        buffer = io.BytesIO()
        with wave.open(buffer, 'wb') as wav_file:
            wav_file.setnchannels(2)  # Stereo
            wav_file.setsampwidth(2)  # 16-bit
            wav_file.setframerate(SAMPLE_RATE)
            
            # Convert to 16-bit integers
            audio_scaled = (audio * 32767).astype(np.int16)
            
            # Write frames
            wav_file.writeframes(audio_scaled.tobytes())
        
        buffer.seek(0)
        st.audio(buffer, format='audio/wav')

        breathing_animation()

        if show_wave:
            waveform_visualizer(audio[0, :])  # Pass left channel

        if show_spectrum:
            spectrum_visualizer(audio[0, :])  # Pass left channel

        countdown_timer(duration)

if __name__ == "__main__":
    show()