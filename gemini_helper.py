import os

# Try to import Gemini API
genai = None
USING_GENAI = False

try:
    import google.genai as genai
    USING_GENAI = True
except ImportError:
    # Fallback: API not available, will use hardcoded suggestions
    pass

# Initialize Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

def get_ai_suggestion(score, stress, mood, sleep_hours, study_hours, screen_time):
    """
    Get personalized AI suggestions based on DayScore and inputs
    Falls back to hardcoded suggestions if API unavailable.
    """
    if not USING_GENAI or not GEMINI_API_KEY:
        # Use fallback suggestions
        return get_fallback_suggestion(score, stress, mood, sleep_hours, study_hours, screen_time)
    
    try:
        client = genai.Client(api_key=GEMINI_API_KEY)
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=_build_prompt(score, stress, mood, sleep_hours, study_hours, screen_time)
        )
        return response.text
    
    except Exception as e:
        print(f"Gemini API error: {e}")
        return get_fallback_suggestion(score, stress, mood, sleep_hours, study_hours, screen_time)

def _build_prompt(score, stress, mood, sleep_hours, study_hours, screen_time):
    """Build the prompt for Gemini"""
    return f"""
You are a wellness coach AI helping a student understand their daily well-being score.
Analyze this student's data and provide personalized, encouraging feedback.

**Today's Data:**
- DayScore: {score}/100
- Stress Level: {stress}/10
- Mood: {mood}/10
- Sleep Hours: {sleep_hours}
- Study Hours: {study_hours}
- Screen Time: {screen_time} hours

**Your Task:**
1. Explain WHY their score is {score} (high/low/moderate)
2. Identify their STRONGEST area (what they did well)
3. Identify ONE area for improvement
4. Give 2-3 specific, actionable recovery tips
5. Add an encouraging emoji at the end

Keep response to 3-4 sentences max. Be warm, supportive, and practical.
"""

def get_fallback_suggestion(score, stress, mood, sleep_hours, study_hours, screen_time):
    """Fallback suggestions when API is unavailable"""
    
    suggestions = []
    
    # Score explanation
    if score >= 80:
        suggestions.append(f"🌟 **Excellent score!** You're maintaining great balance with {sleep_hours}h sleep and manageable stress.")
    elif score >= 60:
        suggestions.append(f"👍 **Good effort!** Your {mood}/10 mood is solid. A bit more rest could boost your score.")
    else:
        suggestions.append(f"💪 **Recovery needed.** Your stress level ({stress}/10) is high. Let's focus on rest today.")
    
    # Stress recommendations
    if stress >= 7:
        suggestions.append("🌬️ **Stress tip:** Try a breathing exercise (4s inhale, 4s hold, 6s exhale)")
    elif stress >= 5:
        suggestions.append("🎮 **Relax:** Take a short break with one of our calm games")
    
    # Sleep recommendations
    if sleep_hours < 7:
        suggestions.append("😴 **Sleep is key:** Aim for 7-9 hours tomorrow—it's your best tool!")
    
    # Screen time recommendations
    if screen_time > 6:
        suggestions.append("📱 **Screen time alert:** Try reducing by 1 hour tomorrow—your eyes will thank you")
    
    # Study balance
    if study_hours > 8:
        suggestions.append("📚 **Study overload:** You're pushing hard! Balance with breaks and movement")
    
    suggestions.append("\n✨ Keep checking in daily to track your progress!")
    
    return "\n\n".join(suggestions)

def get_burnout_risk(stress, sleep_hours, screen_time, study_hours):
    """
    Assess burnout risk level
    
    Returns:
        tuple: (risk_level, recommendation)
    """
    risk_score = 0
    
    # Calculate risk factors
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
    
    # Determine risk level
    if risk_score >= 7:
        return "🔴 HIGH", "⚠️ Take immediate action: Rest now, reduce workload, seek support"
    elif risk_score >= 4:
        return "🟡 MODERATE", "⚡ Be proactive: Increase sleep, reduce screen time, take breaks"
    else:
        return "🟢 LOW", "✅ Great job managing stress! Keep up these healthy habits"
