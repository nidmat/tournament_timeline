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
        
        # Find the first game's start time and add 12 hours for the initial view
        earliest_game = valid_chart_df['Start'].min()
        twelve_hours_later = earliest_game + pd.Timedelta(hours=12)
        
        fig.update_layout(
            xaxis_tickformat="%I %p",             # Simplifies labels to just hour format (e.g., 09 AM, 10 AM)
            height=350,            
            showlegend=True,
            xaxis_title="Timeline (Drag to scroll / Pinch to zoom)",
            margin=dict(l=10, r=10, t=40, b=10),
            
            xaxis=dict(
                range=[earliest_game, twelve_hours_later],
                type="date",
                tickmode="linear",                # Enables manual control over the grid lines
                dtick=3600000                     # Forces a grid mark exactly every 1 hour (in milliseconds)
            )
        )

        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("⏱️ Waiting for a valid date/time format. Please enter like '2026-05-30 09:00 AM'.")
else:
    st.info("Add some games to the schedule table above to populate the timeline visual.")
