import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, time

st.set_page_config(page_title="Tournament Timeline", layout="wide")
st.title("🏆 Tournament Schedule & Timeline")
st.markdown("Add, delete, or update rounds below. Multiple matches in the same category will automatically line up on the same bar to catch time overlaps.")

# 1. Initialize data with structural support for multiple rounds per game
if 'schedule_df' not in st.session_state:
    default_data = {
        "Game Type": ["Soccer", "Soccer", "Soccer", "Basketball", "Basketball", "Chess", "Carroms", "Cards-28"],
        "Round/Match": ["Round 1", "Semi-Final", "Final", "Round 1", "Final", "Round 1", "Round 1", "Final"],
        "Category": [
            "Elementary (M)", "Elementary (M)", "Elementary (M)", 
            "Adult (M)", "Adult (M)", 
            "Adult (F)", "Adult (F)", "Adult (F)"
        ],
        "Start Time": ["09:00", "11:00", "14:00", "09:30", "13:00", "09:00", "10:30", "13:00"],
        "End Time": ["10:15", "12:15", "15:15", "11:00", "14:30", "10:00", "11:30", "14:30"]
    }
    st.session_state.schedule_df = pd.DataFrame(default_data)

# 2. Simplified Dynamic Interface (Bypasses Python 3.14 column metrics tracking)
st.subheader("🗓️ Edit Tournament Matches & Rounds")
st.caption("💡 Tip: Double-click a cell to edit. To add a row, scroll down and use the '+' row. To delete, select a row and hit Delete.")

edited_df = st.data_editor(
    st.session_state.schedule_df,
    num_rows="dynamic",
    use_container_width=True,
    column_config={
        "Game Type": st.column_config.SelectboxColumn("Game Type", options=["Soccer", "Chess", "Carroms", "Cards-Rummy", "Cards-28", "Basketball", "Table Tennis", "Throwball"]),
        "Category": st.column_config.SelectboxColumn("Category", options=["Elementary (M)", "Adult (M)", "Adult (F)"])
    }
)

st.session_state.schedule_df = edited_df
chart_df = edited_df.dropna().copy()

# 3. Process Data for the Timeline Chart safely using robust string conversion
if not chart_df.empty:
    try:
        # Converts simple text string inputs (e.g. "09:00") straight into Datetime blocks
        chart_df['Start'] = pd.to_datetime(chart_df['Start Time'], format='%H:%M', errors='coerce')
        chart_df['End'] = pd.to_datetime(chart_df['End Time'], format='%H:%M', errors='coerce')
        chart_df = chart_df.dropna(subset=['Start', 'End'])
        
        chart_df['Display Label'] = chart_df['Game Type'] + " (" + chart_df['Round/Match'] + ")"

        # 4. Generate the Stacked Timeline Chart
        st.subheader("📊 Schedule Timeline")

        fig = px.timeline(
            chart_df, 
            x_start="Start", 
            x_end="End", 
            y="Category",           
            color="Game Type",       
            text="Display Label",    
            labels={"Category": "Participating Category"},
            title="Tournament Schedule Progression by Category"
        )

        fig.update_yaxes(autorange="reversed")
        fig.update_layout(
            xaxis_tickformat="%I:%M %p",
            height=400,
            showlegend=True,
            xaxis_title="Time of Day",
            textposition="inside"    
        )

        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error("Please ensure times are entered cleanly in 24-hour HH:MM format (e.g., 09:30 or 14:15).")
else:
    st.info("Add some games to the schedule table above to populate the timeline visual.")
