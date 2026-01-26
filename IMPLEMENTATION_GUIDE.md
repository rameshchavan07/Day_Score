# DayScore+ Implementation Guide

## 📋 Project Overview

DayScore+ is a well-being & productivity companion that helps students understand burnout risk using AI-generated scores, insights, trends, and calming activities.

---

## 🟢 LEVEL 1: Landing Page + Auth + Firebase Integration ✅ COMPLETE

### Implemented Features:
- ✅ **Landing Page** (`pages/landing.py`)
  - Modern hero section with CSS animations
  - Feature highlights with interactive cards
  - "How it Works" step-by-step guide
  - Animated CTA buttons
  - Responsive design

- ✅ **Login & Signup** (`pages/auth.py`)
  - Email/password authentication
  - Real Firebase Authentication REST API
  - Form validation
  - User account creation
  - Session management

- ✅ **Firebase Setup** (`firebase_config.py`, `firebase_web_config.py`)
  - Firestore database connected
  - Real user authentication
  - User data persistence
  - Score storage and retrieval

### Files:
- `dayscore_app.py` - Main app with auth flow
- `pages/auth.py` - Login/Signup
- `firebase_config.py` - Backend Firebase
- `firebase_web_config.py` - Frontend config

---

## 🟡 LEVEL 2: Main Dashboard + AI Score + Suggestions ✅ COMPLETE

### Core Algorithm: DayScore Calculation

**Location:** `pages/checkin.py` - `calculate_dayscore()` function

**Algorithm Overview:**
```
Baseline: 50 points (neutral)

Sleep (15 pts):     7-9h = perfect, gradual decrease outside range
Mood (15 pts):      Higher is better (1-10 scaled)
Stress (15 pts):    Lower is better (10-level scaled inversely)
Study (10 pts):     3-6h optimal, penalties for extreme
Screen Time (10 pts): <3h optimal, decreases with more
Activity (10 pts):  >5000 steps optimal

Total: 0-100
```

### Implemented Features:
- ✅ **Daily Check-In** (`pages/checkin.py`)
  - Collects: Study hours, Sleep, Screen time, Stress, Mood, Activity
  - Real-time DayScore calculation
  - Fallback algorithm when ML model unavailable
  - Clamped 0-100 score

- ✅ **AI Suggestions** (via `gemini_helper.py`)
  - Gemini API integration (with fallback)
  - Personalized wellness advice
  - Burnout risk assessment
  - Recovery recommendations
  - Contextual action buttons

- ✅ **Firebase Storage**
  - Saves user inputs
  - Stores DayScore
  - Date-based document organization
  - Automatic timestamp

- ✅ **Burnout Risk Assessment**
  - 🟢 LOW: Score > 70, low stress
  - 🟡 MODERATE: Score 50-70, moderate risk
  - 🔴 HIGH: Score < 50, high risk

### Files:
- `pages/checkin.py` - Main check-in interface
- `gemini_helper.py` - AI suggestions engine
- `pages/results.py` - Daily results display

---

## 🟠 LEVEL 3: User Profile + Analytics Dashboard ✅ COMPLETE

### Implemented Features:
- ✅ **User Profile** (`pages/profile.py`)
  - Username and email display
  - Check-in streak tracking
  - Average DayScore calculation
  - Settings panel
  - Real user data integration

- ✅ **Analytics Dashboard** (`pages/analytics.py`)
  - Weekly/Monthly/All-time views
  - Interactive Plotly charts:
    - DayScore trend line
    - Weekly metrics bar chart
    - Stress vs Mood scatter plot
  - Key metrics cards:
    - Average DayScore
    - Average Sleep
    - Average Stress
    - Average Mood
  - Personalized insights
  - Data export capability
  - Raw data table view

- ✅ **Enhanced Insights** (`pages/insights.py`)
  - User score history
  - Aggregate statistics
  - Trend analysis
  - Pattern detection

### Files:
- `pages/profile.py` - User profile page
- `pages/analytics.py` - Analytics dashboard (NEW)
- `pages/insights.py` - Insights page
- `pages/results.py` - Daily results

---

## 🔵 LEVEL 4: Games + Breathing Experience ✅ COMPLETE

