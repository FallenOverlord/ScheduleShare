import streamlit as st
import pandas as pd
from icalendar import Calendar
import datetime
from collections import defaultdict
from io import BytesIO
import sqlite3
import bcrypt
import streamlit_authenticator as stauth

# Set page configuration
st.set_page_config(page_title="Schedule Share", page_icon="📅", layout="wide")

# Function to get database connection
def get_db_connection():
    conn = sqlite3.connect('users.db')
    return conn

# Function to load users from database
def load_users():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT username, email, name, password FROM users')
    rows = c.fetchall()
    conn.close()
    users = {
        'usernames': {}
    }
    for row in rows:
        users['usernames'][row[0]] = {
            'email': row[1],
            'name': row[2],
            'password': row[3]
        }
    return users

# Function to save new user to database
def save_user(username, email, name, password):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('INSERT INTO users (username, email, name, password) VALUES (?, ?, ?, ?)',
              (username, email, name, password))
    conn.commit()
    conn.close()

# Load users from database
config = {
    'credentials': load_users(),
    'cookie': {
        'expiry_days': 30,
        'name': 'some_cookie_name',
        'key': 'some_signature_key'
    },
    'preauthorized': {
        'emails': [
            'johndoe@example.com',
            'janedoe@example.com'
        ]
    }
}

# Debugging: Print the loaded users
st.write("Loaded users:", config['credentials'])

# Setup the authenticator
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

# Registration form
if 'register' not in st.session_state:
    st.session_state.register = False

if st.session_state.register:
    st.title("Create a New Account")
    new_username = st.text_input("Username")
    new_email = st.text_input("Email")
    new_name = st.text_input("Full Name")
    new_password = st.text_input("Password", type="password")
    new_password_confirm = st.text_input("Confirm Password", type="password")

    if st.button("Register"):
        if new_password != new_password_confirm:
            st.error("Passwords do not match!")
        else:
            hashed_password = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt()).decode()
            save_user(new_username, new_email, new_name, hashed_password)
            st.success("Account created successfully!")
            st.session_state.register = False

    if st.button("Go back to login"):
        st.session_state.register = False

else:
    # Login process
    try:
        name, authentication_status, username = authenticator.login(
            location='main',
            fields={
                'Form name': 'Login',
                'Username': 'Username',
                'Password': 'Password',
                'Login': 'Login'
            }
        )
    except KeyError as e:
        st.error(f"KeyError: {e}")
        st.stop()

    if authentication_status:
        st.write(f"Welcome *{name}*")
        authenticator.logout('Logout', 'main')

        # Function to normalize time
        def normalize_time(dt):
            if isinstance(dt, datetime.datetime):
                return dt.replace(tzinfo=None).time()
            return dt

        # Function to extract events from .ics file content
        def extract_events(file_content):
            events = []
            calendar = Calendar.from_ical(file_content)
            for component in calendar.walk():
                if component.name == "VEVENT":
                    event_summary = component.get('SUMMARY')
                    event_start = normalize_time(component.get('DTSTART').dt)
                    event_end = normalize_time(component.get('DTEND').dt)
                    event_location = component.get('LOCATION')
                    events.append({
                        "Course Name": event_summary,
                        "Start Time": event_start,
                        "End Time": event_end,
                        "Location": event_location
                    })
            return events

        # Function to compare timetables
        def compare_timetables(timetables):
            common_courses = defaultdict(int)
            total_courses = sum(len(timetable) for timetable in timetables)
            
            reference_timetable = timetables[0]
            reference_set = set((course["Course Name"], course["Start Time"], course["End Time"], course["Location"]) for course in reference_timetable)
            
            for timetable in timetables[1:]:
                current_set = set((course["Course Name"], course["Start Time"], course["End Time"], course["Location"]) for course in timetable)
                for course in reference_set:
                    if course in current_set:
                        common_courses[course] += 1
            
            common_courses_set = {course for course, count in common_courses.items() if count == len(timetables) - 1}
            common_percentage = (len(common_courses_set) / total_courses) * 100
            
            return common_courses_set, common_percentage

        # Load custom CSS
        def local_css(file_name):
            with open(file_name) as f:
                st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

        local_css("style.css")

        # Sidebar
        st.sidebar.title("Schedule Share")
        st.sidebar.write("""
        This app helps you find common courses among multiple calendars.
        - Upload your `.ics` files.
        - View the common courses.
        - Download the common courses as an Excel file.
        """)

        st.title("Upload Your Calendars")
        uploaded_files = st.file_uploader("Upload your .ics files", accept_multiple_files=True, type="ics")

        if uploaded_files:
            timetables = [extract_events(file.read()) for file in uploaded_files]
            common_courses, common_percentage = compare_timetables(timetables)
            
            st.write(f"### Percentage of common courses: {common_percentage:.2f}%")
            
            if common_courses:
                df = pd.DataFrame(list(common_courses), columns=["Course Name", "Start Time", "End Time", "Location"])
                st.write("### Common Courses")
                st.dataframe(df)
                
                output = BytesIO()
                df.to_excel(output, index=False)
                output.seek(0)
                st.download_button(label="Download Common Courses as Excel", data=output, file_name="common_courses.xlsx")

    elif authentication_status == False:
        st.error("Username/password is incorrect")
    elif authentication_status == None:
        st.warning("Please enter your username and password")

    if st.button("Create a new account"):
        st.session_state.register = True
