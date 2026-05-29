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
        
        # Define the exact 12-hour window for the default mobile view (First day: 8 AM to 8 PM)
        default_start_view = "2026-05-30 08:00:00"
        default_end_view = "2026-05-30 20:00:00"
        
        fig.update_layout(
            xaxis_tickformat="%b %d, %I:%M %p",
            height=300,                          # Slimmer vertical footprint for phone screens
            showlegend=True,
            xaxis_title="Timeline (Drag to scroll / Pinch to zoom)",
            margin=dict(l=10, r=10, t=40, b=10), # Tiny margins so it hugs the mobile edges perfectly
            
            # This locks the initial screen view to your preferred 12-hour window
            xaxis=dict(
                range=[default_start_view, default_end_view],
                type="date"
            )
        )

        # We switch this back to True so the chart framework resizes beautifully 
        # into the mobile screen layout, relying on Plotly's inner zoom instead of browser scrolling.
        st.plotly_chart(fig, use_container_width=True)
