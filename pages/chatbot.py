import streamlit as st
from datetime import datetime
import os
from google import genai


# ----------------------------------------
# CONFIG (NEW GOOGLE.GENAI STYLE)
# ----------------------------------------

# Option 1 (Recommended): Use Streamlit secrets
# Add in: .streamlit/secrets.toml
# GEMINI_API_KEY="your_api_key_here"
try:
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
except:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Gemini client
client = genai.Client(api_key=GEMINI_API_KEY)

# Use model from your list
MODEL_NAME = "models/gemini-2.5-flash"


# ----------------------------------------
# FIREBASE SAVE + LOAD
# ----------------------------------------
def load_chat_history(db, user_id):
    try:
        doc_ref = db.collection("chat_history").document(user_id)
        doc = doc_ref.get()

        if doc.exists:
            data = doc.to_dict()
            return data.get("messages", [])
        return []
    except:
        return []


def save_chat_history(db, user_id, messages):
    try:
        db.collection("chat_history").document(user_id).set({
            "user_id": user_id,
            "messages": messages,
            "updated_at": datetime.utcnow().isoformat()
        })
    except:
        pass


# ----------------------------------------
# MAIN PAGE
# ----------------------------------------
def show(db):
    st.title("💬 HealthBot")
    st.caption("⚠️ This chatbot gives wellness guidance only. Not medical advice.")

    # -----------------------------
    # PREMIUM THEME CSS (MATCH LANDING)
    # -----------------------------
    st.markdown("""
    <style>
        @keyframes fadeInUp {
            from { opacity: 0; transform: translateY(15px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .chat-hero {
            text-align: center;
            padding: 40px 20px;
            border-radius: 20px;
            background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
            margin-bottom: 25px;
            animation: fadeInUp 0.7s ease-out forwards;
        }

        .chat-title {
            font-size: 2.6em;
            font-weight: 800;
            margin: 0;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }

        .chat-subtitle {
            font-size: 1.1em;
            margin-top: 10px;
            color: #475569;
        }

        .quick-card {
            background: white;
            padding: 18px;
            border-radius: 16px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.08);
            border: 2px solid transparent;
            transition: 0.3s;
            animation: fadeInUp 0.7s ease-out forwards;
        }

        .quick-card:hover {
            transform: translateY(-3px);
            border-color: #667eea;
            box-shadow: 0 8px 25px rgba(102, 126, 234, 0.18);
        }

        .divider {
            margin: 25px 0;
            border: 0;
            height: 3px;
            background: linear-gradient(to right, transparent, #667eea, #764ba2, transparent);
            border-radius: 3px;
        }

        /* Chat message bubbles */
        .user-bubble {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 14px 16px;
            border-radius: 18px;
            margin: 8px 0;
            max-width: 85%;
            margin-left: auto;
            box-shadow: 0 5px 18px rgba(102, 126, 234, 0.25);
        }

        .bot-bubble {
            background: white;
            color: #111827;
            padding: 14px 16px;
            border-radius: 18px;
            margin: 8px 0;
            max-width: 85%;
            margin-right: auto;
            box-shadow: 0 5px 18px rgba(0,0,0,0.08);
            border: 1px solid #eef2ff;
        }

        .bot-label {
            font-weight: 700;
            color: #4338ca;
        }

        .user-label {
            font-weight: 700;
            color: white;
        }
    </style>
    """, unsafe_allow_html=True)

    # -----------------------------
    # HERO
    # -----------------------------
    st.markdown("""
    <div class="chat-hero">
        <div class="chat-title">🤖 HealthBot</div>
        <div class="chat-subtitle">
            Ask about <b>sleep</b>, <b>stress</b>, <b>diet</b>, <b>workout</b> — get AI wellness guidance instantly ✨
        </div>
    </div>
    """, unsafe_allow_html=True)

    # -----------------------------
    # USER CHECK
    # -----------------------------
    if not st.session_state.get("user_id"):
        st.warning("⚠️ Please login first to use the chatbot.")
        return

    user_id = st.session_state.user_id

    # -----------------------------
    # INIT CHAT HISTORY (LOAD FROM FIREBASE)
    # -----------------------------
    if "healthbot_messages" not in st.session_state:
        st.session_state.healthbot_messages = load_chat_history(db, user_id)

        # If empty -> add greeting
        if len(st.session_state.healthbot_messages) == 0:
            st.session_state.healthbot_messages = [
                {"role": "assistant", "content": "Hi 👋 I’m HealthBot! What would you like help with today? 😄"}
            ]
            save_chat_history(db, user_id, st.session_state.healthbot_messages)

    # -----------------------------
    # QUICK BUTTONS
    # -----------------------------
    st.markdown("<hr class='divider'>", unsafe_allow_html=True)
    st.subheader("⚡ Quick Help")

    q1, q2, q3, q4 = st.columns(4)

    def quick_prompt(topic):
        if topic == "Sleep":
            return "Give me tips to improve my sleep schedule as a student."
        if topic == "Stress":
            return "I feel stressed. Give me a 2-minute calming plan."
        if topic == "Diet":
            return "Suggest a healthy student diet plan (simple + budget friendly)."
        if topic == "Workout":
            return "Suggest a simple 15-minute daily workout for beginners."
        return "Give me wellness tips."

    quick_clicked = None

    with q1:
        if st.button("😴 Sleep", use_container_width=True):
            quick_clicked = quick_prompt("Sleep")

    with q2:
        if st.button("😰 Stress", use_container_width=True):
            quick_clicked = quick_prompt("Stress")

    with q3:
        if st.button("🥗 Diet", use_container_width=True):
            quick_clicked = quick_prompt("Diet")

    with q4:
        if st.button("🏋️ Workout", use_container_width=True):
            quick_clicked = quick_prompt("Workout")

    # -----------------------------
    # SHOW CHAT HISTORY
    # -----------------------------
    st.markdown("<hr class='divider'>", unsafe_allow_html=True)
    st.subheader("💬 Chat")

    for msg in st.session_state.healthbot_messages:
        if msg["role"] == "user":
            st.markdown(f"""
                <div class="user-bubble">
                    <div class="user-label">You</div>
                    {msg["content"]}
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
                <div class="bot-bubble">
                    <div class="bot-label">HealthBot</div>
                    {msg["content"]}
                </div>
            """, unsafe_allow_html=True)

    # -----------------------------
    # USER INPUT
    # -----------------------------
    user_input = st.chat_input("Ask about sleep, stress, diet, workout...")

    # If quick button clicked -> treat as user input
    if quick_clicked:
        user_input = quick_clicked

    if user_input:
        # Add user msg
        st.session_state.healthbot_messages.append({"role": "user", "content": user_input})
        save_chat_history(db, user_id, st.session_state.healthbot_messages)

        # Gemini prompt
        prompt = f"""
You are HealthBot inside a student wellness app called DayScore+.

Rules:
- Give safe general wellness guidance.
- No medical diagnosis.
- If emergency -> tell user to consult doctor immediately.
- Keep response structured: bullet points + short steps.
- Be friendly and motivating.

User message: {user_input}
"""

        with st.spinner("🤖 Thinking..."):
            try:
                response = client.models.generate_content(
                    model=MODEL_NAME,
                    contents=prompt
                )
                bot_reply = response.text
            except Exception as e:
                bot_reply = f"⚠️ Sorry, I couldn't respond right now. Please try again.\n\nError: {e}"

        # Add assistant msg
        st.session_state.healthbot_messages.append({"role": "assistant", "content": bot_reply})
        save_chat_history(db, user_id, st.session_state.healthbot_messages)

        st.rerun()

    # -----------------------------
    # CLEAR CHAT BUTTON
    # -----------------------------
    st.markdown("<hr class='divider'>", unsafe_allow_html=True)

    colA, colB = st.columns([2, 1])
    with colB:
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.healthbot_messages = [
                {"role": "assistant", "content": "Chat cleared 😄 Ask me anything again!"}
            ]
            save_chat_history(db, user_id, st.session_state.healthbot_messages)
            st.rerun()
