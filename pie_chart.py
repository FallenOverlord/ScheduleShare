# pie_chart.py
import pandas as pd
import plotly.express as px
from ics_processing import extract_events
import streamlit as st

def plot_pie_chart(timetable):
    if not timetable:
        return None

    # Extract events from the timetable
    events, _ = extract_events(timetable)
    df = pd.DataFrame(events)

    # Calculate the duration of each event
    df['Duration'] = (df['End'] - df['Start']).dt.total_seconds() / 3600

    # Group by course and calculate the total duration for each course
    course_duration = df.groupby('Course')['Duration'].sum().reset_index()

    # Create a pie chart
    fig = px.pie(course_duration, names='Course', values='Duration', title='Course Time Distribution')
    return fig

def show_pie_chart(timetable):
    # Generate and display the pie chart
    pie_chart_fig = plot_pie_chart(timetable)
    if pie_chart_fig:
        st.plotly_chart(pie_chart_fig, use_container_width=True)