import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Tournament Timeline", layout="wide")
st.title("🏆 Tournament Schedule & Timeline")
st.markdown("Add, delete, or update rounds below. Visuals scale automatically to keep bars perfectly proportioned.")

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

# Helper function to cleanly shrink category names for the Y-Axis
def short_cat(cat):
    mapping = {"Elementary (M)": "Ele (M)", "Adult (M)": "Adlt (M)", "Adult (F)": "Adlt (F)"}
    return mapping.get(cat, cat)

# Helper function to cleanly shrink game types for the Y-Axis
def short_game(game):
    mapping = {"Soccer": "Socr", "Basketball": "Bskt", "Chess": "Ches", "Carroms": "Carm", "Cards-28": "Cd28", "Cards-Rummy": "Rumy", "Table Tennis": "TT", "Throwball": "Thrw"}
    return mapping.get(game, game)

# Helper function to map rounds to short codes inside the bars
def short_round(round_text):
    if not isinstance(round_text, str):
        return ""
    r_lower = round_text.lower()
    if "round 1" in r_lower or "rd 1" in r_lower:
        return "R1"
    elif "round 2" in r_lower or "rd 2" in r_lower:
        return "R2"
    elif "semi" in r_lower or "sf" in r_lower:
        return "SF"
    elif "final" in r_lower or "fi" in r_lower:
        return "FI"
    return round_text  # Fallback if it's a unique custom name

# 2. Dynamic Interface Setup
st.subheader("🗓️ Edit Tournament Matches & Rounds")

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

# 3. Data Processing & String Formatting
if not chart_df.empty:
    chart_df['Start'] = pd.to_datetime(chart_df['Start Date & Time'], errors='coerce')
    chart_df['End'] = pd.to_datetime(chart_df['End Date & Time'], errors='coerce')
    
    valid_chart_df = chart_df.dropna(subset=['Start', 'End']).copy()
    
    if not valid_chart_df.empty:
        # Create the short Y-Axis label grouping: "Ele (M) - Socr"
        valid_chart_df['Y_Axis_Label'] = valid_chart_df['Category'].apply(short_cat) + " - " + valid_chart_df['Game Type'].apply(short_game)
        
        # Create the short bar labels: "R1", "SF", "FI"
        valid_chart_df['Bar_Label'] = valid_chart_df['Round/Match'].apply(short_round)

        # 4. Generate the Stacked Timeline Chart
        st.subheader("📊 Schedule Timeline")

        fig = px.timeline(
            valid_chart_df, 
            x_start="Start", 
            x_end="End", 
            y="Y_Axis_Label",        # Group games by unique Category + Sport rows
            color="Game Type",       
            text="Bar_Label",        # Shows ONLY R1, SF, FI inside the blocks
            labels={"Y_Axis_Label": "Bracket / Game"},
            title="Tournament Schedule Progression"
        )

        fig.update_yaxes(autorange="reversed")
        fig.update_traces(textposition="inside")
        
        # Dynamic Height Calculation: Counts unique Y rows and adds baseline padding
        # This keeps the individual bar heights perfectly locked and uniform!
        num_unique_rows = valid_chart_df['Y_Axis_Label'].nunique()
        calculated_height = max(200, (num_unique_rows * 55) + 100)
        
        earliest_game = valid_chart_df['Start'].min()
        four_hours_later = earliest_game + pd.Timedelta(hours=4)
        
        fig.update_layout(
            xaxis_tickformat="%I %p",
            height=calculated_height,  # Applied the fixed bar height formula here
            showlegend=True,
            xaxis_title="Timeline (Drag to scroll / Pinch to zoom)",
            margin=dict(l=10, r=10, t=40, b=10),
            
            xaxis=dict(
                range=[earliest_game, four_hours_later],
                type="date",
                tickmode="linear",
                dtick=3600000  
            )
        )

        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("⏱️ Waiting for a valid date/time format. Please enter like '2026-05-30 09:00 AM'.")
else:
    st.info("Add some games to the schedule table above to populate the timeline visual.")
