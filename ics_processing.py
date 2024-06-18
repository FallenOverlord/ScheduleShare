from icalendar import Calendar

def extract_events(ics_content):
    calendar = Calendar.from_ical(ics_content)
    events = []
    title = None
    for component in calendar.walk():
        if component.name == "VCALENDAR":
            title = component.get('X-WR-CALNAME', 'Timetable')
        if component.name == "VEVENT":
            event_summary = component.get('SUMMARY')
            event_start = component.get('DTSTART').dt
            event_end = component.get('DTEND').dt
            events.append({
                "Course": event_summary,
                "Start": event_start,
                "End": event_end,
                "Day": event_start.strftime("%A"),
                "Duration": (event_end - event_start).total_seconds() / 3600  # Duration in hours
            })
    return events, title

def calculate_total_course_time(events):
    import pandas as pd
    df = pd.DataFrame(events)
    total_time = df.groupby('Course')['Duration'].sum().reset_index()
    total_time.columns = ['Course', 'Total Hours']
    return total_time
