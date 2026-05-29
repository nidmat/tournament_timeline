import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, time

st.set_page_config(page_title="Tournament Timeline", layout="wide")
st.title("🏆 Tournament Schedule & Timeline")
st.markdown("Update the game times in the table below to see the timeline chart update automatically.")

# 1. Initialize default mock data for your specific 8 games and 3 categories
if 'schedule_df' not in st.session_state:
    default_data = {
        "Game": [
            "Soccer", "Chess", "Carroms", "Cards-Rummy", 
            "Cards-28", "Basketball", "Table Tennis", "Throwball"
        ],
        "Category": [
            "Elementary (M)", "Adult (M)", "Adult (F)", "Adult (M)", 
            "Adult (F)", "Elementary (M)", "Adult (M)", "Adult (F)"
        ],
        "Start Time": [time(9, 0), time(9, 0), time(10, 30), time(11, 0), 
                       time(13, 0), time(14, 0), time(15, 30), time(16, 0)],
        "End Time": [time(10, 30), time(10, 30), time(12, 0), time(12, 30), 
                     time(14, 30), time(15, 30), time(17, 0), time(17, 30)]
    }
    st.session_state.schedule_df = pd.DataFrame(default_data)

# 2. Interactive Data Editor Interface
st.subheader("🗓️ Edit Game Schedule")
edited_df = st.data_editor(
    st.session_state.schedule_df,
    num_rows="fixed",
    use_container_width=True,
    column_config={
        "Game": st.column_config.TextColumn("Game Name", disabled=True),
        "Category": st.column_config.SelectboxColumn(
            "Category",
            options=["Elementary (M)", "Adult (M)", "Adult (F)"],
            required=True
        ),
        "Start Time": st.column_config.TimeColumn("Start Time", format="hh:mm a", step=900, required=True),
        "End Time": st.column_config.TimeColumn("End Time", format="hh:mm a", step=900, required=True)
    }
)

# Save edits to session state
st.session_state.schedule_df = edited_df

# 3. Process Data for the Timeline Chart
chart_df = edited_df.copy()
chart_df['Start'] = chart_df['Start Time'].apply(lambda t: datetime.combine(datetime.today(), t))
chart_df['End'] = chart_df['End Time'].apply(lambda t: datetime.combine(datetime.today(), t))

# 4. Generate the Stacked Timeline Chart
st.subheader("📊 Schedule Timeline")

fig = px.timeline(
    chart_df, 
    x_start="Start", 
    x_end="End", 
    y="Category",       # Grouping by category to easily spot overlaps
    color="Game",       # Distinct colors for each game type
    text="Game",        # Displays game name inside the timeline bar
    labels={"Category": "Participating Category"},
    title="Game Overlaps by Category"
)

# Clean up chart layout
fig.update_yaxes(autorange="reversed") # Keeps categories ordered cleanly
fig.update_layout(
    xaxis_tickformat="%I:%M %p",       # 12-hour AM/PM format
    height=400,
    showlegend=True,
    xaxis_title="Time of Day"
)

st.plotly_chart(fig, use_container_width=True)
