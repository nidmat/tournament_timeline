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
        "Start Time": [time(9, 0), time(11, 0), time(14, 0), time(9, 30), time(13, 0), time(9, 0), time(10, 30), time(13, 0)],
        "End Time": [time(10, 15), time(12, 15), time(15, 15), time(11, 0), time(14, 30), time(10, 0), time(11, 30), time(14, 30)]
    }
    st.session_state.schedule_df = pd.DataFrame(default_data)

# 2. Interactive Data Editor Interface (Set num_rows="dynamic" to allow adding/deleting rows)
st.subheader("🗓️ Edit Tournament Matches & Rounds")
st.caption("💡 Tip: To add a new match, scroll to the bottom of the table and look for the '+' row. To delete, select a row and hit Delete on your keyboard.")

edited_df = st.data_editor(
    st.session_state.schedule_df,
    num_rows="dynamic",
    use_container_width=True,
    column_config={
        "Game Type": st.column_config.SelectboxColumn(
            "Game Type",
            options=["Soccer", "Chess", "Carroms", "Cards-Rummy", "Cards-28", "Basketball", "Table Tennis", "Throwball"],
            required=True
        ),
        "Round/Match": st.column_config.TextColumn("Round / Match Name", placeholder="e.g., Semi-Final", required=True),
        "Category": st.column_config.SelectboxColumn(
            "Category",
            options=["Elementary (M)", "Adult (M)", "Adult (F)"],
            required=True
        ),
        "Start Time": st.column_config.TimeColumn("Start Time", format="hh:mm a", step=900, required=True),
        "End Time": st.column_config.TimeColumn("End Time", format="hh:mm a", step=900, required=True)
    }
)

# Save edits back to session state
st.session_state.schedule_df = edited_df

# Drop completely empty rows if any exist from dynamic additions
chart_df = edited_df.dropna(subset=["Start Time", "End Time", "Game Type", "Round/Match"]).copy()

# 3. Process Data for the Timeline Chart
if not chart_df.empty:
    chart_df['Start'] = chart_df['Start Time'].apply(lambda t: datetime.combine(datetime.today(), t))
    chart_df['End'] = chart_df['End Time'].apply(lambda t: datetime.combine(datetime.today(), t))
    
    # Create a nice label string to display inside the colored bar block
    chart_df['Display Label'] = chart_df['Game Type'] + " (" + chart_df['Round/Match'] + ")"

    # 4. Generate the Stacked Timeline Chart
    st.subheader("📊 Schedule Timeline")

    fig = px.timeline(
        chart_df, 
        x_start="Start", 
        x_end="End", 
        y="Category",           # Keeps one row per major category bracket
        color="Game Type",       # Colors match blocks by sport type (Soccer, Chess, etc.)
        text="Display Label",    # Puts "Soccer (Round 1)" directly inside the bar block
        labels={"Category": "Participating Category"},
        title="Tournament Schedule Progression by Category"
    )

    # Clean up chart layout
    fig.update_yaxes(autorange="reversed")
    fig.update_layout(
        xaxis_tickformat="%I:%M %p",
        height=400,
        showlegend=True,
        xaxis_title="Time of Day",
        textposition="inside"    # Forces text to stay cleanly inside the timeline segments
    )

    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Add some games to the schedule table above to populate the timeline visual.")
