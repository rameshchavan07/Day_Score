import os

# Try to import Gemini API
genai = None
USING_GENAI = False

try:
    import google.generativeai as genai
    USING_GENAI = True
except ImportError:
    # Fallback: API not available
    pass

# Initialize Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyAl2EIGoXJ17AbMTCW898luI6DA9nobVOk")

if USING_GENAI and GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)


def get_ai_suggestion(score, stress, mood, sleep_hours, study_hours, screen_time):
    """
    Get personalized AI suggestions based on DayScore.
    Falls back to hardcoded suggestions if API unavailable.
    """
    if not USING_GENAI or not GEMINI_API_KEY:
        return get_fallback_suggestion(
            score, stress, mood, sleep_hours, study_hours, screen_time
        )

    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(
            _build_prompt(score, stress, mood, sleep_hours, study_hours, screen_time)
        )
        return response.text

    except Exception as e:
        print(f"Gemini API error: {e}")
        return get_fallback_suggestion(
            score, stress, mood, sleep_hours, study_hours, screen_time
        )


def _build_prompt(score, stress, mood, sleep_hours, study_hours, screen_time):
    """Build the prompt for Gemini"""
    return f"""
You are a wellness coach AI helping a student understand their daily well-being score.

Today's Data:
- DayScore: {score}/100
- Stress Level: {stress}/10
- Mood: {mood}/10
- Sleep Hours: {sleep_hours}
- Study Hours: {study_hours}
- Screen Time: {screen_time} hours

Tasks:
1. Explain why the score is high/moderate/low
2. Mention one strong habit
3. Suggest one improvement area
4. Give 2–3 actionable tips
5. End with one encouraging emoji

Keep the response short, friendly, and supportive.
"""


def get_fallback_suggestion(score, stress, mood, sleep_hours, study_hours, screen_time):
    """Fallback suggestions when API is unavailable"""

    suggestions = []

    if score >= 80:
        suggestions.append(
            f"🌟 Excellent work! Your balance looks great with {sleep_hours}h of sleep."
        )
    elif score >= 60:
        suggestions.append(
            f"👍 Good effort! Your mood ({mood}/10) is decent—more rest could help."
        )
    else:
        suggestions.append(
            f"💪 Recovery needed. Stress is high ({stress}/10); focus on rest today."
        )

    if stress >= 7:
        suggestions.append("🌬️ Try deep breathing: inhale 4s, hold 4s, exhale 6s.")
    if sleep_hours < 7:
        suggestions.append("😴 Aim for 7–9 hours of sleep tonight.")
    if screen_time > 6:
        suggestions.append("📱 Reduce screen time by at least 1 hour tomorrow.")
    if study_hours > 8:
        suggestions.append("📚 Break study sessions with short walks or stretches.")

    suggestions.append("✨ Keep tracking daily—you’re building healthy habits!")

    return "\n\n".join(suggestions)


def get_burnout_risk(stress, sleep_hours, screen_time, study_hours):
    """
    Assess burnout risk level
    Returns: (risk_level, recommendation)
    """

    risk_score = 0

    if stress >= 8:
        risk_score += 3
    elif stress >= 6:
        risk_score += 2
    elif stress >= 5:
        risk_score += 1

    if sleep_hours < 6:
        risk_score += 3
    elif sleep_hours < 7:
        risk_score += 2

    if screen_time > 8:
        risk_score += 2
    elif screen_time > 6:
        risk_score += 1

    if study_hours > 10:
        risk_score += 2

    if risk_score >= 7:
        return "🔴 HIGH", "⚠️ Rest immediately, reduce workload, and seek support"
    elif risk_score >= 4:
        return "🟡 MODERATE", "⚡ Increase sleep, reduce screen time, and take breaks"
    else:
        return "🟢 LOW", "✅ Great balance! Keep maintaining these habits"
