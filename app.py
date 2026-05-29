import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Tournament Timeline", layout="wide")
st.title("🏆 Tournament Schedule & Timeline")
st.markdown("Add, delete, or update rounds below. Multiple matches in the same category will automatically line up on the same bar to catch time overlaps.")

# 1. Initialize session data with ultra-safe, explicit strings
if 'schedule_df' not in st.session_state:
    default_data = {
        "Game Type": ["Soccer", "Soccer", "Soccer", "Basketball", "Basketball", "Chess", "Carroms", "Cards-28"],
        "Round/Match": ["Round 1", "Semi-Final", "Final", "Round 1", "Final", "Round 1", "Round 1", "Final"],
        "Category": [
            "Elementary (M)", "Elementary (M)", "Elementary (M)", 
            "Adult (M)", "Adult (M)", 
            "Adult (F)", "Adult (F)", "Adult (F)"
        ],
        "Start Time": ["09:00 AM", "11:00 AM", "02:00 PM", "09:30 AM", "01:00 PM", "09:00 AM", "10:30 AM", "01:00 PM"],
        "End Time": ["10:15 AM", "12:15 PM", "03:15 PM", "11:00 AM", "02:30 PM", "10:00 AM", "11:30 AM", "02:30 PM"]
    }
    st.session_state.schedule_df = pd.DataFrame(default_data)

# 2. Dynamic Interface Setup
st.subheader("🗓️ Edit Tournament Matches & Rounds")
st.caption("💡 Tip: Double-click a cell to edit. You can type times as standard 12-hour format (e.g., 9:30 AM, 1:15 PM).")

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

# Drop rows that are completely empty
chart_df = edited_df.dropna(subset=["Start Time", "End Time", "Game Type", "Round/Match"]).copy()

# 3. Forgiving Data Parsing Logic
if not chart_df.empty:
    chart_df['Start'] = pd.to_datetime(chart_df['Start Time'], errors='coerce')
    chart_df['End'] = pd.to_datetime(chart_df['End Time'], errors='coerce')
    
    # Filter out rows where the user is still actively typing or formatting is completely broken
    valid_chart_df = chart_df.dropna(subset=['Start', 'End']).copy()
    
    if not valid_chart_df.empty:
        valid_chart_df['Display Label'] = valid_chart_df['Game Type'] + " (" + valid_chart_df['Round/Match'] + ")"

        # 4. Generate the Stacked Timeline Chart
        st.subheader("📊 Schedule Timeline")

        fig = px.timeline(
            valid_chart_df, 
            x_start="Start", 
            x_end="End", 
            y="Category",           
            color="Game Type",       
            text="Display Label",    
            labels={"Category": "Participating Category"},
            title="Tournament Schedule Progression by Category"
        )

        fig.update_yaxes(autorange="reversed")
        
        # FIX: Move textposition configuration to update_traces
        fig.update_traces(textposition="inside")
        
        fig.update_layout(
            xaxis_tickformat="%I:%M %p",
            height=400,
            showlegend=True,
            xaxis_title="Time of Day"
        )

        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("⏱️ Waiting for a valid time format. Please enter times like '9:00 AM' or '14:30'.")
else:
    st.info("Add some games to the schedule table above to populate the timeline visual.")
