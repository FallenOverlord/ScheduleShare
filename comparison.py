import plotly.graph_objects as go

def plot_comparison(data):
    usernames = [item[0] for item in data]
    total_hours = [item[1] for item in data]

    fig = go.Figure(
        data=[go.Bar(name='Total Course Hours', x=usernames, y=total_hours)],
        layout_title_text="Comparison of Total Course Time"
    )
    return fig
