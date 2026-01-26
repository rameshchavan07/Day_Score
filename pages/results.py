import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import date

def show(db):
    st.header("😄 Your Day Avatar")
    
    user_id = "shivani_123"
    today_doc = db.collection("dayscores").document(f"{user_id}_{date.today()}").get()
    
    if today_doc.exists:
        data = today_doc.to_dict()
        dayscore = data['dayscore']
        st.metric("🎯 DayScore", f"{dayscore:.2f}")
        
        # Progress bar
        st.progress(min(int(dayscore), 100))
        
        # Streak / XP (dummy values)
        st.write("🔥 Streak: 3 days")
        st.write("⭐ XP Gained: +78")
        
        # Burnout risk calculation (simple logic)
        if dayscore > 80:
            risk = "Low 🟢"
        elif dayscore > 50:
            risk = "Medium 🟡"
        else:
            risk = "High 🔴"
        st.write(f"🧠 Burnout Risk: {risk}")
        
        # Explainable AI Panel
        st.info("Risk increased due to low sleep and high screen time")
    else:
        st.warning("No data for today. Please do Daily Check-In first.")
