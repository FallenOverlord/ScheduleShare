import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from io import BytesIO
from icalendar import Calendar, Event

# Function to add event to the schedule
def add_event(events, event):
    events.append(event)
    return events

# Function to delete event from the schedule
def delete_event(events, event_index):
    if 0 <= event_index < len(events):
        del events[event_index]
        st.rerun()
    return events

# Function to edit an event
def edit_event(events, event_index, new_event):
    if 0 <= event_index < len(events):
        events[event_index] = new_event
    return events

# Function to convert DataFrame to .ics
def dataframe_to_ics(df):
    cal = Calendar()
    for index, row in df.iterrows():
        event = Event()
        event.add('summary', row['name'])
        event.add('dtstart', datetime.combine(row['date'], row['start_time']))
        event.add('dtend', datetime.combine(row['date'], row['end_time']))
        cal.add_component(event)
    return cal.to_ical()

# Function to display the schedule creator interface
def schedule_creator():
    st.title("Create Your Custom Schedule 🚀")

    # Initialize session state for events
    if 'events' not in st.session_state:
        st.session_state.events = []

    # Input fields for event details
    event_name = st.text_input("Event Name")
    event_date = st.date_input("Event Date")
    start_time = st.time_input("Start Time")
    end_time = st.time_input("End Time", value=(datetime.now() + timedelta(hours=1)).time())

    if st.button("Add Event"):
        event = {
            'name': event_name,
            'date': event_date,
            'start_time': start_time,
            'end_time': end_time
        }
        st.session_state.events = add_event(st.session_state.events, event)
        st.success("Event added successfully!")

    # Display current events
    st.write("### Current Schedule")
    for i, event in enumerate(st.session_state.events):
        st.write(f"{i+1}. {event['name']} - {event['date']} - {event['start_time']} to {event['end_time']}")
        if st.button(f"Delete Event {i+1}"):
            st.session_state.events = delete_event(st.session_state.events, i)
            st.success("Event deleted successfully!")

        if st.button(f"Edit Event {i+1}"):
            new_event_name = st.text_input(f"New Event Name {i+1}", value=event['name'])
            new_event_date = st.date_input(f"New Event Date {i+1}", value=event['date'])
            new_start_time = st.time_input(f"New Start Time {i+1}", value=event['start_time'])
            new_end_time = st.time_input(f"New End Time {i+1}", value=event['end_time'])
            new_event = {
                'name': new_event_name,
                'date': new_event_date,
                'start_time': new_start_time,
                'end_time': new_end_time
            }
            st.session_state.events = edit_event(st.session_state.events, i, new_event)
            st.success("Event edited successfully!")

    # Display final schedule in a table
    if st.session_state.events:
        st.write("### Final Schedule")
        schedule_df = pd.DataFrame(st.session_state.events)
        st.write(schedule_df)
        
        ics_data = dataframe_to_ics(schedule_df)
        st.download_button(label="Download Schedule as ICS", data=ics_data, file_name="mySchedule.ics")

if __name__ == "__main__":
    schedule_creator()
