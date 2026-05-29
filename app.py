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
        
        fig.update_layout(
            xaxis_tickformat="%b %d, %I:%M %p",
            height=350,            # Keeps the vertical height short and sleek
            width=1400,            # Forces a long horizontal layout to stretch the bars out
            showlegend=True,
            xaxis_title="Timeline",
            margin=dict(l=50, r=50, t=50, b=50) # Tighter margins for a cleaner look
        )

        # Setting use_container_width=False allows the 1400px width to take effect,
        # creating a smooth horizontal scroll tracking experience on phone screens!
        st.plotly_chart(fig, use_container_width=False)
