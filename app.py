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
        
        fig.update_layout(
            xaxis_tickformat="%b %d, %I:%M %p",
            height=350,            
            width=1400,            
            showlegend=True,
            xaxis_title="Timeline",
            margin=dict(l=50, r=50, t=50, b=50)
        )

        st.plotly_chart(fig, use_container_width=False)
