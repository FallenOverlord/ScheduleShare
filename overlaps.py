import pandas as pd
from ics_processing import extract_events

def find_overlaps(events1, events2):
    df1 = pd.DataFrame(events1)
    df2 = pd.DataFrame(events2)

    # Fill missing locations with a placeholder to avoid merge issues
    df1['Location'] = df1['Location'].fillna('Unknown')
    df2['Location'] = df2['Location'].fillna('Unknown')

    # Ensure the 'Day' field is included
    df1['Day'] = df1['Start'].dt.strftime('%A')
    df2['Day'] = df2['Start'].dt.strftime('%A')

    # Find overlaps based on Start Time, End Time, and Location
    overlaps = pd.merge(df1, df2, on=['Start', 'End', 'Location', 'Day'])
    overlaps['Course'] = overlaps['Course_x']  # Choose one of the course columns to retain
    overlaps = overlaps[['Course', 'Start', 'End', 'Location', 'Day']]  # Select relevant columns
    return overlaps.to_dict('records')

def get_overlapping_courses(timetable1, timetable2):
    events1, _ = extract_events(timetable1)
    events2, _ = extract_events(timetable2)
    return find_overlaps(events1, events2)
