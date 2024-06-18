import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

def plot_timetable(events, title):
    if not events:
        return None

    df = pd.DataFrame(events)
    df['Start Time'] = df['Start'].dt.hour + df['Start'].dt.minute / 60
    df['End Time'] = df['End'].dt.hour + df['End'].dt.minute / 60
    df['Day'] = pd.Categorical(df['Day'], categories=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'], ordered=True)

    fig = go.Figure()

    color_map = px.colors.qualitative.Set3
    unique_courses = df['Course'].unique()
    color_dict = {course: color_map[i % len(color_map)] for i, course in enumerate(unique_courses)}

    for course in unique_courses:
        course_df = df[df['Course'] == course]
        fig.add_trace(go.Scatter(
            x=course_df['Day'],
            y=course_df['Start Time'],
            mode='markers',
            marker=dict(size=20, color=color_dict[course]),
            name=course,
            text=[f"{course}<br>{start.strftime('%H:%M')} - {end.strftime('%H:%M')}" for course, start, end in zip(course_df['Course'], course_df['Start'], course_df['End'])]
        ))

    fig.update_layout(
        title=title,
        xaxis_title="Day of the Week",
        yaxis_title="Time of Day",
        yaxis=dict(
            tickmode='linear',
            tick0=8,
            dtick=1,
            range=[18, 8]
        ),
        margin=dict(l=20, r=20, t=40, b=20),
        height=600,
        showlegend=True
    )
    fig.update_xaxes(categoryorder='array', categoryarray=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
    return fig
