# DayScore+ Setup Guide

## ✅ Installation

1. **Install required packages:**
```bash
pip install streamlit firebase-admin google-generativeai pandas scikit-learn requests
```

2. **Set your Gemini API Key** (get from [Google AI Studio](https://aistudio.google.com/app/apikey)):

**PowerShell:**
```powershell
$env:GEMINI_API_KEY = "your-gemini-api-key-here"
streamlit run dayscore_app.py
```

**Command Prompt:**
```cmd
set GEMINI_API_KEY=your-gemini-api-key-here
streamlit run dayscore_app.py
```

## 🔧 Configuration

### Firebase Web Config
Your Firebase configuration is already in `firebase_web_config.py`:
- ✅ API Key: `AIzaSyDTXzay8vcfGri0HvgOff1tPgvlbP4eHxk`
- ✅ Project: `dayscore-webapp`
- ✅ Auth Domain: `dayscore-webapp.firebaseapp.com`

### Firebase Service Account
The `serviceAccountKey.json` is used for backend Firestore access.

## 🚀 Features

- ✅ **Real Firebase Authentication** - Users sign up & log in with real credentials
- ✅ **Personalized Data** - Each user sees only their own data
- ✅ **AI Suggestions** - Gemini API provides personalized wellness advice
- ✅ **Burnout Risk Assessment** - Real-time wellness status
- ✅ **Firebase Firestore** - Secure cloud database for all user data

## 📝 First Time Setup

1. Run the app: `streamlit run dayscore_app.py`
2. Click **Sign Up** and create an account
3. Complete your first daily check-in
4. View personalized AI suggestions
5. Track your wellness journey

## 🛑 Troubleshooting

**"Firebase not connected"**
- Check `serviceAccountKey.json` path is correct
- Ensure Firebase project exists

**"API Key invalid"**
- Verify your Gemini API key is set correctly
- Get it from https://aistudio.google.com/app/apikey

**"Login failed: Invalid credentials"**
- Make sure you're using the correct email/password
- Check Firebase Authentication is enabled in console

## 📱 Production Deployment

To deploy on Streamlit Cloud:
1. Push to GitHub
2. Set `GEMINI_API_KEY` secret in Streamlit settings
3. App will auto-authenticate with `serviceAccountKey.json`
