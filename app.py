import streamlit as st
import pandas as pd
import bcrypt
import streamlit_authenticator as stauth

from db import load_users, save_user, save_profile, load_profile, search_profiles
from ics_processing import extract_events, calculate_total_course_time
from visualization import plot_timetable

# Set page configuration
st.set_page_config(page_title="Schedule Share", page_icon="📅", layout="wide")

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

if 'comparison_data' not in st.session_state:
    st.session_state.comparison_data = []

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

        # Profile Page
        st.sidebar.title("Menu")
        page = st.sidebar.selectbox("Choose a page", ["Home", "Profile", "Search Profiles"])

        if page == "Home":
            st.title("Home")
            st.write("Welcome to Schedule Share!")

        elif page == "Profile":
            st.title("Create Your Profile")
            profile_name = st.text_input("Name", value=name)
            profile_email = st.text_input("Email", value=config['credentials']['usernames'][username]['email'])
            profile_instagram = st.text_input("Instagram Username")
            profile_timetable = st.file_uploader("Upload your timetable (.ics file)", type="ics")

            if st.button("Save Profile"):
                timetable_content = profile_timetable.read() if profile_timetable else None
                save_profile(username, profile_name, profile_email, profile_instagram, timetable_content)
                st.success("Profile created successfully!")

        elif page == "Search Profiles":
            st.title("Search for a Profile")
            search_name = st.text_input("Enter name to search")
            if st.button("Search"):
                profiles = search_profiles(search_name)
                if profiles:
                    for p in profiles:
                        st.write(f"Username: {p[0]}, Name: {p[1]}, Email: {p[2]}, Instagram: {p[3]}")
                        profile = load_profile(p[0])
                        if profile[4]:
                            events, title = extract_events(profile[4])
                            timetable_fig = plot_timetable(events, title)
                            if timetable_fig:
                                st.plotly_chart(timetable_fig, use_container_width=True)

                            # Calculate and display total course time
                            total_course_time = calculate_total_course_time(events)
                            st.write("### Total Course Time per Week")
                            st.dataframe(total_course_time)

                            # Add data to comparison
                            if st.button(f"Compare {p[0]}'s timetable", key=f"comp_{p[0]}"):
                                st.session_state.comparison_data.append((p[0], total_course_time))
                                st.success(f"{p[0]}'s timetable added for comparison")

            # Display Comparison Results
            if st.session_state.comparison_data:
                st.write("## Comparison of Total Course Time")
                comparison_dfs = [df for _, df in st.session_state.comparison_data]
                comparison_df = pd.concat(comparison_dfs, axis=1)
                st.dataframe(comparison_df)

                # Clear comparison data for next search
                st.session_state.comparison_data = []

    elif authentication_status == False:
        st.error("Username/password is incorrect")
    elif authentication_status == None:
        st.warning("Please enter your username and password")

    if st.button("Create a new account"):
        st.session_state.register = True
