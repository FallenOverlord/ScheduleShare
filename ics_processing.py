from icalendar import Calendar
import pandas as pd

def extract_events(ics_content):
    calendar = Calendar.from_ical(ics_content)
    events = []

    for component in calendar.walk():
        if component.name == "VEVENT":
            event = {
                'Course': component.get('SUMMARY'),
                'Start': component.get('DTSTART').dt,
                'End': component.get('DTEND').dt,
                'Location': component.get('LOCATION', 'Unknown'),  # Handle missing location
                'Day': component.get('DTSTART').dt.strftime('%A')
            }
            events.append(event)
    
    return events, calendar.get('X-WR-CALNAME', 'Timetable')

def calculate_total_course_time(events):
    # Convert the list of events to a DataFrame
    if not events:
        return pd.DataFrame(columns=['Course', 'Total Hours'])
    
    df = pd.DataFrame(events)
    
    # Ensure 'Start' and 'End' are in datetime format
    df['Start'] = pd.to_datetime(df['Start'])
    df['End'] = pd.to_datetime(df['End'])
    
    # Calculate the duration in hours
    df['Duration'] = (df['End'] - df['Start']).dt.total_seconds() / 3600
    
    # Group by 'Course' and sum the durations
    total_time = df.groupby('Course')['Duration'].sum().reset_index()
    total_time.columns = ['Course', 'Total Hours']
    
    return total_time
    
