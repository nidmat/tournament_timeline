import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Tournament Timeline", layout="wide")
st.title("🏆 Tournament Schedule & Timeline")
st.markdown("Add, delete, or update rounds below. You can include both the Date and Time in the fields to manage multi-day tournaments.")

# 1. Initialize session data with Date and Time combined
if 'schedule_df' not in st.session_state:
    default_data = {
        "Game Type": ["Soccer", "Soccer", "Soccer", "Basketball", "Basketball", "Chess", "Carroms", "Cards-28"],
        "Round/Match": ["Round 1", "Semi-Final", "Final", "Round 1", "Final", "Round 1", "Round 1", "Final"],
        "Category": [
            "Elementary (M)", "Elementary (M)", "Elementary (M)", 
            "Adult (M)", "Adult (M)", 
            "Adult (F)", "Adult (F)", "Adult (F)"
        ],
        "Start Date & Time": [
            "2026-05-30 09:00 AM", "2026-05-30 11:00 AM", "2026-05-30 02:00 PM", 
            "2026-05-31 09:30 AM", "2026-05-31 01:00 PM", 
            "2026-05-30 09:00 AM", "2026-05-30 10:30 AM", "2026-05-31 01:00 PM"
        ],
        "End Date & Time": [
            "2026-05-30 10:15 AM", "2026-05-30 12:15 PM", "2026-05-30 03:15 PM", 
            "2026-05-31 11:00 AM", "2026-05-31 02:30 PM", 
            "2026-05-30 10:00 AM", "2026-05-30 11:30 AM", "2026-05-31 02:30 PM"
        ]
    }
    st.session_state.schedule_df = pd.DataFrame(default_data)

# 2. Dynamic Interface Setup
st.subheader("🗓️ Edit Tournament Matches & Rounds")
st.caption("💡 Tip: Enter dates and times together (e.g., '2026-05-30 9:30 AM' or '05/30/2026 13:00').")

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
chart_df = edited_df.dropna(subset=["Start Date & Time", "End Date & Time", "Game Type", "Round/Match"]).copy()

# 3. Forgiving Data Parsing Logic
if not chart_df.empty:
    chart_df['Start'] = pd.to_datetime(chart_df['Start Date & Time'], errors='coerce')
    chart_df['End'] = pd.to_datetime(chart_df['End Date & Time'], errors='coerce')
    
    # Filter out rows where the parsing is incomplete
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
        fig.update_traces(textposition="inside")
        
        # Find the first game's start time and add 4 hours to make the default view wider
        earliest_game = valid_chart_df['Start'].min()
        four_hours_later = earliest_game + pd.Timedelta(hours=4)
        
        fig.update_layout(
            xaxis_tickformat="%I %p",
            height=350,            
            showlegend=True,
            xaxis_title="Timeline (Drag to scroll / Pinch to zoom)",
            margin=dict(l=10, r=10, t=40, b=10),
            
            xaxis=dict(
                range=[earliest_game, four_hours_later],
                type="date",
                tickmode="linear",
                dtick=3600000  # Forces a grid mark exactly every 1 hour (in milliseconds)
            )
        )

        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("⏱️ Waiting for a valid date/time format. Please enter like '2026-05-30 09:00 AM'.")
else:
    st.info("Add some games to the schedule table above to populate the timeline visual.")
