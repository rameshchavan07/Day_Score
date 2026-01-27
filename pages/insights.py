import streamlit as st
import pandas as pd

def show(db):
    st.title("💡 Insights")
    if db and st.session_state.user_id:
        try:
            user_id = st.session_state.user_id
            docs = db.collection("dayscores") \
                .where("user_id", "==", user_id) \
                .stream()

            records = []
            for d in docs:
                records.append(d.to_dict())
            
            if records:
                df = pd.DataFrame(records)
                st.dataframe(df)
                
                # Display insights
                st.subheader("Key Metrics")
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Avg DayScore", f"{df['DayScore'].mean():.1f}")
                with col2:
                    st.metric("Avg Sleep", f"{df['SleepHours'].mean():.1f} hrs")
                with col3:
                    st.metric("Avg Stress", f"{df['StressLevel'].mean():.1f}")
            else:
                st.info("No data yet. Start with a daily check-in!")
        except Exception as e:
            st.error(f"Error loading data: {e}")
    else:
        st.warning("Please log in to view your insights")