import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px

def show(db):
    st.title("📈 Analytics")
    st.write("Your wellness trends")
    """
    LEVEL 3: Analytics Dashboard with Weekly Charts
    Track wellness trends over time with visualizations
    """
    st.markdown("""
    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 40px 20px; border-radius: 10px; color: white; margin-bottom: 30px;'>
        <h1 style='margin: 0; color: white;'>📈 Analytics Dashboard</h1>
        <p style='margin-top: 10px; opacity: 0.9;'>Visualize your wellness trends and patterns</p>
    </div>
    """, unsafe_allow_html=True)

    if not db or not st.session_state.user_id:
        st.warning("📊 Please log in to view your analytics")
        return
    
    try:
        user_id = st.session_state.user_id
        
        # Fetch user data
        docs = list(db.collection("dayscores").where("user_id", "==", user_id).stream())
        
        if not docs:
            st.info("📝 No data yet. Complete your daily check-ins to see analytics!")
            return
        
        # Convert to DataFrame
        records = [d.to_dict() for d in docs]
        df = pd.DataFrame(records)
        
        # Convert date to datetime
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values('date')
        
        # Time period selector
        col1, col2, col3 = st.columns(3)
        with col1:
            time_period = st.radio("Select Period:", ["📅 Last 7 Days", "📊 Last 30 Days", "📈 All Time"])
        
        # Filter data based on period
        now = datetime.now()
        if "7 Days" in time_period:
            df = df[df['date'] >= now - timedelta(days=7)]
        elif "30 Days" in time_period:
            df = df[df['date'] >= now - timedelta(days=30)]
        
        st.markdown("---")
        
        # Key Metrics
        st.subheader("📊 Key Metrics")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            avg_score = df['DayScore'].mean()
            st.metric("Avg DayScore", f"{avg_score:.1f}", f"+{avg_score-50:.1f}")
        
        with col2:
            avg_sleep = df['SleepHours'].mean()
            st.metric("Avg Sleep", f"{avg_sleep:.1f}h", delta=f"Target: 8h")
        
        with col3:
            avg_stress = df['StressLevel'].mean()
            st.metric("Avg Stress", f"{avg_stress:.1f}/10", delta=f"Goal: <5")
        
        with col4:
            avg_mood = df['Mood'].mean()
            st.metric("Avg Mood", f"{avg_mood:.1f}/10", delta=f"Goal: >7")
        
        st.markdown("---")
        
        # Charts
        st.subheader("📈 Weekly Trends")
        
        chart_type = st.radio("Chart Type:", ["📉 Line Chart", "📊 Bar Chart", "🔄 All Metrics"], horizontal=True)
        
        if "Line Chart" in chart_type or "All" in chart_type:
            # DayScore trend
            fig_score = go.Figure()
            fig_score.add_trace(go.Scatter(
                x=df['date'], 
                y=df['DayScore'],
                mode='lines+markers',
                name='DayScore',
                line=dict(color='#667eea', width=3),
                marker=dict(size=8)
            ))
            fig_score.update_layout(
                title='DayScore Over Time',
                xaxis_title='Date',
                yaxis_title='Score (0-100)',
                hovermode='x unified',
                height=400,
                template='plotly_white'
            )
            st.plotly_chart(fig_score, use_container_width=True)
        
        if "Bar Chart" in chart_type or "All" in chart_type:
            # Multiple metrics
            fig_metrics = px.bar(
                df.tail(7),
                x='date',
                y=['SleepHours', 'StressLevel', 'Mood'],
                title='Weekly Metrics Comparison',
                labels={'date': 'Date', 'value': 'Value'},
                barmode='group',
                height=400
            )
            fig_metrics.update_layout(template='plotly_white')
            st.plotly_chart(fig_metrics, use_container_width=True)
        
        if "All" in chart_type:
            # Stress vs Mood scatter
            fig_scatter = px.scatter(
                df,
                x='StressLevel',
                y='Mood',
                color='DayScore',
                size='DayScore',
                hover_data=['date'],
                title='Stress vs Mood Relationship',
                labels={'StressLevel': 'Stress Level', 'Mood': 'Mood'},
                color_continuous_scale='RdYlGn',
                height=400
            )
            st.plotly_chart(fig_scatter, use_container_width=True)
        
        st.markdown("---")
        
        # Insights
        st.subheader("💡 Your Insights")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Best day
            best_day = df.loc[df['DayScore'].idxmax()]
            st.write(f"**🏆 Best Day:** {best_day['date'].strftime('%Y-%m-%d')} with score {best_day['DayScore']:.1f}")
            
            # Sleep insight
            if avg_sleep < 7:
                st.warning(f"😴 **Sleep Alert:** Your avg sleep is {avg_sleep:.1f}h. Aim for 7-9 hours.")
            else:
                st.success(f"✅ **Sleep:** Great! Averaging {avg_sleep:.1f} hours per night.")
        
        with col2:
            # Stress insight
            if avg_stress > 7:
                st.warning(f"⚠️ **Stress:** High stress levels ({avg_stress:.1f}/10). Try breathing exercises!")
            else:
                st.success(f"✅ **Stress:** Well managed at {avg_stress:.1f}/10.")
            
            # Mood insight
            st.info(f"😊 **Mood:** Average {avg_mood:.1f}/10. {('Consider talking to someone' if avg_mood < 5 else 'Keep feeling positive!')}")
        
        st.markdown("---")
        
        # Data table
        if st.checkbox("📋 Show Raw Data"):
            st.dataframe(df.sort_values('date', ascending=False))
    
    except Exception as e:
        st.error(f"❌ Error loading analytics: {e}")
