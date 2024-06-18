import plotly.graph_objects as go

def plot_bar_chart(user1, time1, user2, time2):
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=[user1, user2],
        y=[time1, time2],
        marker_color=['#1f77b4', '#ff7f0e'],  # Example colors, you can customize them
    ))

    fig.update_layout(
        title="Total Course Hours Comparison",
        xaxis_title="Users",
        yaxis_title="Total Hours",
        yaxis=dict(
            tickmode='linear',
            tick0=10,
            dtick=5,
            range=[10, 30]
        ),
        margin=dict(l=20, r=20, t=40, b=20),
        height=400,
        showlegend=False
    )

    return fig

def show_pie_chart(timetable):
    # Generate and display the pie chart
    pie_chart_fig = plot_pie_chart(timetable)
    if pie_chart_fig:
        st.plotly_chart(pie_chart_fig, use_container_width=True)