### Implemented Features:
- ✅ **Games Page** (`pages/games.py`)
  - 🧩 Puzzle category (Zen Puzzles, Color Match)
  - 🎨 Cozy Games (Garden Sim, Café Manager)
  - 🎯 Focus Games (Memory Master, Focus Quest)
  - Beautiful UI with interactive buttons
  - Ready for itch.io integration

- ✅ **Breathing Exercises** (`pages/breathing.py`)
  - 🌊 4-7-8 Relaxation (4-7-8 pattern)
  - 📿 Box Breathing (4-4-4-4 pattern)
  - 🧘 Extended Exhale (4-8 pattern)
  - 💤 Sleep Prep (4-4-6 pattern)
  - Customizable duration (1-10 minutes)
  - Optional background music
  - CSS animation (breathing circle)
  - Detailed breathing instructions
  - Tips for effective practice

### Files:
- `pages/games.py` - Games page (NEW)
- `pages/breathing.py` - Breathing exercises (NEW)

---

## 📊 Achievement System

**Badges Unlocked by:**
- 🌟 Early Riser: 8+ hours sleep
- 💪 Active Streak: 7 days of exercise
- 🧠 Scholar: 50+ hours studying
- 🌙 Sleep Champion: 8+ hours for 7 days
- 📚 Bookworm: 10 study sessions

**Location:** `pages/achievements.py`

---

## 🔧 Technology Stack

### Frontend
- **Streamlit** - Web framework
- **Plotly** - Interactive charts
- **CSS Animations** - Visual effects

### Backend & Auth
- **Firebase Authentication** - User login/signup
- **Firebase Firestore** - Real-time database
- **Firebase Admin SDK** - Backend operations

### AI & ML
- **Google Gemini API** - AI suggestions
- **Scikit-learn** - ML model (optional)
- **Pandas** - Data processing

---

## 🚀 Running the App

### Setup
```bash
pip install streamlit firebase-admin google-genai pandas scikit-learn requests plotly
```

### Environment Variables
```powershell
$env:GEMINI_API_KEY = "your-key-from-aistudio.google.com"
```

### Run
```bash
streamlit run dayscore_app.py
```

### Features by Page
| Page | Level | Status | Purpose |
|------|-------|--------|---------|
| Landing | 1 | ✅ Done | Marketing/onboarding |
| Auth (Login/Signup) | 1 | ✅ Done | User authentication |
| Daily Check-In | 2 | ✅ Done | Data collection + scoring |
| Results Dashboard | 2 | ✅ Done | Daily score display |
| Analytics | 3 | ✅ Done | Trend visualization |
| Profile | 3 | ✅ Done | User profile |
| Achievements | 3 | ✅ Done | Badge system |
| Breathing | 4 | ✅ Done | Stress relief |
| Games | 4 | ✅ Done | Relaxation activities |

---

## 📈 Future Enhancements

- [ ] Integrate itch.io game embeds
- [ ] Add music/ambient sounds
- [ ] SMS/Email notifications
- [ ] Social sharing features
- [ ] Predictive analytics
- [ ] Mobile app version
- [ ] Wearable integration
- [ ] Advanced burnout prediction

---

## 🐛 Troubleshooting

**Blank Pages?**
- Check imports in terminal
- Verify all dependencies installed

**Firebase Errors?**
- Check service account key path
- Verify authentication enabled

**Gemini Errors?**
- Set GEMINI_API_KEY environment variable
- App uses fallback suggestions if API unavailable

**Model Warnings?**
- Sklearn version mismatch is non-critical
- App automatically falls back to calculation formula

---

## 📝 Database Schema

### Collections
```
users/
  {user_id}/
    - name: string
    - email: string
    - created_at: timestamp

dayscores/
  {user_id}_{date}/
    - user_id: string
    - date: string (YYYY-MM-DD)
    - DayScore: number (0-100)
    - StressLevel: number (1-10)
    - Mood: number (1-10)
    - SleepHours: number
    - StudyHours: number
    - ScreenTimeHours: number
    - Steps: number
```

---

## ✨ Key Achievements

✅ Complete LEVEL 1: Auth + Landing
✅ Complete LEVEL 2: Scoring + AI
✅ Complete LEVEL 3: Analytics
✅ Complete LEVEL 4: Games + Breathing
✅ Real Firebase integration
✅ Real user authentication
✅ AI-powered suggestions
✅ Beautiful animations
✅ Responsive design

---

**Built with ❤️ for student wellness**
